---
name: model-field-guide
description: >-
  Which AI model and coding agent to use, with a nightly-updated coding-agent
  leaderboard (Artificial Analysis Coding Agent Index: Claude Code, Codex,
  Devin, Grok Build, Opencode, Kimi Code; running Claude, GPT, Grok, GLM, Kimi,
  Qwen, DeepSeek, Gemini, Muse models) plus dated human notes per model. Use
  whenever the user asks which model, LLM, coding agent or provider to use;
  compares models (e.g. "Opus vs Fable", "is Grok better than Sol"); asks for
  the current leaderboard, benchmark scores, cost or speed per task; wants
  cheap or open-weights options; or is choosing models for subagents or
  parallel workers. Your training data is out of date here, since models ship
  weekly, so read this skill instead of answering from memory.
license: MIT
compatibility: Needs file read access. Optional network access to refresh tables older than 7 days.
metadata:
  repo: https://github.com/Juliusolsson05/model-field-guide
---

# Model field guide

All paths below are relative to this SKILL.md's directory.

Two layers, never mixed:
- `tables/coding-agents.md` is **measurement**: the Artificial Analysis coding-agent leaderboard, refreshed nightly. Each row is an agent running one model at one effort level. Never edit it and never invent numbers that are not in it.
- `references/` is **human judgment**: dated notes per model (`references/models/<id>.md`) and `references/pick-by-job.md`.

## 1. Check freshness

Read the "Data as of" line at the top of `tables/coding-agents.md`.
- If it is more than 7 days old and you have network access, fetch
  `https://raw.githubusercontent.com/Juliusolsson05/model-field-guide/main/skills/model-field-guide/tables/coding-agents.md`
  and use that copy. Say that you refreshed it.
- Otherwise tell the user how old the data is.

## 2. Classify the job

coding (big repo, migration, review, terminal/devops) · hardest reasoning · computer or browser use · writing · cheap bulk / subagents · open weights · frontend · many parallel agents · "just give me the leaderboard". A request can combine several jobs; answer each part.

## 3. Read `references/pick-by-job.md` for that job

It gives first / value / cheap picks, what to avoid, and the effort level to use.

## 4. For coding questions, read `tables/coding-agents.md`

Quote setups, not bare models ("Codex with GPT-6 Sol at max: index 56.7, $2.99 and 22 min per task"). Use the column that matches the job: Terminal-Bench for terminal/devops work, DeepSWE for repo edits, SWE-Atlas QnA for questions about a codebase. The "Best score for the money" and "Fastest" sections answer the cost and speed questions. What each column means: `references/sources.md`.

For non-coding jobs there is no measured table. Say that the answer is judgment.

## 5. Read the notes for the 2 to 4 candidate models

`references/models/<id>.md` (list: `references/models/_index.md`). If a file is `provisional` or STALE, say its notes are early or overdue for review.

## 6. Answer

- Lead with the recommendation and the reason, in plain language.
- Back it with a few table rows (not the whole table), naming the agent, model and effort level.
- Give the data-as-of date and the source: "Artificial Analysis Coding Agent Index v1.5, data as of ...".
- If the notes and the table disagree, show both.

## Rules

- Never invent a score, price or ranking. If a setup is not in the table, say it has not been measured.
- "Just give me the leaderboard": quote `tables/coding-agents.md`. Do not rank from memory.
- A model with no row in the table and no notes file is not covered. Say so.
- Never compare across effort levels or agents without saying so.
