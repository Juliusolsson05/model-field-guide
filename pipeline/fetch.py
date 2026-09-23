"""Download every upstream source into a raw directory, byte for byte.

Fetching is kept separate from parsing so that tests (and a human debugging a
bad night) can run the whole pipeline against a recorded raw directory with no
network. `tests/fixtures/raw/` has exactly the layout this module writes.

Every source here was chosen because its licence allows public redistribution
of the numbers (see DATA-LICENSES.md). Do NOT add Artificial Analysis, ARC
Prize, llm-stats, Scale SEAL or OpenRouter's /models payload here: their terms
forbid republishing tables of their data, and one bad fetcher makes the whole
public repo non-compliant.
"""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = "model-field-guide nightly (+https://github.com/Juliusolsson05/model-field-guide)"

EPOCH_ZIP = "https://epoch.ai/data/benchmark_data.zip"
MODELS_DEV = "https://models.dev/api.json"
LMARENA_ROWS = "https://datasets-server.huggingface.co/rows"
LMARENA_DATASET = "lmarena-ai/leaderboard-dataset"
LMARENA_CONFIGS = ("text", "webdev", "agent")
TAU2_BASE = "https://raw.githubusercontent.com/sierra-research/tau2-bench/main/web/leaderboard/public/submissions"
STEEL_BASE = "https://raw.githubusercontent.com/steel-dev/leaderboard/main/src/data"
STEEL_BOARDS = ("osworld", "osworld2")


def _get(url: str, *, timeout: int = 60, tries: int = 3) -> bytes:
    # Upstreams (HF datasets-server especially) return transient 5xx/timeouts.
    # Three tries with backoff turns a flaky night into a green one without
    # hiding a real outage: the third failure still raises and fails the run.
    last: Exception | None = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 - re-raised below
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"fetch failed after {tries} tries: {url}: {last}")


def fetch_epoch(raw: Path) -> None:
    (raw / "epoch").mkdir(parents=True, exist_ok=True)
    (raw / "epoch" / "benchmark_data.zip").write_bytes(_get(EPOCH_ZIP, timeout=120))


def fetch_models_dev(raw: Path) -> None:
    (raw / "models_dev").mkdir(parents=True, exist_ok=True)
    (raw / "models_dev" / "api.json").write_bytes(_get(MODELS_DEV))


def fetch_lmarena(raw: Path) -> None:
    # The `latest` split holds every category (text alone is ~10k rows), but the
    # rows come ordered with category "overall" first. We page until the first
    # non-overall row instead of downloading everything; the HF /filter
    # endpoint would be neater but routinely took >2 minutes when tested.
    out = raw / "lmarena"
    out.mkdir(parents=True, exist_ok=True)
    for config in LMARENA_CONFIGS:
        rows: list[dict] = []
        offset = 0
        while True:
            q = urllib.parse.urlencode(
                {"dataset": LMARENA_DATASET, "config": config, "split": "latest", "offset": offset, "length": 100}
            )
            page = json.loads(_get(f"{LMARENA_ROWS}?{q}"))
            batch = [r["row"] for r in page.get("rows", [])]
            overall = [r for r in batch if r.get("category") == "overall"]
            rows.extend(overall)
            if len(overall) < len(batch) or len(batch) < 100:
                break
            offset += 100
            if offset > 5000:  # guard against an upstream reorder looping forever
                raise RuntimeError(f"lmarena {config}: overall rows never ended")
        (out / f"{config}.json").write_text(json.dumps(rows, indent=1, sort_keys=True))


def fetch_tau2(raw: Path) -> None:
    out = raw / "tau2"
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(_get(f"{TAU2_BASE}/manifest.json"))
    subs = {}
    for name in manifest["submissions"]:
        subs[name] = json.loads(_get(f"{TAU2_BASE}/{urllib.parse.quote(name)}/submission.json"))
    (out / "submissions.json").write_text(json.dumps(subs, indent=1, sort_keys=True))


def fetch_steel(raw: Path) -> None:
    out = raw / "steel"
    out.mkdir(parents=True, exist_ok=True)
    for board in STEEL_BOARDS:
        (out / f"{board}.json").write_bytes(_get(f"{STEEL_BASE}/{board}.json"))


FETCHERS = {
    "epoch": fetch_epoch,
    "models_dev": fetch_models_dev,
    "lmarena": fetch_lmarena,
    "tau2": fetch_tau2,
    "steel": fetch_steel,
}


def fetch_all(raw: Path) -> dict[str, str]:
    """Fetch every source. Returns {source: error} for sources that failed.

    A failed source is not fatal here: nightly.py falls back to yesterday's
    rows for that source (one flaky upstream must not blank the tables) and
    only fails the run when a source has been down for several days.
    """
    errors: dict[str, str] = {}
    for name, fn in FETCHERS.items():
        try:
            fn(raw)
        except Exception as e:  # noqa: BLE001
            errors[name] = str(e)
    return errors
