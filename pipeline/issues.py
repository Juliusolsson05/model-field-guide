"""Upsert one GitHub issue per notice kind, never a new issue per night.

    uv run python -m pipeline.issues .nightly

Issues rather than PRs because a PR opened with GITHUB_TOKEN needs a repo
setting that is off by default and, since June 2026, its CI waits for manual
approval. An issue only needs `issues: write`, reaches every watcher, and the
human fix (edit models.yaml, write prose) is a normal PR anyway.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

KINDS = {
    "new-agent.md": ("new-agent", "New coding-agent setup on the leaderboard"),
    "stale-prose.md": ("stale-prose", "Model notes past their review date"),
}


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def main(directory: str) -> int:
    d = Path(directory)
    stamp = datetime.now(timezone.utc).date().isoformat()
    for fname, (label, title) in KINDS.items():
        body_file = d / fname
        if not body_file.exists():
            continue
        subprocess.run(["gh", "label", "create", label, "--force", "--color", "5319e7"], capture_output=True)
        open_ = json.loads(gh("issue", "list", "--label", label, "--state", "open", "--json", "number"))
        body = f"_Nightly run {stamp}_\n\n" + body_file.read_text()
        if open_ and label == "stale-prose":
            # The same stale list would otherwise be re-posted every night
            # until someone reviews it; one open issue is the reminder.
            continue
        if open_:
            gh("issue", "comment", str(open_[0]["number"]), "--body", body)
        else:
            gh("issue", "create", "--title", title, "--label", label, "--body", body)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ".nightly"))
