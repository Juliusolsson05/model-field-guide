"""Trigger eval for Claude Code: does the skill get invoked for each query?

    uv run python evals/run_triggers.py [--runs 3] [--model sonnet] [--jobs 8]

Loads this repo as a plugin (--plugin-dir), runs every query headless in
parallel, and counts a trigger only when the transcript contains a real Skill
tool_use naming model-field-guide (the repo path also contains that string,
so grepping raw output over-counts). Method from agentskills.io: a
should-trigger query passes at rate >= 0.5, a should-not query below 0.5.
Costs real tokens: queries x runs headless sessions, each capped at $0.50.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def triggered(query: str, model: str, timeout: int = 240) -> bool:
    """Stream the session and stop at the first Skill call naming this skill.

    Reading stream-json live and killing the process on the first decisive
    event keeps a run from hanging on a long answer: the question is only
    whether the skill fired, not what the agent went on to say. A session
    that times out without a Skill call counts as not triggered.
    """
    proc = subprocess.Popen(
        ["claude", "-p", query, "--model", model, "--plugin-dir", str(ROOT),
         "--output-format", "stream-json", "--verbose", "--max-budget-usd", "0.5",
         "--disallowedTools", "Bash,Edit,Write"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, cwd=ROOT,
    )
    timer = threading.Timer(timeout, proc.kill)
    timer.start()
    try:
        for line in proc.stdout:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            for c in (d.get("message") or {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Skill" \
                        and "model-field-guide" in json.dumps(c.get("input")):
                    return True
            if d.get("type") == "result":
                return False
        return False
    finally:
        timer.cancel()
        proc.kill()
        proc.wait()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()

    spec = json.loads((ROOT / "evals" / "triggers.json").read_text())
    cases = [(q, True) for q in spec["should_trigger"]] + [(q, False) for q in spec["should_not_trigger"]]
    work = [(q, want) for q, want in cases for _ in range(args.runs)]
    with ThreadPoolExecutor(args.jobs) as ex:
        hits = list(ex.map(lambda qw: triggered(qw[0], args.model), work))

    passed = 0
    for i, (q, want) in enumerate(cases):
        h = hits[i * args.runs:(i + 1) * args.runs]
        rate = sum(h) / args.runs
        ok = (rate >= 0.5) if want else (rate < 0.5)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  want={'Y' if want else 'N'} rate={rate:.2f}  {q}")
    tp = sum(1 for i, (_, w) in enumerate(cases) if w and sum(hits[i*args.runs:(i+1)*args.runs]) / args.runs >= 0.5)
    fp = sum(1 for i, (_, w) in enumerate(cases) if not w and sum(hits[i*args.runs:(i+1)*args.runs]) / args.runs >= 0.5)
    print(f"passed {passed}/{len(cases)} (should-trigger {tp}/{sum(w for _, w in cases)}, false triggers {fp}) "
          f"model={args.model} runs={args.runs}")


if __name__ == "__main__":
    main()
