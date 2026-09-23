# model-field-guide

Which AI model and coding agent to use, kept current every night. It's an
[Agent Skill](https://agentskills.io), so Claude Code, Codex, Cursor, OpenCode,
Gemini CLI, Copilot and Agent Code can load it and answer "which model should
I use for X?" from a dated table instead of out-of-date training data.

Two layers:

- **The leaderboard** (`skills/model-field-guide/tables/coding-agents.md`) is
  refreshed nightly from the
  [Artificial Analysis Coding Agent Index](https://artificialanalysis.ai/agents/coding-agents).
  Each row is an agent product (Claude Code, Codex, Devin, Grok Build,
  Opencode, Kimi Code…) running one model at one effort level. Columns: the
  index, DeepSWE / Terminal-Bench 4 / SWE-Atlas QnA, cost and time per task,
  refusal rate. Two derived views: best score for the money, and fastest.
- **Human notes** (`skills/model-field-guide/references/`): one file per model
  covering what it shines at, where it falls over, and when to use it or not,
  plus `pick-by-job.md` for jobs the leaderboard doesn't measure (computer use,
  writing, cheap bulk work). Each file carries `reviewed` / `review_by` dates.
  The nightly job never edits them.

## Install

**Claude Code**
```
/plugin marketplace add Juliusolsson05/model-field-guide
/plugin install model-field-guide@model-field-guide
```
Turn on auto-update for this marketplace in `/plugin`. `plugin.json` has no
`version`, so every nightly data commit counts as an update.

**Codex**
```
codex plugin marketplace add Juliusolsson05/model-field-guide
```

**Anything that reads `.agents/skills`** (Codex, Cursor, OpenCode, Gemini CLI, Copilot)
```
npx skills add Juliusolsson05/model-field-guide
# or: gh skill install Juliusolsson05/model-field-guide model-field-guide
```

**Pin a date:** every data commit is tagged `snapshot-YYYY-MM-DD`
(`/plugin marketplace add Juliusolsson05/model-field-guide@snapshot-2026-09-22`).

Copied installs only update when you run an update command. To cover that, the
skill checks its own data age: when the table is more than 7 days old, it
fetches the latest one from this repo.

## How it works

`pipeline/aa.py` reads the leaderboard data embedded in the page, once a night.
Artificial Analysis's API has no endpoint for coding agents.

It fails loudly instead of publishing a broken table. If the page format
changes or fewer than 10 rows parse, the run fails without writing anything,
yesterday's table stays, and a `nightly-failure` issue opens.

Output is byte-deterministic, so a night with no changes makes no commit.
`tables/changelog.md` lists what moved: new setups, index moves of 1 point or
more, cost changes, methodology version changes. A new setup also opens a
`new-agent` issue as a prompt to write notes.

```
uv sync
uv run python -m pipeline.nightly                       # live
uv run python -m pipeline.nightly --html saved.html     # from a saved page
uv run pytest                                           # tests run on a real recorded page
```

## About the data

All measurements in the table are by
[Artificial Analysis](https://artificialanalysis.ai), and all credit for them
is theirs. This is a small, non-commercial, open-source mirror of one public
page, made so coding agents can read it.

Artificial Analysis's website terms restrict automated collection and
republication. If Artificial Analysis asks, this mirror comes down, or moves to
their API if they add a coding-agents endpoint. The notes and code are MIT.
