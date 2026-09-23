"""Nightly entry point: fetch -> build+validate -> write -> notices.

    uv run python -m pipeline.nightly                 # full run (network)
    uv run python -m pipeline.nightly --offline       # rebuild from .cache/raw
    uv run python -m pipeline.nightly --raw tests/fixtures/raw --offline

Order matters: EVERYTHING is parsed and validated before ANY file is written.
A failed validation exits non-zero and leaves yesterday's committed data
untouched, so the workflow commits nothing and opens a failure issue.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from . import build, diff, fetch, prose, render

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "model-field-guide"
TABLES = SKILL / "tables"
MODELS_DIR = SKILL / "references" / "models"
SNAPSHOT = ROOT / "data" / "snapshot.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=ROOT / ".cache" / "raw")
    ap.add_argument("--offline", action="store_true", help="do not fetch; build from --raw as-is")
    ap.add_argument("--today", type=date.fromisoformat, default=datetime.now(timezone.utc).date())
    ap.add_argument("--issues-dir", type=Path, default=ROOT / ".nightly",
                    help="markdown bodies for GitHub issues (git-ignored)")
    args = ap.parse_args(argv)

    allow = build.load_allowlist()
    prev = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else None

    failed: dict[str, str] = {}
    if not args.offline:
        args.raw.mkdir(parents=True, exist_ok=True)
        failed = fetch.fetch_all(args.raw)
        for name, err in failed.items():
            print(f"::warning::{name} fetch failed: {err}", file=sys.stderr)

    try:
        snap = build.build(args.raw, allow, prev, set(failed))
        notes, problems = prose.load_all(MODELS_DIR, [m["id"] for m in allow])
        if problems:
            raise build.ValidationError("\n".join(problems))
    except build.ValidationError as e:
        for line in str(e).splitlines():
            print(f"::error::{line}", file=sys.stderr)
        return 1

    # ── write (only after everything validated) ──────────────────────────
    new_text = build.dumps(snap)
    changed = not SNAPSHOT.exists() or SNAPSHOT.read_text() != new_text
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_text(new_text)
    TABLES.mkdir(parents=True, exist_ok=True)
    for name, text in render.render_all(snap).items():
        (TABLES / name).write_text(text)
    (MODELS_DIR / "_index.md").write_text(prose.render_index(snap, notes, args.today))

    lines, notices = diff.diff(prev, snap) if changed else ([], [])
    cl = TABLES / "changelog.md"
    if changed or not cl.exists():
        cl.write_text(diff.update_changelog(cl.read_text() if cl.exists() else "", args.today.isoformat(), lines))

    # ── notices for humans (GitHub issues) ───────────────────────────────
    args.issues_dir.mkdir(parents=True, exist_ok=True)
    for f in args.issues_dir.glob("*.md"):
        f.unlink()
    if notices:
        (args.issues_dir / "new-model.md").write_text(
            "The nightly data picked up scores for a model for the first time.\n\n" + "\n".join(f"- {n}" for n in notices) +
            "\n\nIf this is a launch: add or update the prose file, keep `status: provisional`, and set `review_by` two weeks out.\n")
    st = prose.stale(notes, args.today)
    if st:
        (args.issues_dir / "stale-prose.md").write_text(
            "These prose files are past their `review_by` date. Re-read the evidence, update the notes, "
            "bump `reviewed` and `review_by`.\n\n" + "\n".join(f"- references/models/{m}.md (review_by {notes[m]['review_by']})" for m in st) + "\n")
    if failed:
        (args.issues_dir / "source-down.md").write_text(
            "One or more sources failed to download. Tables keep the previous data for these sources and are marked STALE.\n\n" +
            "\n".join(f"- {k}: {v}" for k, v in failed.items()) + "\n")

    print(f"snapshot {'changed' if changed else 'unchanged'}; {len(snap['scores'])} scores; "
          f"{len(lines)} changelog lines; {len(st)} stale prose files; {len(failed)} failed sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
