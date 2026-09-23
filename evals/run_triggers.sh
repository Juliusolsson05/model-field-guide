#!/usr/bin/env bash
# Trigger eval for Claude Code: does the skill get invoked for each query?
#   evals/run_triggers.sh [runs=3] [model=sonnet]
# Loads this repo as a plugin with --plugin-dir, runs each query headless, and
# counts a trigger when the transcript contains a Skill tool call for
# model-field-guide. Costs real tokens: 20 queries x runs.
set -euo pipefail
cd "$(dirname "$0")/.."
RUNS="${1:-3}"; MODEL="${2:-sonnet}"
jq -r '.should_trigger[] | "Y\t" + .' evals/triggers.json > /tmp/mfg-q.tsv
jq -r '.should_not_trigger[] | "N\t" + .' evals/triggers.json >> /tmp/mfg-q.tsv
pass=0; total=0
while IFS=$'\t' read -r want q; do
  hits=0
  for _ in $(seq "$RUNS"); do
    out=$(claude -p "$q" --model "$MODEL" --plugin-dir . --output-format stream-json --verbose --max-budget-usd 0.5 \
            --disallowedTools "Bash,Edit,Write" 2>/dev/null || true)
    # Count only a real Skill tool_use whose input names this skill; the repo
    # path also contains "model-field-guide", so a plain grep over-counts.
    if python3 -c 'import json,sys
for l in sys.stdin:
    try: d=json.loads(l)
    except Exception: continue
    for c in (d.get("message") or {}).get("content") or []:
        if isinstance(c,dict) and c.get("type")=="tool_use" and c.get("name")=="Skill" and "model-field-guide" in json.dumps(c.get("input")):
            sys.exit(0)
sys.exit(1)' <<<"$out"; then hits=$((hits+1)); fi
  done
  rate=$(awk "BEGIN{print $hits/$RUNS}")
  ok=$(awk "BEGIN{ if ((\"$want\"==\"Y\" && $rate>=0.5) || (\"$want\"==\"N\" && $rate<0.5)) print 1; else print 0 }")
  pass=$((pass+ok)); total=$((total+1))
  printf '%s  want=%s rate=%s  %s\n' "$([ "$ok" = 1 ] && echo PASS || echo FAIL)" "$want" "$rate" "$q"
done < /tmp/mfg-q.tsv
echo "passed $pass/$total"
