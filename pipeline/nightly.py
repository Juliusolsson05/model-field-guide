"""Nightly entry point: fetch -> parse+validate -> write -> notices.

    uv run python -m pipeline.nightly                         # live
    uv run python -m pipeline.nightly --html page.html[.gz]   # from a saved page

Everything is parsed and validated before any file is written. A parse
failure exits non-zero and leaves the committed table untouched, so the
workflow commits nothing and opens a failure issue.
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from . import aa, diff, prose, render

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "model-field-guide"
TABLES = SKILL / "tables"
MODELS_DIR = SKILL / "references" / "models"
SNAPSHOT = ROOT / "data" / "coding-agents.json"


def dumps(data: dict) -> str:
    head = json.dumps({k: v for k, v in data.items() if k != "rows"}, sort_keys=True)[:-1]
    body = ",\n  ".join(json.dumps(r, sort_keys=True, ensure_ascii=False) for r in data["rows"])
    return f'{head}, "rows": [\n  {body}\n]}}\n'


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", type=Path, help="parse a saved page instead of fetching")
    ap.add_argument("--today", type=date.fromisoformat, default=datetime.now(timezone.utc).date())
    ap.add_argument("--issues-dir", type=Path, default=ROOT / ".nightly")
    args = ap.parse_args(argv)

    try:
        if args.html:
            raw = args.html.read_bytes()
            html = (gzip.decompress(raw) if args.html.suffix == ".gz" else raw).decode("utf-8")
        else:
            html = aa.fetch()
        data = aa.parse(html)
        notes, problems = prose.load_dir(MODELS_DIR)
        if problems:
            raise aa.ParseError("\n".join(problems))
    except Exception as e:  # noqa: BLE001 - any failure must fail the run loudly
        for line in str(e).splitlines():
            print(f"::error::{line}", file=sys.stderr)
        return 1

    prev = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else None
    text = dumps(data)
    changed = not SNAPSHOT.exists() or SNAPSHOT.read_text() != text
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_text(text)
    TABLES.mkdir(parents=True, exist_ok=True)
    (TABLES / "coding-agents.md").write_text(render.render_table(data))
    (MODELS_DIR / "_index.md").write_text(prose.render_index(notes, args.today))

    lines, notices = diff.diff(prev, data) if changed else ([], [])
    cl = TABLES / "changelog.md"
    if changed or not cl.exists():
        cl.write_text(diff.update_changelog(cl.read_text() if cl.exists() else "", args.today.isoformat(), lines))

    args.issues_dir.mkdir(parents=True, exist_ok=True)
    for f in args.issues_dir.glob("*.md"):
        f.unlink()
    if notices:
        (args.issues_dir / "new-agent.md").write_text("\n".join(f"- {n}" for n in notices) + "\n")
    stale = prose.stale(notes, args.today)
    if stale:
        (args.issues_dir / "stale-prose.md").write_text(
            "These notes are past their `review_by` date:\n\n" +
            "\n".join(f"- references/models/{m}.md (review_by {notes[m]['review_by']})" for m in stale) + "\n")

    print(f"{'changed' if changed else 'unchanged'}; {len(data['rows'])} rows; as of {data['as_of']}; "
          f"{len(lines)} changelog lines; {len(stale)} stale notes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
