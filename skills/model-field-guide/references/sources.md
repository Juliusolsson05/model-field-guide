# Sources: what the numbers mean

## The one measured table: Artificial Analysis Coding Agent Index

`tables/coding-agents.md` mirrors the [Artificial Analysis coding-agent leaderboard](https://artificialanalysis.ai/agents/coding-agents), refreshed nightly.

- **What a row is:** an agent product (Claude Code, Codex, Devin, Grok Build, Opencode, Kimi Code…) running one model at one effort level. The same model scores differently in a different harness, so rank setups, not models.
- **Index (v1.5):** the average pass rate over three evals, each weighted one third:
  - **DeepSWE v1.1** (113 real software-engineering tasks)
  - **Terminal-Bench 4.0** (66 terminal workflow tasks)
  - **SWE-Atlas QnA** (124 technical Q&A tasks about codebases)
- **Cost / task and time / task** are measured averages from AA's runs at list prices. They are not sticker prices per token. A model that thinks longer costs more per task at the same token price.
- **Refusal** is the share of attempts the model refused on safety grounds. It matters for security-adjacent coding work: Fable 5.1's rate is visibly higher.
- **Alt config** rows are non-default setups AA also measured (e.g. a lower effort level, or an older model in the same agent).
- **Independent:** AA runs every row itself. No lab-reported numbers are in this table.

How to use it:
- Quote the setup ("Codex with GPT-6 Sol at max"), not just the model.
- Terminal-Bench is where setups differ most (from about 10% to about 58%). DeepSWE is much flatter. If the job is mostly terminal/devops work, weight that column. If it is mostly repo Q&A or reviews, weight SWE-Atlas.
- A score change after an index version change (e.g. v1.5 to v1.6) is a methodology change, not a model change. `tables/changelog.md` flags it.

## Everything else is judgment

There is no measured table for computer use, writing, multimodal work or cheap non-coding bulk work. For those, `references/pick-by-job.md` and the per-model notes are human judgment with linked evidence. Say that when you answer.

Good places to point the user for live numbers (link, don't copy):
- Artificial Analysis Intelligence Index, speed and price: https://artificialanalysis.ai
- Epoch AI Benchmarking Hub (ECI, OSWorld 2.0): https://epoch.ai/benchmarks
- LMArena human-preference leaderboards (text, webdev): https://lmarena.ai
- models.dev for current prices and context windows: https://models.dev

## Comparability warnings

1. **Effort levels.** The same model at `low` and `max` can differ more than two different models do. Always name the effort.
2. **Harness matters.** "Claude Code - Qwen3.8 Max" measures Qwen inside Anthropic's agent, not in Alibaba's own tooling.
3. **Launch-day numbers elsewhere are vendor numbers.** Lab blog posts report their own harness. They are not comparable to this table.
4. **Rerouted API names.** Since 2026-09-14, calls to `deepseek-v4-pro` are served by V4.1-Flash. Scores recorded under that name after that date belong to Flash.
