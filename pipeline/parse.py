"""Turn each raw source into normalized records for the allowlisted models.

Every score becomes one flat dict:
    {model, source, board, variant, value, unit, kind, extra}
- model    our id from models.yaml
- board    which benchmark/leaderboard ("epoch.swe_bench_verified", ...)
- variant  the upstream's own label for the exact configuration measured,
           e.g. "GPT-6 Astra (max)" or "claude-opus-5-high". We keep the
           upstream label verbatim instead of inventing an effort taxonomy:
           effort levels are first-class and different sources spell them
           differently, and a label we made up could misattribute a score.
- kind     "independent" (the source ran it) or "vendor" (a lab's own claim)

Parsers never fetch and never read models.yaml themselves; they receive the
alias map. That keeps them pure functions over recorded bytes, which is what
the fixture tests exercise.
"""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path

# ── Epoch ─────────────────────────────────────────────────────────────────

# Only Epoch's OWN runs (files without the _external suffix) are plain CC BY.
# External files "retain their original licensing", so each one we use is
# listed here deliberately with its upstream licence noted in DATA-LICENSES.md.
EPOCH_BOARDS = {
    # file                               board id                    score column                   kind
    "gpqa_diamond.csv":                 ("epoch.gpqa_diamond",        "Best score (across scorers)", "independent"),
    "frontiermath_tiers_1_3_v2.csv":    ("epoch.frontiermath_t1_3",   "Best score (across scorers)", "independent"),
    "swe_bench_verified.csv":           ("epoch.swe_bench_verified",  "Best score (across scorers)", "independent"),
    "simpleqa_verified.csv":            ("epoch.simpleqa_verified",   "Best score (across scorers)", "independent"),
    "mirrorcode.csv":                   ("epoch.mirrorcode",          "Best score (across scorers)", "independent"),
    # External, Apache-2.0 upstream (Terminal-Bench 2.0 leaderboard via Epoch).
    "terminalbench_external.csv":       ("epoch.terminalbench_2",     "Accuracy mean",               "independent"),
    # External coding leaderboards Epoch mirrors (third-party sites with no
    # stated data licence; published here as attributed factual scores, see
    # DATA-LICENSES.md). They are what makes the coding table useful: Epoch's
    # own SWE-bench run covers few current frontier models.
    "deepswe_external.csv":             ("epoch.deepswe",             "Pass@1",                      "independent"),
    "frontierswe_external.csv":         ("epoch.frontierswe",         "Score",                       "independent"),
    "cursorbench_external.csv":         ("epoch.cursorbench",         "Score",                       "independent"),
    # External, OSWorld 2.0 official results (xlang); see DATA-LICENSES.md.
    "osworld_2_external.csv":           ("epoch.osworld_2",           "Binary accuracy",             "independent"),
}

# A row from an _external file whose provenance mentions any of these is
# dropped. Epoch mirrors some Artificial Analysis numbers (scicode_external has
# an "AA model slug" column); AA's terms forbid redistributing them as tables.
BANNED_PROVENANCE = ("artificialanalysis",)


def _csv_rows(z: zipfile.ZipFile, basename: str) -> list[dict]:
    name = next((n for n in z.namelist() if n.rsplit("/", 1)[-1] == basename), None)
    if name is None:
        raise ValueError(f"epoch zip is missing {basename}")
    return list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8"))))


def _tainted(row: dict) -> bool:
    return any(b in (v or "").lower() for v in row.values() for b in BANNED_PROVENANCE)


def parse_epoch(zip_path: Path, groups: dict[str, str]) -> tuple[list[dict], set[str], str]:
    """groups: {epoch model_group -> our id}.

    Returns (scores, groups_present_in_metadata, as_of).
    """
    with zipfile.ZipFile(zip_path) as z:
        # as_of = newest member timestamp inside the zip. Deterministic for the
        # same upload, unlike the HTTP Last-Modified or our own fetch time.
        as_of = max(datetime(*i.date_time) for i in z.infolist()).date().isoformat()

        meta = {r["model_version"]: r for r in _csv_rows(z, "model_metadata.csv") if r.get("model_version")}
        present = {r["model_group"] for r in meta.values() if r.get("model_group")}

        scores: list[dict] = []
        for r in _csv_rows(z, "eci_scores.csv"):
            mid = groups.get(r["Model"])
            if mid and r.get("eci"):
                scores.append(_score(mid, "epoch", "epoch.eci", r["Model"], float(r["eci"]), "index",
                                     "independent", {"ci_low": _f(r.get("eci_ci_low")), "ci_high": _f(r.get("eci_ci_high"))}))

        for fname, (board, col, kind) in EPOCH_BOARDS.items():
            external = fname.endswith("_external.csv")
            for r in _csv_rows(z, fname):
                if external and _tainted(r):
                    continue
                version = r.get("Model version", "")
                m = meta.get(version)
                if not m:
                    continue
                mid = groups.get(m["model_group"])
                raw = _f(r.get(col))
                if not mid or raw is None:
                    continue
                variant = m.get("display_name") or version
                extra: dict = {"version": version}
                if board == "epoch.terminalbench_2":
                    extra["agent"] = r.get("Agent", "")
                if board in ("epoch.deepswe", "epoch.frontierswe"):
                    extra["agent"] = r.get("Harness", "")
                if board == "epoch.osworld_2":
                    extra["partial"] = _pct(_f(r.get("Partial score")))
                    extra["step_budget"] = r.get("Step budget", "")
                scores.append(_score(mid, "epoch", board, variant, _pct(raw), "%", kind, extra))

    # Harness-based boards have one row per (model, agent harness). Keep the best
    # harness per exact model variant and name it; showing all harnesses would
    # turn the coding table into an agent-harness leaderboard.
    for b in ("epoch.terminalbench_2", "epoch.deepswe", "epoch.frontierswe"):
        scores = _best_per_variant(scores, b)
    return scores, present, as_of


# ── LMArena ───────────────────────────────────────────────────────────────

# Tokens that describe HOW a model was run, not WHICH model it is. Stripping
# them before comparing to a base name lets new effort variants match
# automatically, while "claude-opus-5-5-max" still cannot match
# "claude-opus-5" (the leftover token "5" is not in this set).
_VARIANT_TOKENS = {"low", "medium", "high", "xhigh", "max", "none", "minimal", "thinking", "codex", "harness"}


def lmarena_tokens(name: str) -> list[str]:
    s = name.lower().replace("(", " ").replace(")", " ").replace(",", " ")
    s = re.sub(r"[\s_]+", "-", s.strip())
    return [t for t in s.split("-") if t]


def lmarena_match(name: str, bases: list[str]) -> bool:
    # Strip variant tokens from BOTH sides: some model names contain them
    # ("qwen3.8-max", "mistral-medium-3.5"), and stripping only the upstream
    # name made those models unmatchable.
    core = lambda s: [t for t in lmarena_tokens(s) if t not in _VARIANT_TOKENS]  # noqa: E731
    return any(core(name) == core(b) for b in bases)


def parse_lmarena(raw_dir: Path, aliases: dict[str, list[str]]) -> tuple[list[dict], str]:
    """aliases: {our id -> [base names]}. Returns (scores, as_of)."""
    scores: list[dict] = []
    dates: list[str] = []
    for config in ("text", "webdev", "agent"):
        rows = json.loads((raw_dir / f"{config}.json").read_text())
        for r in rows:
            if r.get("category") != "overall":
                continue
            dates.append(r.get("leaderboard_publish_date") or "")
            for mid, bases in aliases.items():
                if lmarena_match(r["model_name"], bases):
                    if config == "agent":
                        value, unit = r.get("score"), "score"
                        extra = {"rank": r.get("rank"), "sessions": r.get("session_count")}
                    else:
                        value, unit = r.get("rating"), "elo"
                        extra = {"rank": r.get("rank"), "votes": r.get("vote_count"),
                                 "ci_low": r.get("rating_lower"), "ci_high": r.get("rating_upper")}
                    if value is not None:
                        scores.append(_score(mid, "lmarena", f"lmarena.{config}", r["model_name"],
                                             float(value), unit, "independent", extra))
                    break
    return scores, max(dates) if dates else ""


# ── models.dev ────────────────────────────────────────────────────────────


def parse_models_dev(api_json: Path, keys: dict[str, str]) -> tuple[dict[str, dict], str]:
    """keys: {our id -> "<provider>/<model>"}. Returns ({id: facts}, as_of)."""
    api = json.loads(api_json.read_text())
    facts: dict[str, dict] = {}
    dates: list[str] = []
    for mid, key in keys.items():
        provider, _, model = key.partition("/")
        m = (api.get(provider) or {}).get("models", {}).get(model)
        if not m:
            continue
        cost = m.get("cost") or {}
        limit = m.get("limit") or {}
        efforts: list[str] = []
        for opt in m.get("reasoning_options") or []:
            if opt.get("type") == "effort":
                efforts = list(opt.get("values") or [])
        facts[mid] = {
            "price_in": cost.get("input"),
            "price_out": cost.get("output"),
            "price_cache_read": cost.get("cache_read"),
            "price_in_long": (cost.get("context_over_200k") or {}).get("input"),
            "price_out_long": (cost.get("context_over_200k") or {}).get("output"),
            "context": limit.get("context"),
            "max_output": limit.get("output"),
            "efforts": efforts,
            "reasoning": bool(m.get("reasoning")),
            "open_weights": bool(m.get("open_weights")),
            "knowledge": m.get("knowledge"),
            "release_date": m.get("release_date"),
            "status": m.get("status"),
            "modalities_in": sorted((m.get("modalities") or {}).get("input") or []),
        }
        dates.append(m.get("last_updated") or "")
    return facts, max(dates) if dates else ""


# ── tau2-bench ────────────────────────────────────────────────────────────

TAU2_DOMAINS = ("airline", "retail", "telecom", "banking_knowledge")


def parse_tau2(submissions_json: Path, names: dict[str, list[str]]) -> tuple[list[dict], str]:
    subs = json.loads(submissions_json.read_text())
    by_name = {n: mid for mid, ns in names.items() for n in ns}
    scores: list[dict] = []
    dates: list[str] = []
    for sub_id, s in sorted(subs.items()):
        dates.append(s.get("submission_date") or "")
        mid = by_name.get(s.get("model_name", ""))
        if not mid:
            continue
        effort = s.get("reasoning_effort") or "default"
        for dom in TAU2_DOMAINS:
            res = (s.get("results") or {}).get(dom) or {}
            if res.get("pass_1") is None:
                continue
            scores.append(_score(mid, "tau2", f"tau2.{dom}", f"{s['model_name']} ({effort})",
                                 float(res["pass_1"]), "%", "independent" if s.get("submitting_organization") == "Sierra" else "vendor",
                                 {"submission": sub_id, "submitted_by": s.get("submitting_organization"),
                                  "date": s.get("submission_date")}))
    return scores, max(dates) if dates else ""


# ── Steel (computer use, mostly vendor-reported) ─────────────────────────


def steel_match(system_name: str, prefixes: list[str]) -> bool:
    # "Claude Opus 5 (Snorkel run)" matches "Claude Opus 5"; "Claude Opus 5.5"
    # must not, so the character after the prefix has to end the model name.
    for p in prefixes:
        if system_name == p or system_name.startswith(p + " "):
            return True
    return False


def parse_steel(raw_dir: Path, prefixes: dict[str, list[str]]) -> tuple[list[dict], str]:
    scores: list[dict] = []
    dates: list[str] = []
    for board in ("osworld", "osworld2"):
        data = json.loads((raw_dir / f"{board}.json").read_text())
        rows = data[board] if isinstance(data, dict) else data
        for r in rows:
            dates.append(str(r.get("reportedAt") or ""))
            for mid, ps in prefixes.items():
                if steel_match(r.get("systemName", ""), ps):
                    notes = r.get("notesShort") or ""
                    kind = "vendor" if "self-reported" in notes.lower() else "independent"
                    scores.append(_score(mid, "steel", f"steel.{board}", r["systemName"], float(r["scoreValue"]), "%",
                                         kind, {"source_url": r.get("sourceUrl"), "notes": notes,
                                                "reported": str(r.get("reportedAt") or "")}))
                    break
    return scores, max(dates) if dates else ""


# ── helpers ───────────────────────────────────────────────────────────────


def _f(v) -> float | None:
    try:
        return float(v) if v not in (None, "") else None
    except ValueError:
        return None


def _pct(v: float | None) -> float | None:
    return None if v is None else round(v * 100, 1)


def _score(model, source, board, variant, value, unit, kind, extra) -> dict:
    return {"model": model, "source": source, "board": board, "variant": variant,
            "value": round(value, 1) if isinstance(value, float) and unit != "score" else round(value, 4),
            "unit": unit, "kind": kind, "extra": extra}


def _best_per_variant(scores: list[dict], board: str) -> list[dict]:
    keep: dict[tuple, dict] = {}
    rest = []
    for s in scores:
        if s["board"] != board:
            rest.append(s)
            continue
        k = (s["model"], s["variant"])
        if k not in keep or s["value"] > keep[k]["value"]:
            keep[k] = s
    return rest + list(keep.values())
