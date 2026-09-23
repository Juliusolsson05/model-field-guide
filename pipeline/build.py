"""Join every parsed source into one validated snapshot.

The snapshot is the machine layer (data/snapshot.json) and the only input the
renderer sees. It must be byte-deterministic for the same upstream data:
sorted keys, sorted records, fixed rounding, and NO fetch timestamp anywhere.
Dates in it are each source's own as-of date. That is what makes "commit only
if changed" meaningful and keeps the nightly diff readable.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from . import parse

ROOT = Path(__file__).resolve().parent.parent
MODELS_YAML = ROOT / "pipeline" / "models.yaml"

SOURCES = {
    "epoch": {"name": "Epoch AI Benchmarking Hub", "license": "CC-BY-4.0", "url": "https://epoch.ai/benchmarks"},
    "lmarena": {"name": "LMArena leaderboard dataset", "license": "CC-BY-4.0",
                "url": "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset"},
    "models_dev": {"name": "models.dev", "license": "MIT", "url": "https://models.dev"},
    "tau2": {"name": "tau2-bench leaderboard (Sierra)", "license": "MIT", "url": "https://github.com/sierra-research/tau2-bench"},
    "steel": {"name": "Steel agent leaderboard", "license": "MIT", "url": "https://leaderboard.steel.dev"},
}

# Row-count floors. An upstream that returns an HTML error page or an empty
# list must fail loudly, not publish an empty table that looks like "no model
# scored anything". Floors are deliberately far below today's counts.
MIN_MODELS_DEV = 15   # of 21 allowlisted
MIN_SCORES = {"epoch": 40, "lmarena": 20}


class ValidationError(Exception):
    pass


def load_allowlist(path: Path = MODELS_YAML) -> list[dict]:
    models = yaml.safe_load(path.read_text())["models"]
    ids = [m["id"] for m in models]
    if len(ids) != len(set(ids)):
        raise ValidationError(f"duplicate ids in models.yaml: {ids}")
    return models


def build(raw: Path, allow: list[dict], prev: dict | None = None, failed: set[str] = frozenset()) -> dict:
    """Parse raw/ into a snapshot. `failed` sources reuse `prev` rows.

    Reusing yesterday's rows for a source that failed to download keeps one
    flaky upstream from blanking a table; the source's as_of stays at the old
    date, so _meta.md shows readers exactly how old that part is.
    """
    src = lambda key: {m["id"]: m["sources"][key] for m in allow if m["sources"].get(key)}  # noqa: E731

    snap_sources: dict[str, dict] = {}
    scores: list[dict] = []
    facts: dict[str, dict] = {}
    present: dict[str, set[str]] = {}

    def reuse(name: str) -> None:
        if not prev or name not in prev.get("sources", {}):
            raise ValidationError(f"{name}: download failed and there is no previous snapshot to fall back on")
        snap_sources[name] = {**prev["sources"][name], "stale": True}
        scores.extend(s for s in prev["scores"] if s["source"] == name)
        present[name] = set(prev["sources"][name].get("present", []))

    # Epoch
    if "epoch" in failed:
        reuse("epoch")
    else:
        groups = {g: mid for mid, g in src("epoch").items()}
        s, groups_present, as_of = parse.parse_epoch(raw / "epoch" / "benchmark_data.zip", groups)
        scores += s
        present["epoch"] = {groups[g] for g in groups_present if g in groups}
        snap_sources["epoch"] = {"as_of": as_of}

    # LMArena
    if "lmarena" in failed:
        reuse("lmarena")
    else:
        s, as_of = parse.parse_lmarena(raw / "lmarena", src("lmarena"))
        scores += s
        present["lmarena"] = {x["model"] for x in s}
        snap_sources["lmarena"] = {"as_of": as_of}

    # models.dev
    if "models_dev" in failed:
        if not prev:
            raise ValidationError("models_dev: download failed and no previous snapshot")
        facts = {k: v["facts"] for k, v in prev["models"].items() if v.get("facts")}
        snap_sources["models_dev"] = {**prev["sources"]["models_dev"], "stale": True}
        present["models_dev"] = set(prev["sources"]["models_dev"].get("present", []))
    else:
        facts, as_of = parse.parse_models_dev(raw / "models_dev" / "api.json", src("models_dev"))
        present["models_dev"] = set(facts)
        snap_sources["models_dev"] = {"as_of": as_of}

    # tau2
    if "tau2" in failed:
        reuse("tau2")
    else:
        s, as_of = parse.parse_tau2(raw / "tau2" / "submissions.json", src("tau2"))
        scores += s
        present["tau2"] = {x["model"] for x in s}
        snap_sources["tau2"] = {"as_of": as_of}

    # Steel
    if "steel" in failed:
        reuse("steel")
    else:
        s, as_of = parse.parse_steel(raw / "steel", src("steel"))
        scores += s
        present["steel"] = {x["model"] for x in s}
        snap_sources["steel"] = {"as_of": as_of}

    # ── validation: fail loudly, write nothing ────────────────────────────
    problems: list[str] = []
    for m in allow:
        for need in m.get("expect", []):
            if m["id"] not in present.get(need, set()):
                problems.append(f"{m['id']}: expected in {need} but missing (renamed upstream? fix models.yaml)")
    if len(facts) < MIN_MODELS_DEV:
        problems.append(f"models_dev: only {len(facts)} allowlisted models found (floor {MIN_MODELS_DEV})")
    for name, floor in MIN_SCORES.items():
        n = sum(1 for s in scores if s["source"] == name)
        if n < floor:
            problems.append(f"{name}: only {n} scores for allowlisted models (floor {floor})")
    for s in scores:
        if any(b in json.dumps(s).lower() for b in parse.BANNED_PROVENANCE):
            problems.append(f"banned provenance leaked into {s['board']} for {s['model']}")
        v = s["value"]
        if s["unit"] == "%" and not (0 <= v <= 100):
            problems.append(f"{s['board']} {s['model']}: {v}% out of range")
    for mid, f in facts.items():
        for k in ("price_in", "price_out"):
            if f.get(k) is not None and f[k] < 0:
                problems.append(f"{mid}: negative {k}")
    if problems:
        raise ValidationError("\n".join(problems))

    for name, meta in snap_sources.items():
        meta.update(SOURCES[name])
        meta["present"] = sorted(present.get(name, set()))

    models = {}
    for m in allow:
        models[m["id"]] = {
            "display": m["display"], "lab": m["lab"], "tier": m["tier"],
            "facts": facts.get(m["id"], {}),
        }

    scores.sort(key=lambda s: (s["board"], s["model"], s["variant"], s["value"]))
    return {"schema_version": 1, "sources": snap_sources, "models": models, "scores": scores}


def dumps(snapshot: dict) -> str:
    # One record per line keeps git deltas tiny and diffs reviewable.
    head = {k: v for k, v in snapshot.items() if k != "scores"}
    lines = json.dumps(head, indent=1, sort_keys=True, ensure_ascii=False)[:-2]
    body = ",\n  ".join(json.dumps(s, sort_keys=True, ensure_ascii=False) for s in snapshot["scores"])
    return f'{lines},\n "scores": [\n  {body}\n ]\n}}\n'
