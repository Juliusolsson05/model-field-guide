# Sources: what each number means

Every table under `tables/` names its source and that source's own as-of date. This file explains what each source measures, who ran it, and how far to trust a comparison.

**Independent** = a third party ran the evaluation or collected the votes. **Vendor-reported** = the lab that made the model published the number. Always say which kind you are quoting.

## Published in our tables (openly licensed)

| Source | What it measures | Who runs it | License |
|---|---|---|---|
| **Epoch AI** Benchmarking Hub | **ECI** (Epoch Capabilities Index), a composite across many benchmarks; plus Epoch's own runs of GPQA Diamond, FrontierMath, SWE-bench Verified, SimpleQA Verified and others; OSWorld 2.0 / OSWorld-Verified from `*_external` files | Independent (Epoch runs most of it). External rows keep their upstream source; we drop any row sourced from Artificial Analysis. | CC BY 4.0 |
| **LMArena** leaderboard dataset | Human-preference Elo from blind side-by-side votes: text, text with style control, webdev, vision, search, document, agent | Independent (crowd votes) | CC BY 4.0 |
| **models.dev** | Price per 1M tokens (incl. cache and long-context tiers), context and output limits, effort values, release date, open-weights flag | Community-maintained from provider docs | MIT |
| **tau2-bench** (Sierra) | Tool-using customer-service agents; pass^k per domain | Submissions, often by the labs themselves; check the submitter | MIT |
| **Terminal-Bench** | Terminal agents completing real shell tasks; accuracy with 95% CI, cost, tokens | Submissions; the repo holds fewer entries than tbench.ai shows | Apache-2.0 |
| **Steel** leaderboard | Computer-use and browser-agent scores (OSWorld, WebArena, BrowseComp, Mind2Web, WebVoyager, GAIA) | **Mostly vendor-reported**, each row links its `sourceUrl` | MIT |

How to read them:
- **ECI** is the headline "how capable overall" number. It is a composite, so it hides job-specific strengths — pair it with the job table.
- **LMArena Elo** measures what people *prefer*, not what is *correct*. Style, length and formatting move it. Prefer the style-controlled board for text.
- **Price is per token, not per task.** A model that thinks twice as long costs twice as much at the same sticker price (see Sonnet 5, Gemini 3.8 Flash, Grok 4.7 notes).
- Steel rows sit in their own "vendor-reported, not independently verified" section. Never mix them into an independent ranking.

## Artificial Analysis: link only

Artificial Analysis (AA) runs good independent evaluations — the Intelligence Index, speed, time-to-first-token, hallucination tests — and model notes in this repo link to its articles. We do **not** put AA numbers in tables. Its Data Platform Terms forbid reproducing its data in structured or tabular form, bulk downloads, combining it with other data, and building products whose purpose is model comparison or selection guidance — even on the free tier. That is why there is no speed column.

**Live AA numbers under your own access:** if the official **OpenRouter MCP** (`https://mcp.openrouter.ai/mcp`) is connected, its `list-benchmarks` tool returns live AA (and Design Arena) scores through your own OpenRouter login. Use it for speed or AA index questions, say the number came from there, and don't copy it back into this repo. Whether that use fits AA's terms is between you, OpenRouter and AA.

## Link-only (cite, never tabulate)

- **ARC Prize** — ARC-AGI results; terms ban aggregated republishing. https://arcprize.org
- **Scale SEAL** — SWE-Bench Pro, Humanity's Last Exam, MCP Atlas; site terms are internal-use only. https://scale.com/leaderboard
- **Vals.ai** — domain-specific enterprise evals; no data license found. https://www.vals.ai
- **LiveBench** — contamination-resistant rolling benchmark; data license unclear. https://livebench.ai
- **llm-stats** — aggregator; its own terms forbid republishing even on paid plans. https://llm-stats.com
- **Every, Simon Willison, Zvi Mowshowitz, Latent Space** — the best qualitative reviews; copyrighted prose. We summarize in our own words and link.

Not used: the SWE-bench leaderboard (non-commercial license, stale), Aider polyglot (stale since 2025-10), HELM (maintenance mode), the HF Open LLM Leaderboard (retired).

## Comparability warnings

1. **Effort levels.** The same model at `low` and `max` can differ by more than two different models do. A row is `(model, effort)`; never compare Astra `max` with Sol `medium` without saying so. If a source doesn't split by effort, the table footnote names the default.
2. **Benchmark versions.** OSWorld vs OSWorld-Verified vs OSWorld 2.0, Terminal-Bench 2.x vs 3.0 vs 4.0, GDPval-AA v2 vs v2.1 — different task sets. Compare only within one version.
3. **Cross-lab OSWorld harnesses.** Each lab reports computer-use scores with its own harness, screenshot resolution, step budget and retries. Vendor OSWorld numbers from different labs are **not comparable**; only same-harness independent runs (Epoch) rank across labs.
4. **Harness-dependent headlines.** ARC-AGI-3 and agentic coding scores swing heavily with the scaffold (e.g. GPT-6 Astra's ARC-AGI-3 result).
5. **Launch-day numbers are vendor numbers.** Independent runs arrive later and can come in lower (AA measured Opus 5.5 below Anthropic's own HLE and Terminal-Bench figures).
6. **Rerouted API names.** `deepseek-v4-pro` has served V4.1-Flash since 2026-09-14; scores taken through that API name after that date belong to Flash.
