# Data licences

The code and the human-written prose in this repo are MIT (see `LICENSE`).
The generated numbers in `data/` and `skills/model-field-guide/tables/` come
from third parties. Each source is here because its licence allows public
redistribution, with the attribution given below.

## Sources we publish

| Source | What we use | Licence | Required attribution |
|---|---|---|---|
| [Epoch AI Benchmarking Hub](https://epoch.ai/benchmarks/use-this-data) | ECI, and benchmarks Epoch runs itself: GPQA Diamond, FrontierMath Tiers 1-3 v2, SWE-bench Verified, SimpleQA Verified, MirrorCode | CC BY 4.0 | "Benchmark data: Epoch AI, CC BY 4.0 (epoch.ai/benchmarks)" |
| Epoch AI, external rows | Terminal-Bench 2.0 | Apache-2.0 upstream | Epoch AI + Terminal-Bench |
| Epoch AI, external rows | DeepSWE (Datacurve), FrontierSWE, CursorBench (Cursor), OSWorld 2.0 (xlang) | **No data licence stated upstream** (see below) | Epoch AI + the named upstream |
| [LMArena leaderboard dataset](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset) | Text, WebDev and Agent leaderboards (category "overall") | CC BY 4.0 | "Human-preference data: LMArena, CC BY 4.0" |
| [models.dev](https://github.com/anomalyco/models.dev) | Prices, context, output limits, effort levels, knowledge cutoff | MIT | "Pricing: models.dev, MIT" |
| [tau2-bench](https://github.com/sierra-research/tau2-bench) | Leaderboard submissions | MIT | "tau2-bench (Sierra), MIT" |
| [Steel leaderboard](https://github.com/steel-dev/leaderboard) | OSWorld and OSWorld 2.0 compilations (mostly vendor-reported) | MIT | "Steel (leaderboard.steel.dev), MIT" |

### About the external rows with no stated licence

Epoch says external data "retains its original licensing". DeepSWE, FrontierSWE,
CursorBench and the OSWorld 2.0 results site publish scores without a data
licence. We republish them as attributed factual scores that Epoch already
republishes, each with its upstream named in the table. This is a judgment
call, not a grant. If an upstream objects, delete its line from
`EPOCH_BOARDS` in `pipeline/parse.py` and the next nightly run drops it.

## Sources we deliberately do NOT publish

| Source | Why |
|---|---|
| Artificial Analysis | Data Platform Terms v1.1 (2026-08-19) cover the free tier too. They forbid structured or tabular reproduction (§2.3), bulk exports (§2.4) and products for "model/provider selection guidance" (§2.5). The pipeline also drops any Epoch row whose provenance mentions artificialanalysis; `tests/test_pipeline.py` checks this. |
| ARC Prize | Terms forbid aggregation or republication without written permission. |
| llm-stats | Its developer terms forbid republishing the dataset. |
| Scale SEAL, Vals.ai, LiveBench | No redistribution grant found. Link only. |
| OpenRouter `/api/v1/models` | No licence grant; it also embeds Artificial Analysis scores. |
| SWE-bench official leaderboard | CC BY-NC 4.0 (non-commercial). Epoch's own SWE-bench run is used instead. |

`skills/model-field-guide/references/sources.md` explains to agents what each
source measures and where to get the link-only numbers.
