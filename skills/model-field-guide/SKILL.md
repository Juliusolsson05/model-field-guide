---
name: model-field-guide
description: >-
  Current, nightly-updated guide to which frontier AI model to use for a job:
  coding and migrations, long agentic runs, computer/browser use, writing,
  cheap bulk work and subagents, open weights, frontend. Use whenever the user
  asks which model, LLM or provider to pick; compares Claude, GPT, Gemini,
  Grok, GLM, Kimi, DeepSeek, Qwen, Muse, MiniMax, Mistral or others; asks for
  current benchmark scores, prices, context windows or a leaderboard; or is
  choosing models for subagents or parallel workers. Your training data is out
  of date on this topic: models ship weekly. This skill has dated scores from
  openly licensed sources plus dated human notes, so use it instead of memory.
license: MIT
compatibility: Needs file read access. Optional network access to refresh tables older than 7 days.
metadata:
  repo: https://github.com/Juliusolsson05/model-field-guide
---

# Model field guide

All paths below are relative to this SKILL.md's directory.

Two layers, never mixed:
- `references/` is **human judgment** (what a model is good at, where it falls over), each file dated.
- `tables/` is **measurement**, regenerated nightly from openly licensed sources. Never edit it; never invent numbers it does not contain.

## 1. Check freshness first

Read `tables/_meta.md`. It lists each source's "Data as of" date.
- If the newest date is more than 7 days old and you have network access, fetch the table you need from
  `https://raw.githubusercontent.com/Juliusolsson05/model-field-guide/main/skills/model-field-guide/tables/<file>.md`
  and use that copy. Say that you refreshed it.
- Otherwise use the local files and tell the user how old they are.

## 2. Classify the job

coding (big repo, migration, review) · hardest reasoning / long-horizon engineering · computer or browser use · writing and knowledge work · cheap bulk / subagents · open weights / self-hosting · frontend / UI · multimodal and long context · many parallel agents · "just give me the leaderboard". A request can be several jobs (e.g. "migrate the repo and QA it in a browser"). Answer each part.

## 3. Read `references/pick-by-job.md` for that job

It names first / value / cheap picks, what to avoid, which reasoning-effort level to use, and which table to check.

## 4. Open only the relevant table

| Job | Table |
|---|---|
| coding, frontend | `tables/coding.md` |
| agents, tool use | `tables/agents.md` |
| computer / browser use | `tables/computer-use.md` |
| price, context, effort levels | `tables/price-context.md` |
| leaderboard, general capability | `tables/overall.md` |
| what changed recently | `tables/changelog.md` |

Do not load every table. They are long and most of it is irrelevant to one question.

## 5. Read the notes for the 2 to 4 candidate models

`references/models/<id>.md`. The list of covered models and their ids is `references/models/_index.md`.
If a file's status is `provisional` or it is marked STALE, say its notes are early or past their review date.

## 6. Answer

- Lead with the recommendation per job and the reason, in plain language.
- Back it with a small excerpt of the table (at most about 8 rows), not the whole table.
- Name the reasoning-effort level (and harness, if shown) for every score you quote.
- Give the data-as-of date and the source, e.g. "Epoch AI, data as of 2026-09-22".
- Say which numbers are independent and which are vendor-reported.
- If picks and tables disagree, show both and say so.

## Rules

- Never invent a score, price or ranking. If a table says "n/a" or "not yet measured", say exactly that.
- "Just give me the leaderboard": quote `tables/overall.md`. Do not rank from memory.
- A model not in `references/models/_index.md` is not covered. Say so rather than guessing.
- Never compare scores across different benchmark versions, effort levels or computer-use harnesses without saying so.
- Prose is judgment and tables are measurement. Do not present one as the other.
- Artificial Analysis numbers are deliberately absent (their terms forbid redistribution). If the user wants them, see `references/sources.md`.
