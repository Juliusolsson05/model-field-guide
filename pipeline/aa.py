"""Fetch and parse the Artificial Analysis Coding Agent leaderboard.

Source: https://artificialanalysis.ai/agents/coding-agents
Each row is an agent product running a specific model at a specific effort
(e.g. "Codex - GPT-6 Astra (max)"), scored on the Coding Agent Index (DeepSWE,
Terminal-Bench 4.0, SWE-Atlas QnA) with cost, wall time and refusal rate.

The AA API has no endpoint for this page, so we read the data the page itself
embeds (Next.js flight payload), once a night. Note that AA's website terms
restrict automated scraping and republication; the maintainer chose to run
this openly with attribution (see README). If AA ships an API endpoint for
coding agents, switch to it (header `x-api-key`, base /api/v2), and if AA asks
us to stop, stop.

Why parse the flight payload instead of the rendered HTML table: the page
renders charts client-side, so the numbers are only in the payload. We locate
row objects by their shape ({"id": <32 hex>, "isDefault": ...} with an
indexScore) rather than by a path into the React tree, because the tree shape
changes with every frontend deploy while the row objects have stayed stable.
"""

from __future__ import annotations

import json
import re
import time
import urllib.request

URL = "https://artificialanalysis.ai/agents/coding-agents"
UA = "model-field-guide nightly (+https://github.com/Juliusolsson05/model-field-guide; one request per day)"

# The three evals inside Coding Agent Index v1.5, with our column labels.
EVALS = {
    "deep-swe-v1.1": "DeepSWE",
    "terminal-bench-v4": "Terminal-Bench 4",
    "swe-atlas-qna": "SWE-Atlas QnA",
}

# The page has always carried ~20 rows. Fewer than this means the page or
# its payload format changed, and publishing a near-empty table would read as
# "these are the only agents" when it really means "our parser broke".
MIN_ROWS = 10


class ParseError(Exception):
    pass


def fetch(timeout: int = 60, tries: int = 3) -> str:
    last: Exception | None = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8")
        except Exception as e:  # noqa: BLE001 - re-raised below
            last = e
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"fetch failed after {tries} tries: {last}")


def _payload(html: str) -> str:
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.S)
    if not chunks:
        raise ParseError("no Next.js flight payload found; the page format changed")
    return "".join(json.loads(f'"{c}"') for c in chunks)


def parse(html: str) -> dict:
    """Return {"as_of", "index_version", "rows": [...]}, sorted by index desc."""
    s = _payload(html)
    dec = json.JSONDecoder()
    raw: dict[str, dict] = {}
    for m in re.finditer(r'\{"id":"[0-9a-f]{32}","isDefault"', s):
        try:
            obj, _ = dec.raw_decode(s, m.start())
        except ValueError:
            continue
        if isinstance(obj.get("indexScore"), (int, float)):
            raw[obj["id"]] = obj

    rows = []
    materialized: list[str] = []
    for o in raw.values():
        disp = _obj(o.get("display"))
        creator = _obj(disp.get("creator"))
        evals = {}
        for e in o.get("evals") or []:
            key = e.get("datasetIndexName")
            if key in EVALS and (e.get("mean") or {}).get("reward") is not None:
                evals[key] = round(e["mean"]["reward"] * 100, 1)
            rh = e.get("rewardHacking") or {}
            if rh.get("materializedAt"):
                materialized.append(rh["materializedAt"][:10])
        mean = o.get("mean") or {}
        label = _clean_label(o.get("displayLabel") or "")
        agent = disp.get("agent") or o.get("agentName") or ""
        # The label ("Opencode - GLM-5.3 (max)") carries the effort level that
        # display.model sometimes drops ("GLM-5.3"), so derive the model from it.
        model = label.split(" - ", 1)[1] if label.startswith(agent + " - ") else _clean_label(disp.get("model") or "")
        rows.append({
            "id": o["id"],
            "label": label,
            "agent": agent,
            "model": model,
            "agent_maker": creator.get("agent") or "",
            "model_maker": creator.get("model") or "",
            "index": round(o["indexScore"] * 100, 1),
            "evals": evals,
            "cost_usd": _r(mean.get("costUsd"), 2),
            "minutes": _r((mean.get("agentWallTimeSec") or 0) / 60, 1) if mean.get("agentWallTimeSec") else None,
            "steps": _r(mean.get("steps"), 0),
            "refusal_pct": _r(((o.get("safety") or {}).get("rate") or 0) * 100, 1),
            "default_config": bool(o.get("isDefault")),
            "unavailable": bool(o.get("isUnavailable")),
        })

    if len(rows) < MIN_ROWS:
        raise ParseError(f"only {len(rows)} coding-agent rows parsed (floor {MIN_ROWS}); the page format changed")
    for r in rows:
        if not (0 <= r["index"] <= 100) or not r["label"]:
            raise ParseError(f"implausible row: {r}")

    version = re.search(r"Coding Agent Index (v[\d.]+)", s)
    rows.sort(key=lambda r: (-r["index"], r["label"]))
    return {
        # No date is shown on the page; the newest audit timestamp inside the
        # payload is the best available "data as of".
        "as_of": max(materialized) if materialized else "",
        "index_version": version.group(1) if version else "",
        "rows": rows,
    }


def _obj(v) -> dict:
    # Next.js serializes a missing object as the string "$undefined", so any
    # nested object in the payload may be a string. Seen live on 2026-09-23
    # for the Devin Fusion rows' `display.creator`.
    return v if isinstance(v, dict) else {}


def _clean_label(s: str) -> str:
    # Some labels carry a raw config dict: "GLM-5.3 ({'reasoning_effort': 'max'})".
    s = re.sub(r"\(\{'reasoning_effort': '(\w+)'\}\)", r"(\1)", s)
    s = re.sub(r"\((\w+)\) \(\1\)", r"(\1)", s)  # "(max) (max)" after the rewrite
    return re.sub(r"\s+", " ", s).strip()


def _r(v, nd):
    if v is None:
        return None
    return round(float(v), nd) if nd else int(round(float(v)))
