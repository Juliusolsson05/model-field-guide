# model-field-guide

A field guide to frontier AI models: **which model to use for which job**, kept
current every night. It is also an [Agent Skill](https://agentskills.io), so
Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Copilot and Agent Code can
load it and answer "which model should I use for X?" from dated tables instead
of out-of-date training data.

Two layers, never mixed:

- **Human notes** (`skills/model-field-guide/references/`): one file per model
  covering what it shines at, where it falls over, when to reach for it and when
  not to, plus `pick-by-job.md`. Written by hand. Every file carries `reviewed`
  and `review_by` dates.
- **Nightly tables** (`skills/model-field-guide/tables/`): generated from openly
  licensed sources (Epoch AI, LMArena, models.dev, tau2-bench, Steel). They cover
  overall, coding, agents, computer use, price and context, and a changelog.

## Install

**Claude Code**
```
/plugin marketplace add Juliusolsson05/model-field-guide
/plugin install model-field-guide@model-field-guide
```
Turn on auto-update for this marketplace in `/plugin`. Third-party marketplaces
don't auto-update by default. `plugin.json` has no `version` on purpose, so
every nightly commit counts as an update.

**Codex**
```
codex plugin marketplace add Juliusolsson05/model-field-guide
```

**Any runtime that reads `.agents/skills`** (Codex, Cursor, OpenCode, Gemini CLI, Copilot)
```
npx skills add Juliusolsson05/model-field-guide
# or
gh skill install Juliusolsson05/model-field-guide model-field-guide
# or
git clone https://github.com/Juliusolsson05/model-field-guide /tmp/mfg && cp -r /tmp/mfg/skills/model-field-guide ~/.agents/skills/
```

**Pin a dated snapshot** (freeze for production): every data commit is tagged
`snapshot-YYYY-MM-DD`.
```
/plugin marketplace add Juliusolsson05/model-field-guide@snapshot-2026-09-22
npx skills add Juliusolsson05/model-field-guide#snapshot-2026-09-22
```

Copied installs only update when you run an update command, so the skill checks
its own data age. If the tables are more than 7 days old, it fetches fresh ones
from this repo, or tells you how old they are.

## How the data works

```
epoch.ai zip ─┐
LMArena (HF) ─┤
models.dev ───┼─► pipeline/ ─► validate ─► data/snapshot.json ─► tables/*.md ─► commit + tag
tau2-bench ───┤      (allowlist + alias map: pipeline/models.yaml)
Steel ────────┘
```

- **Allowlist.** About 20 frontier models, listed on purpose in
  `pipeline/models.yaml`. No two sources name models the same way, so each
  model's id in every source is mapped by hand.
- **Fails loudly.** If a model we require disappears from a source (usually an
  upstream rename), or a source returns nothing, the run fails without writing
  anything. Yesterday's data stays, and a `nightly-failure` issue opens.
- **One flaky source doesn't blank the tables.** A source that fails to
  download keeps its previous rows and is marked STALE.
- **Nothing is invented.** A model with no score shows "not yet measured".
- **Effort levels are kept separate** (e.g. Astra `max` vs `high`), always with
  the upstream's own label.
- **Commit only on change.** Output is byte-deterministic, so a quiet night
  makes no commit.
- **Notes are never machine-written.** The nightly job never edits them. It
  opens issues when a new model gets data or when notes pass their `review_by`
  date.
- **No Artificial Analysis data.** Their terms forbid republishing it as tables
  (see `DATA-LICENSES.md`).

Run it locally:
```
uv sync
uv run python -m pipeline.nightly            # fetch + build + render
uv run python -m pipeline.nightly --offline  # rebuild from .cache/raw
uv run pytest
```

## Maintaining it

- **Lab release (about 20 minutes).**
  1. Add the model to `pipeline/models.yaml`, with its id in each source.
  2. Write `references/models/<id>.md` with `status: provisional` and
     `review_by` two weeks out.
  3. Update `pick-by-job.md` if the model changes a pick.
  4. Run `gh workflow run nightly` to refresh the data.
- **Daily (about 5 minutes).** Skim `tables/changelog.md`.
- **Issues** labelled `new-model`, `stale-prose` and `source-down` are the to-do
  list.

## Licence

Code and prose: MIT. Data: see `DATA-LICENSES.md`.
