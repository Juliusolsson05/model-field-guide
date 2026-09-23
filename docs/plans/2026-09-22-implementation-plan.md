# model-field-guide — implementation plan

**Date:** 2026-09-22
**Status:** Plan, not yet built. Every fact below was checked live on the web on 2026-09-22 by six parallel research passes (data sources, Artificial Analysis terms, Agent Skills spec, frontier model landscape, nightly GitHub Actions, prior art). Anything marked **UNVERIFIED** was not confirmed against a primary source and must be checked before we depend on it.
**Working name:** `model-field-guide`. It has no collision on GitHub today. `which-llm` is taken twice, by `richard-gyiko/which-llm` and `ariobarin/which-llm`.

---

## 0. TL;DR: what changed from the original brief

The brief was right about the product: prose we write by hand, plus nightly tables, packaged as an Agent Skill. It was wrong about the data spine.

1. **Artificial Analysis (AA) is out.** The brief treated AA's Terms of Service as a check to do later. It turned out to decide the question. The AA Data Platform Terms v1.1 (revised 2026-08-19) explicitly cover the **free tier**, and they forbid exactly this repo:
   - **§2.3** allows brief public citations only if they "do not reproduce Data in a structured, tabular, or machine-readable format".
   - **§2.4(b)** bans "bulk data downloads (including CSV, Excel, JSON…)".
   - **§2.4(d)** bans combining AA data with other data into anything third parties can use.
   - **§2.5** bans any "Competitive Product" whose primary purpose is "benchmarking, ranking, comparison … or model/provider selection guidance". That last phrase describes our product.
   - The free tier is labelled "Internal use only; no redistribution". Liability for breaching §2.4/§2.5 is **uncapped** (§10.3).
   - The AA website ToS separately bans scraping.
   - Redistribution needs a Commercial contract.
   - Two existing public repos (`garo-pro/aa-leaderboards`, `romancircus/sota-tracker-claw`) do republish AA data. That shows the terms are unenforced so far, not that republishing is permitted.
2. **We use sources that are openly licensed:**
   - **Benchmarks and composite:** Epoch AI (CC BY 4.0).
   - **Human preference:** the LMArena Hugging Face dataset (CC BY 4.0).
   - **Price, context and effort levels:** models.dev (MIT).
   - **Agent benchmarks:** tau2-bench (MIT) and Terminal-Bench (Apache-2.0).
   - **Computer use (vendor-reported):** steel-dev/leaderboard (MIT).
   - Each one is a plain HTTP GET or a zip download.
3. **Epoch's ECI replaces "AA Intelligence Index" as the headline composite.** ECI is the Epoch Capabilities Index. It is CC BY, it is updated daily, it already has Grok 4.7 (released yesterday), and it splits effort variants.
4. **Speed (tokens/s, time to first token) has no source we can redistribute.** AA is the only rich one. We either measure speed ourselves later (phase 2) or leave the column out. For v1 we leave it out and say so in the table header.
5. **Real-world model names, as verified:**
   - Exist: GPT-6 Astra, Claude Opus 5.5 (launched today), Claude Fable 5.1, GLM-5.3, Grok 4.6/4.7.
   - Also launched today: GPT-6 Sol and GPT-6 Luna.
   - **GPT-6 Terra does not exist.**
   - Claude Mythos 5.1 exists but is gated. We exclude it.
6. **Skill packaging:** the skill lives in `skills/model-field-guide/`, not at the repo root, because `gh skill install` cannot install a root `SKILL.md`. The repo is also a Claude Code plugin marketplace and a Codex plugin marketplace.
7. **Updates are the hard part of distribution.** 53% of reused skills on skills.sh are never updated after they are copied (arXiv 2607.00911). Copied installs rot. So the skill checks its own data age and can fetch fresh tables from `raw.githubusercontent.com` at run time.

---

## 1. What we are building (restated after research)

A public GitHub repo that is:

- **A skill.** `skills/model-field-guide/SKILL.md` is loaded by Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Copilot and Agent Code when someone asks "which model should I use for X?" or "what's the current leaderboard?".
- **Two layers, never mixed:**
  - **Layer A, prose (human, slow):** one markdown file per model with shines / fails / use when / avoid when / feel. Each carries `reviewed:` and `review_by:` dates in frontmatter. Plus `pick-by-job.md`.
  - **Layer B, tables (machine, nightly):** generated markdown tables with a data-as-of date, built only from redistributable sources, with an attribution block per source.
- **A nightly GitHub Action.** It fetches, validates, renders, commits only if something changed, tags `snapshot-YYYY-MM-DD`, opens an issue when a new model appears or prose is stale, and opens and updates a single failure issue when a run breaks.

Explicit non-goals, unchanged from the brief:
- It does not replace AA or Arena.
- It does not route or call models.
- It is not a 400-model encyclopedia.
- It never generates vibes with an LLM.

---

## 2. Prior art: the gap is real but narrow

Of about 30 projects surveyed, **none combines per-model prose, nightly data and a skill package.** The closest:

| Project | Has | Lacks | What we take from it |
|---|---|---|---|
| `romancircus/sota-tracker-claw` (MIT, daily) | Nightly data, "forbidden models" list with a reason and a replacement | Prose; not a spec skill; republishes AA | The `forbidden.json` idea becomes our `superseded_by` + reason field |
| `leoncuhk/awesome-llm-bench` (MIT, daily) | Nightly markdown top-10s, commits only on change | Prose, skill | Workflow shape |
| `ariobarin/which-llm` | Claude and Codex marketplaces, runtime fetch of fresh data | Prose; pins `version: 0.4.0`, so data commits never reach Claude plugin users; scrapes AA | Dual marketplace layout, runtime fetch, **the version-pin mistake to avoid** |
| `MadAppGang/dingo` `external-model-selection` | The best prose shape ("Best for / Proven / Why it wins") | Freshness (last updated 2025-11) | Entry shape |
| `itsual/frontier-atlas` | Effort-level routing prose, `SOURCES.md`, "current as of" date | Nightly data, skill | Effort axis, dated sources |
| `richardadonnell/model-watch` | Nightly history, pytest before fetch, rolling "new model suggestions" issue | Prose, skill | Issue-upsert pattern |
| OpenRouter official MCP | Live AA and Design Arena scores through the user's own login | Prose | Optional live pointer (§6.6) |
| Every.to Vibe Check, Simon Willison, Zvi | The best qualitative prose there is | It is copyrighted | We **link and summarize in our own words**, never copy |

What makes us different: **the reasons.** OpenRouter's Auto Router already answers "which model" by share of spend, and learned routers (RouteLLM, Not Diamond) answer it with a classifier. Nobody answers it in dated prose tied to dated evidence.

---

## 3. Data sources: final decision

### 3.1 Spine (fetched nightly, published in tables)

| # | Source | Access | License (verbatim or summarized) | Provides | Effort split | IDs |
|---|---|---|---|---|---|---|
| S1 | **Epoch AI Benchmarking Hub** | `GET https://epoch.ai/data/benchmark_data.zip`. No auth. About 85 CSVs plus `model_metadata.csv`, `benchmark_metadata.csv`, `epoch_capabilities_index/eci_scores.csv`. Alternative: `pip install epochai`. | "Epoch AI's data is free to use, distribute, and reproduce provided the source and authors are credited under the Creative Commons Attribution license." **Caveat:** "data sourced from external projects … retains its original licensing." | ECI composite; Epoch's own runs (GPQA Diamond, FrontierMath, SWE-bench Verified run by Epoch, SimpleQA Verified, MirrorCode…); OSWorld 2.0 and OSWorld-Verified in `*_external.csv` | Yes: a suffix on the model id (`claude-opus-5_max`) plus `model_group` and `display_name` in `model_metadata` | Stable snake-case |
| S2 | **LMArena leaderboard dataset** | HF `lmarena-ai/leaderboard-dataset`. Parquet, or `https://datasets-server.huggingface.co/rows?dataset=lmarena-ai/leaderboard-dataset&config=<cfg>&split=latest&offset=0&length=100` | `license: cc-by-4.0` on the dataset card | Human-preference Elo for `text`, `text_style_control`, `webdev`, `vision`, `search`, `document`, `agent` | Yes, inside the name string (`gpt-6-astra-max`) | Free text, inconsistent, **needs an alias map** |
| S3 | **models.dev** | `GET https://models.dev/models.json` (provider-agnostic, about 425 models) or `api.json` (about 4.9 MB, by provider). No auth. | MIT (`anomalyco/models.dev`, formerly `sst/models.dev`) | Price (USD per 1M tokens, incl. cache, tiers, >200k), context/input/output limits, `reasoning_options` (effort values), knowledge cutoff, release date, `open_weights`, `status: deprecated/beta`, modes (e.g. Opus 5.5 fast mode) | `reasoning_options[{type:"effort", values:[…]}]` | Provider API ids |
| S4 | **tau2-bench** | `https://raw.githubusercontent.com/sierra-research/tau2-bench/main/web/leaderboard/public/submissions/manifest.json` plus `/{submission}/submission.json` | Repo MIT | Tool-use agent pass^k per domain | `reasoning_effort` field | Submission names |
| S5 | **Terminal-Bench** | `harbor-framework/terminal-bench` `leaderboard/submissions/*.json` | Apache-2.0 | Terminal-agent accuracy with 95% CI, cost, tokens | `reasoning_effort` | Submission names. **UNVERIFIED completeness:** the repo had 13 files while tbench.ai shows more; canonical rows come from a keyed Harbor Hub API. |
| S6 | **steel-dev/leaderboard** | `https://raw.githubusercontent.com/steel-dev/leaderboard/main/src/data/{osworld,osworld2,webarena,browsecomp,mind2web,webvoyager,gaia,tauBench}.json` | Repo MIT | Computer-use and browser-agent scores, **mostly vendor-reported**, each with `sourceUrl` | In `systemName` sometimes | Free text |

### 3.2 Cross-checks (fetched, used for validation, not published as a table)

- **LiteLLM `model_prices_and_context_window.json`** (MIT). We flag it when a models.dev price differs from LiteLLM's by more than 10%. The mismatch goes to the job summary and never blocks a run.
- **OpenRouter `GET /api/v1/models`** (no license grant; ToS §12 says "you may not make use of the Materials" unless authorized). Cross-check only; **never commit its values**. Note that it embeds AA scores under `benchmarks.artificial_analysis` for 188 of 454 models, so treat the payload as tainted and extract only the id and price fields.

### 3.3 Optional (phase 2)

- **OpenRouter Datasets API.** It is explicitly CC BY 4.0 ("reuse and republish it, including commercially, with attribution to OpenRouter"). Endpoints like `/api/v1/datasets/rankings-daily` need an API key, allow 30 requests/min and 500/day, and require the citation "Source: OpenRouter (openrouter.ai/rankings), as of {as_of}." That gives a "what people actually spend tokens on" usage table.
- **Our own speed probes.** A nightly job with provider keys sends a fixed prompt and records tokens/s and time to first token. Data we measure is ours to publish. It costs money and keys, and it is not v1.

### 3.4 Link-only (named in `references/sources.md`, never in tables)

| Source | Why link-only |
|---|---|
| Artificial Analysis | Terms (§0) |
| ARC Prize | Terms: no "aggregated, republished … without our express prior written permission"; systematic compilation is banned |
| llm-stats | Its own developer page: "paid plans still prohibit republishing the dataset" |
| Scale SEAL (SWE-Bench Pro, HLE, MCP Atlas) | Website terms are "internal purposes"; no API |
| Vals.ai | No terms found (UNVERIFIED) |
| LiveBench | Leaderboard data license UNVERIFIED |
| OSWorld primary sites | No license |
| Every.to, Simon Willison, Zvi, Latent Space | Copyrighted prose; we link and summarize |

### 3.5 Dead or stale: do not build on

- **SWE-bench leaderboard:** CC BY-NC 4.0, and its last Verified entry is from February 2026.
- **Aider polyglot:** last updated October 2025.
- **HELM:** in maintenance mode since 2026-06-01.
- **HF Open LLM Leaderboard:** retired in March 2025.
- **HLE site:** last updated April 2025.
- **`githubocto/flat`:** archived.
- **`evaleval/EEE_datastore`:** it re-hosts AA, llm-stats and Vals data under an MIT label. That is license laundering, so don't use it.

### 3.6 Epoch provenance rule (important)

Epoch's `*_external.csv` files carry a `Source` column, and some rows are **sourced from AA**:
- `scicode_external.csv` has 174 rows from artificialanalysis.ai, with an "AA model slug" column.
- `critpt_external.csv` is probably AA too (UNVERIFIED).

The fetcher must:
1. Treat non-`_external` files as Epoch's own runs, which are plain CC BY.
2. Keep an `_external` file only if it is on an explicit allowlist in `pipeline/sources.yaml`, **and** drop every row whose `Source` matches `artificialanalysis`. The job **fails** if an AA-sourced row reaches a rendered table. There is a test for this.
3. Record the upstream license per benchmark in `benchmark_meta`, so the attribution block can name it:
   - Terminal-Bench and Aider: Apache-2.0.
   - OSWorld: no stated license. We publish it with attribution and a note. These are factual scores already republished by Epoch and by Steel (MIT). It is low-risk but flagged here as a decision.

---

## 4. Model allowlist (seed)

`pipeline/models.yaml` is a product decision, not a dump. It holds about 20 entries, and each maps our stable id to every source's id. **No shared id exists across sources**, so this alias table is the core artifact of Layer B.

```yaml
# pipeline/models.yaml — the ONLY place model identity is defined.
# Our id == the vendor's API id where one exists (it's the most stable public string).
- id: claude-opus-5-5
  display: Claude Opus 5.5
  lab: Anthropic
  tier: frontier                # frontier | open-frontier | value | fast-cheap | legacy
  released: 2026-09-22
  efforts: [low, medium, high, xhigh, max]
  sources:
    models_dev: anthropic/claude-opus-5-5
    epoch: claude-opus-5-5      # + _<effort> suffixes discovered at fetch time
    lmarena: [claude-opus-5-5, claude-opus-5-5-max]   # alias list; UNVERIFIED until it appears
    steel: "Claude Opus 5.5"
  expect: [models_dev]          # sources that MUST have it; missing => job fails
  prose: references/models/claude-opus-5-5.md
```

**Two kinds of "missing":**
- `expect:` lists the sources that must have the model. If one of those loses it, the run **fails**. This is the brief's "fail loudly if Grok vanishes".
- Anything else is allowed to be absent. A model released today will not be in Epoch or LMArena yet. Tables show `—`, never a guess.

**Seed list (21 models), with facts verified 2026-09-22:**

| id | Display | Lab | Tier | Efforts | $ in/out per 1M | Context |
|---|---|---|---|---|---|---|
| `claude-opus-5-5` | Claude Opus 5.5 | Anthropic | frontier | low…max (default medium) | 4 / 20 | 1M |
| `claude-fable-5-1` | Claude Fable 5.1 | Anthropic | frontier (premium) | low…max | 10 / 50 | 1M |
| `claude-sonnet-5` | Claude Sonnet 5 | Anthropic | value | adaptive | 2 / 10 (docs; intro price possibly ended, UNVERIFIED) | 1M |
| `claude-haiku-4-5` | Claude Haiku 4.5 | Anthropic | fast-cheap | — | 1 / 5 | 200K |
| `gpt-6-astra` | GPT-6 Astra | OpenAI | frontier (premium) | low…max | 10 / 50 | 1.05M |
| `gpt-6-sol` | GPT-6 Sol | OpenAI | value | none…max | 2 / 10 | 1.05M |
| `gpt-6-luna` | GPT-6 Luna | OpenAI | fast-cheap | none…max | 0.10 / 0.50 | 1.05M |
| `gemini-3.1-pro-preview` | Gemini 3.1 Pro (preview) | Google | frontier (aging) | thinking levels | 2 / 12 (≤200K) | 1M |
| `gemini-3.8-flash` | Gemini 3.8 Flash | Google | fast-cheap | low/med/high | 0.75 / 3.75 (doubles 2027-01-01) | 1M |
| `grok-4.7` | Grok 4.7 | xAI | value | low…xhigh | 2 / 6 (≤200K) | 500K |
| `muse-spark-1.3` | Muse Spark 1.3 | Meta | value | xhigh | 1.25 / 4.25 | 1M (id UNVERIFIED) |
| `kimi-k3` | Kimi K3 | Moonshot | open-frontier | low/high/max | 3 / 15 | 1M |
| `glm-5.3` | GLM-5.3 | Z.ai | open-frontier | low/high/max | ~1.40 / 4.40 (secondary source) | 1M |
| `qwen3.8-max` | Qwen3.8-Max | Alibaba | value (API is proprietary) | low/med/xhigh | 2 / 6 | 1M |
| `deepseek-v4-pro` | DeepSeek V4 Pro | DeepSeek | open-frontier | low/high/max | 0.66/1.98 off-peak | 1M |
| `deepseek-flash` | DeepSeek V4.1 Flash | DeepSeek | fast-cheap | on/off | 0.15/0.60 off-peak | 1M |
| `mimo-v2.6-pro` | MiMo-V2.6-Pro | Xiaomi | open-frontier | UNVERIFIED | 0.435 / 0.87 | 1M (id UNVERIFIED) |
| `minimax-m3` | MiniMax M3 | MiniMax | fast-cheap (open) | UNVERIFIED | 0.28 / 1.10 | 1M (id UNVERIFIED) |
| `mistral-medium-3-5` | Mistral Medium 3.5 | Mistral | value (open) | reasoning toggle | 1.50 / 7.50 | UNVERIFIED |
| `claude-opus-5` | Claude Opus 5 | Anthropic | legacy | low…max | 5 / 25 | 1M |
| `gpt-5.6-sol` | GPT-5.6 Sol | OpenAI | legacy | none…max | 4 / 20 | 1.05M |

**Excluded on purpose:**
- Claude Mythos 5.1 and the Gemini Cyber variants are gated.
- `gpt-5.6-terra` is superseded by GPT-6 Sol.
- GPT-6 Terra does not exist.

**Prices in this table are seed facts for review only.** The published price table always comes from models.dev at render time, never from this file.

**Effort variants are first-class.**
- A table row is `(model, effort)` wherever a source splits by effort.
- If a source doesn't split, the row is `(model, "default")` with the default effort named in a footnote.
- We never collapse efforts, and never compare Astra max with Sol medium without saying so.

---

## 5. Repository layout

```
model-field-guide/
├── README.md                         # humans: what it is, install per runtime, attribution
├── LICENSE                           # MIT for code + our prose
├── DATA-LICENSES.md                  # per-source licenses + required attribution strings
├── .claude-plugin/
│   ├── marketplace.json              # Claude Code + Copilot CLI + npx skills read this
│   └── plugin.json                   # name only; NO version (see §8.3)
├── .agents/plugins/marketplace.json  # Codex plugin marketplace
├── skills/
│   └── model-field-guide/            # THE SKILL — self-contained so copy-installs work
│       ├── SKILL.md                  # short procedure (<200 lines)
│       ├── references/
│       │   ├── pick-by-job.md        # job → first pick / cheap pick / avoid (human)
│       │   ├── sources.md            # what each number means, vendor vs independent
│       │   └── models/
│       │       ├── _index.md         # GENERATED: model list + prose freshness badges
│       │       ├── claude-opus-5-5.md
│       │       ├── gpt-6-astra.md
│       │       └── …                 # one per allowlisted model (human)
│       └── tables/                   # GENERATED nightly — never hand-edit
│           ├── _meta.md              # data-as-of per source + staleness rules
│           ├── overall.md            # ECI + LMArena text
│           ├── coding.md             # Epoch SWE-bench Verified (Epoch-run), Terminal-Bench, LMArena webdev
│           ├── agents.md             # tau2, Terminal-Bench, LMArena agent
│           ├── computer-use.md       # OSWorld 2.0 (Epoch) + Steel (vendor-reported, marked)
│           ├── price-context.md      # models.dev
│           └── changelog.md          # last 30 days of movements
├── data/                             # GENERATED machine layer (outside the skill on purpose)
│   ├── snapshot.json                 # normalized, byte-deterministic
│   ├── manifest.json                 # per-source as_of + content hash (see §7.4)
│   └── schema/snapshot.schema.json   # exported from pydantic
├── pipeline/                         # Python, run by CI (never loaded by agents)
│   ├── models.yaml                   # allowlist + alias map (human)
│   ├── sources.yaml                  # which Epoch files/benchmarks, LMArena configs, etc.
│   ├── fetch/{epoch,lmarena,models_dev,tau2,tbench,steel,litellm,openrouter}.py
│   ├── normalize.py                  # → pydantic Snapshot
│   ├── render.py                     # Snapshot → tables/*.md (jinja-free, plain f-strings)
│   ├── diff.py                       # prev vs new → changelog + new-model / vanished lists
│   ├── staleness.py                  # prose review_by checks → _index.md + issue body
│   └── nightly.py                    # orchestrator (validate-all-then-write)
├── tests/
│   ├── fixtures/                     # REAL recorded payloads (see §10)
│   ├── test_normalize.py
│   ├── test_render_snapshot.py       # syrupy snapshots of tables
│   ├── test_provenance.py            # no AA-sourced row ever renders
│   └── test_skill_frontmatter.py     # spec limits (name/desc lengths, fields)
├── evals/                            # trigger + behavior evals (see §9)
├── pyproject.toml / uv.lock
└── .github/workflows/{nightly.yml,ci.yml}
```

Why the layout is shaped this way:

- **Everything an agent reads lives under `skills/model-field-guide/`.** Copy installs (`npx skills`, `gh skill`, Gemini) take only the skill folder, so tables must live inside it.
- **`data/` and `pipeline/` stay outside the skill,** so agents never see a 5 MB JSON file and never pay context for it.
- **One file per model, instead of the brief's single `shines.md`.** The agent opens only the models it's weighing. Each file carries its own `reviewed:` date. PRs for a new launch touch one file.
- **No other `SKILL.md` anywhere in the tree,** including eval fixtures. Codex scans skill roots six levels deep and would load them.
- **No Git LFS.** Claude marketplace clones don't fetch LFS objects.

---

## 6. The skill itself

### 6.1 Frontmatter (spec-portable)

Only spec fields are allowed. The reference validator rejects anything else, and OpenCode ignores anything else.

```yaml
---
name: model-field-guide
description: >-
  Current (nightly-updated) guide to which frontier AI model to use for a job —
  coding, long agentic runs, computer/browser use, writing, cheap bulk work,
  open weights. Use whenever the user asks which model/LLM/provider to pick,
  compares Claude, GPT, Gemini, Grok, GLM, Kimi, DeepSeek, Qwen or others, asks
  for current benchmark scores, prices or a leaderboard, or is choosing models
  for subagents/workers. Your training data is out of date on this topic; this
  skill has dated scores and dated human notes — use it instead of memory.
license: MIT
compatibility: Needs file read access; optional network access to refresh stale tables.
metadata:
  repo: github.com/<owner>/model-field-guide
---
```

Constraints from the research:
- **`name`:** at most 64 characters, lowercase with hyphens, and equal to the folder name (OpenCode, Cursor and `skills-ref` enforce this). No "claude" or "anthropic" in the name.
- **`description`:** at most 1024 characters, the spec and Codex hard limit. Claude allows 1,536. The first sentence carries the use case, because Claude and Codex **truncate descriptions first** when the skill listing overflows its budget (Claude: 1% of context; Codex: about 2% or 8,000 characters).
- **Push it.** skill-creator says models "undertrigger", and agentskills.io says agents skip skills for tasks they think they can handle alone. A "which model" skill hits exactly that failure: the model thinks it already knows. Hence the explicit "your training data is out of date" line.

### 6.2 SKILL.md body: procedure (draft)

Keep the body under 200 lines. The spec budget is under 5,000 tokens.

```markdown
# Model field guide

Paths below are relative to this SKILL.md's directory.

## 1. Check freshness first
Read `tables/_meta.md`. It states "Data as of" per source.
- If the newest date is > 7 days old AND you have network access, fetch the
  latest copies of the table(s) you need from
  https://raw.githubusercontent.com/<owner>/model-field-guide/main/skills/model-field-guide/tables/<file>.md
  and use those. Say you did.
- Otherwise use the local files and state their date.

## 2. Classify the job
coding (big repo / migration / review) · long agentic runs · computer or
browser use · writing & knowledge work · cheap bulk / subagents · open weights /
self-host · multimodal · "just the leaderboard".

## 3. Read `references/pick-by-job.md` for that job.

## 4. Open ONLY the relevant table(s)
coding → tables/coding.md · agents → tables/agents.md · computer use →
tables/computer-use.md · price/context → tables/price-context.md ·
leaderboard → tables/overall.md. Never load all tables.

## 5. Read the prose for the 2–4 candidate models
`references/models/<id>.md`. If its `review_by` date has passed, say the notes
may be stale.

## 6. Answer
- Natural-language recommendation per job, with the reason.
- A small excerpt (≤ 8 rows) of the relevant table.
- Name the reasoning-effort level for every score you quote.
- Quote the data-as-of date and the source (e.g. "Epoch AI, CC BY").
- Distinguish independent vs vendor-reported numbers.

## Rules
- Never invent a score or a price. If it isn't in a table, say "not measured".
- Never rank from memory. "Just give me the leaderboard" → tables/overall.md.
- Models not in `references/models/_index.md` → say they're not covered.
- Prose is judgment, tables are measurements; don't present one as the other.
- Do not compare scores across different benchmark versions or effort levels
  without saying so.
```

### 6.3 Per-model prose file format

```markdown
---
id: gpt-6-astra
reviewed: 2026-09-22        # last HUMAN pass — never touched by CI
review_by: 2026-10-22       # CI flags staleness after this
status: provisional         # provisional (< 2 weeks of evidence) | settled | legacy
superseded_by: null         # e.g. gpt-5.6-terra → gpt-6-sol, with reason
---
# GPT-6 Astra — the computer-user

**Feel:** …one line…
**Shines:** …
**Falls over:** …
**Reach for it when:** …
**Avoid when:** …
**Evidence:** [Zvi 2026-09-xx](…), [Every vibe check](…), [Epoch ECI](…) — summarized, not quoted.
```

Editorial rules, from what keeps caniuse, MDN and GOV.UK docs from rotting:
- `reviewed` is a human date, **separate from the git commit date**, because a bot commit is not a review.
- `review_by` defaults to `reviewed` + 30 days, or + 14 days while `status: provisional`.
- New models start `provisional`. The research found that launch-day prose is mostly vendor claims.
- The nightly job may **flag** staleness. It **never edits prose**.
- "Feel" language is allowed. A causal claim from a single benchmark is not.

### 6.4 `pick-by-job.md` (seed shape)

Each job gets a first pick, a value pick, a cheap pick, an avoid, and a note on effort. The seed below is only a starting point from today's research; it gets a human pass on day 5.

| Job | First pick | Value pick | Cheap / workers | Avoid | Effort note |
|---|---|---|---|---|---|
| Big-repo coding, migrations | Claude Opus 5.5 | GPT-6 Sol | GLM-5.3 (wrong-hypothesis loops: supervise) | Kimi K3 on large codebases (Semgrep precision 0.684) | Opus 5.5: medium–xhigh; **max overthinks** (Willison) |
| Hardest reasoning / long-horizon eng | Claude Fable 5.1 | Opus 5.5 | — | Fable on security/bio (classifier handoff) | |
| Computer / browser use | GPT-6 Astra | GPT-6 Luna at max (vendor claim) | Luna | Gemini 3.8 Flash (OSWorld 59%) | Vendor OSWorld numbers aren't comparable across labs |
| Writing, knowledge work, decks | Opus 5.5 / Astra (split opinion) | — | — | GPT-6 Sol (GDPval regressed) | |
| Cheap bulk, extraction, subagents | GPT-6 Luna | DeepSeek V4.1 Flash | Gemini 3.8 Flash (watch time to first token) | Luna for factual recall (77% hallucination on AA; cite only as "reported") | |
| Open weights / self-host | GLM-5.3, MiMo-V2.6-Pro (MIT) | DeepSeek V4 Pro | MiniMax M3 | Note custom licenses (Kimi, GLM, Qwen) | |
| Frontend / UI | Kimi K3 (Frontend Code Arena lead) | | | | |
| Agent Code: tiling many workers | One Opus 5.5 / Astra lead | Sol / Grok 4.7 workers | Luna / GLM workers | | |

The Agent Code row covers the brief's "12 workers" note. It stays prose, not software.

### 6.5 Attribution

A single `tables/_meta.md` footer, repeated as the last line of each table, carries the required strings:
- "Benchmark data: Epoch AI, CC BY 4.0 (epoch.ai/benchmarks)."
- "Human-preference data: LMArena (arena.ai), CC BY 4.0."
- "Pricing: models.dev, MIT."
- tau2-bench (MIT, Sierra) and Terminal-Bench (Apache-2.0).
- "Computer-use compilation: Steel (leaderboard.steel.dev), MIT; mostly vendor-reported."

Phase 2 adds "Source: OpenRouter (openrouter.ai/rankings), as of {as_of}."

### 6.6 Optional live pointer (no redistribution)

`references/sources.md` tells the agent: if the user has the **official OpenRouter MCP** connected (`https://mcp.openrouter.ai/mcp`), it can call `list-benchmarks` for live AA and Design Arena numbers **under the user's own access**. Our repo never stores them. This is how we reach AA-quality speed and index numbers without breaching §2.4.

The OpenRouter key issued through the MCP's OAuth has a 7-day expiry and a $10 spend cap by default. Is that consistent with AA §2.5 for the end user? That is the user's own relationship with OpenRouter and AA; we only mention the option.

---

## 7. Nightly pipeline

### 7.1 Language and tooling

Python 3.12 managed with **uv**. Versions as of 2026-09-22:

| Tool | Version |
|---|---|
| uv | 0.12.18 |
| astral-sh/setup-uv | v10.2.0 |
| pydantic | 2.13.x |
| pytest | 9.1 |
| syrupy | 6.1 |
| pandas or pyarrow | reading Epoch CSVs and LMArena Parquet |

Why Python and not Node:
- Epoch ships CSVs plus a Python client.
- LMArena ships Parquet.
- LiteLLM's own sync jobs use `uv run --frozen`.

**`setup-uv` no longer publishes floating major tags** (`@v10` doesn't exist), so pin by SHA.

### 7.2 Run order (validate everything, then write)

```
1. fetch all sources → raw payloads in memory (and $RUNNER_TEMP for debugging artifacts)
2. per-source parse → pydantic models (strict; unknown shape = fail)
3. provenance filter (drop AA-sourced Epoch rows; assert none survive)
4. join via pipeline/models.yaml alias map
5. assertions:
   - every `expect:` source has every allowlisted model → else FAIL
   - row counts per table ≥ floor (e.g. models.dev ≥ 15 of 21) → else FAIL (catches empty/HTML error responses)
   - numeric sanity (prices ≥ 0, scores in range)
6. ONLY if all pass: write data/snapshot.json, data/manifest.json, tables/*.md, references/models/_index.md
7. diff vs HEAD snapshot → tables/changelog.md entries, new-models list, vanished list
8. staleness: prose files past review_by → issue body
```

If a source is **down**, as opposed to returning bad data:
- The run keeps yesterday's rows for that source.
- It marks that source's `as_of` as unchanged in `_meta.md`.
- It fails only if the outage lasts longer than 3 consecutive days.

One flaky upstream should not blank the tables. A permanently dead one should page us.

### 7.3 Deterministic output

This is required for "commit only if changed" to mean anything.
- Sort keys and records.
- Fixed float formatting (1 decimal for scores, 2 for prices).
- One record per line.
- **No fetch timestamp inside `snapshot.json` or the tables.** The date shown is each **source's own as-of date** (Epoch's "Updated" date, LMArena's `leaderboard_publish_date`, the models.dev commit), so an unchanged source produces a byte-identical file.

### 7.4 manifest.json

```json
{
  "schema_version": 1,
  "sources": {
    "epoch":      {"as_of": "2026-09-22", "sha256": "…", "license": "CC-BY-4.0"},
    "lmarena":    {"as_of": "2026-09-13", "sha256": "…", "license": "CC-BY-4.0"},
    "models_dev": {"as_of": "2026-09-22", "sha256": "…", "license": "MIT"}
  }
}
```

The skill's freshness check reads the rendered `_meta.md`. Tooling reads this JSON.

### 7.5 Changelog rules (written for skimming)

Emit an entry for any of:
- A new allowlisted model appears in a source.
- A model vanishes from a source.
- A model's ECI moves by 2 points or more.
- An LMArena rating moves by 15 or more, or its rank moves by 3 or more.
- A price changes by 5% or more.
- A new effort variant appears.

Example lines:

```
## 2026-09-23
- Epoch ECI: Claude Opus 5.5 (max) added at 16x.x.
- models.dev: gpt-6-sol price 2.00/10.00 (new).
- LMArena webdev: grok-4.7-high added, rank #4.
```

Keep a rolling 30 days in `tables/changelog.md`. Git history is the archive.

### 7.6 `nightly.yml` (adapted from research; SHAs resolved 2026-09-22)

```yaml
name: nightly-snapshot
on:
  schedule:
    - cron: "41 3 * * *"        # UTC; odd minute (top-of-hour runs are delayed/dropped most)
  workflow_dispatch:            # launch-day manual refresh
permissions:
  contents: read
concurrency:
  group: nightly-snapshot
  cancel-in-progress: false
jobs:
  snapshot:
    if: github.repository == 'OWNER/model-field-guide'   # forks no-op
    runs-on: ubuntu-latest
    timeout-minutes: 15
    permissions:
      contents: write
      issues: write
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
        with: { enable-cache: true, cache-dependency-glob: uv.lock }
      - run: uv sync --frozen
      - run: uv run --frozen pytest -q            # renderer/provenance/frontmatter tests on fixtures
      - name: Fetch, validate, render
        run: uv run --frozen python -m pipeline.nightly --issues-dir .nightly   # .nightly/ is gitignored
      - name: Commit + tag if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add data/ skills/model-field-guide/tables/ skills/model-field-guide/references/models/_index.md
          if git diff --cached --quiet; then echo "No changes."; exit 0; fi
          day=$(date -u +%F)
          git diff --cached --stat | tee -a "$GITHUB_STEP_SUMMARY"
          git commit -m "chore(data): snapshot $day"
          git push origin HEAD
          git tag "snapshot-$day" && git push origin "snapshot-$day" || true   # immutable; 2nd run same day skips
      - name: New-model / stale-prose issues
        if: ${{ hashFiles('.nightly/*.md') != '' }}
        continue-on-error: true
        env: { GH_TOKEN: "${{ github.token }}" }
        run: uv run --frozen python -m pipeline.issues .nightly   # upsert by title; never duplicate
      - name: Staleness watchdog
        run: |
          age=$(( ( $(date +%s) - $(git log -1 --format=%ct -- data/) ) / 86400 ))
          [ "$age" -le 45 ] || { echo "::error::data unchanged for $age days"; exit 1; }
      - name: Failure issue
        if: failure()
        env: { GH_TOKEN: "${{ github.token }}" }
        run: |
          url="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
          n=$(gh issue list --label nightly-failure --state open --json number --jq '.[0].number')
          if [ -n "$n" ]; then gh issue comment "$n" --body "Failed again: $url"
          else gh issue create --title "Nightly snapshot failing" --label nightly-failure --body "Run: $url"; fi
```

Why each choice (verified gotchas):
- **Issues, not PRs, for "new model appeared".**
  - PRs created with `GITHUB_TOKEN` need the repo setting "Allow GitHub Actions to create and approve pull requests", which is off by default.
  - Since 2026-06-11, such PRs' CI sits in an approval-required state.
  - An issue needs only `issues: write` and notifies watchers.
  - The human then edits `models.yaml` and adds a prose file in a normal PR.
- **The issue writer uses a workspace-local `.nightly/` directory.** `hashFiles()` only sees `$GITHUB_WORKSPACE`, so the research pass's `$RUNNER_TEMP` variant would never fire.
- **Labels (`new-model`, `stale-prose`, `nightly-failure`) are created once at setup,** or `--label` fails.
- **The 60-day auto-disable.** Public repos' scheduled workflows are disabled after 60 days without "repository activity".
  - Bot commits appear to count: `arena-ai-leaderboards` is still running 67 days after its last human commit (observed, not documented).
  - The risk is that commit-if-changed makes no commits in a quiet stretch. Epoch updates daily, so a quiet stretch is very unlikely.
  - The watchdog at 45 days catches it anyway.
  - **Do not use keepalive-commit actions.** GitHub blocked `gautamkrishnar/keepalive-workflow` for a ToS violation in April 2025.
- **Failure notification.** Scheduled-run failure emails go only to the user who last edited the cron line. The failure issue reaches everyone watching.
- **Tags.** Immutable daily tags give pinning (`raw.githubusercontent.com/<owner>/model-field-guide/snapshot-2026-09-22/...`). Tags pushed with `GITHUB_TOKEN` don't trigger other workflows, which is fine here. No daily GitHub Releases, because they would spam notifications.
- **Repo growth.** It is tiny. One comparable repo is about 1.8 MB after about 100 daily commits. Keep one record per line so git's delta compression works.

`ci.yml` runs `pytest`, `skills-ref validate skills/model-field-guide`, and `claude plugin validate` (if available) on every PR.

---

## 8. Distribution: one repo, every runtime

### 8.1 Claude Code (plus Copilot CLI and `npx skills`, which read the same file)

`.claude-plugin/marketplace.json`:
```json
{
  "name": "model-field-guide",
  "owner": { "name": "<owner>" },
  "plugins": [
    { "name": "model-field-guide", "source": "./",
      "description": "Nightly-updated, human-edited guide to which frontier model to use for which job.",
      "license": "MIT", "category": "reference" }
  ]
}
```
The plugin root is `./`, and Claude scans `skills/` by default. Install:

```
/plugin marketplace add <owner>/model-field-guide
/plugin install model-field-guide@model-field-guide
```

The marketplace name must not be a reserved name (`agent-skills`, `claude-plugins-official`, and so on).

### 8.2 Codex

`.agents/plugins/marketplace.json`:

```json
{"name":"model-field-guide","interface":{"displayName":"Model Field Guide"},"plugins":[{"name":"model-field-guide","source":{"source":"local","path":"./"},"policy":{"installation":"AVAILABLE","authentication":"ON_INSTALL"},"category":"reference"}]}
```

Install with `codex plugin marketplace add <owner>/model-field-guide`, or clone into `~/.agents/skills/`.

### 8.3 Updates (the part most skills get wrong)

- **Claude plugin versioning.** If `plugin.json` has **no `version`**, the git commit SHA is the version, so every nightly commit counts as an update. `ariobarin/which-llm` pinned `version: 0.4.0`, and its data commits never reached Claude users. **Leave `version` out.**
- **Third-party marketplace auto-update is off by default.** The README tells users to enable it in `/plugin`.
- **Copy installs only refresh on explicit update:** `npx skills update`, `gh skill update --all`, Gemini reinstall.
- **Runtime self-refresh (§6.2 step 1) is therefore the real freshness guarantee.** The skill notices when `_meta.md` is more than 7 days old and fetches the raw GitHub copy.
- **Pinning for "freeze for prod":** `/plugin marketplace add <owner>/model-field-guide@snapshot-2026-09-22`, `npx skills add <owner>/model-field-guide#snapshot-2026-09-22`, `gh skill install … --pin snapshot-2026-09-22`.

### 8.4 Others

| Runtime | Install |
|---|---|
| OpenCode | Reads `.claude/skills`, `.agents/skills`, `~/.config/opencode/skills`; clone or `npx skills add` |
| Cursor | Reads `.agents/skills`, `.cursor/skills` and the `.claude` / `.codex` equivalents |
| Gemini CLI | `gemini skills install https://github.com/<owner>/model-field-guide --path skills/model-field-guide` |
| Copilot | `gh skill install <owner>/model-field-guide model-field-guide` (GitHub CLI 2.90+, preview) |
| Agent Code | Its managed-skills / GitHub skill installer deploys it to every pane's runtime. Pin a snapshot tag there. |

---

## 9. Evaluation: does it trigger, and does it answer well?

### 9.1 Trigger eval (day 4)

Use the agentskills.io method:
- About 20 queries: 10 that should trigger, 10 near-misses that should not.
- Run each 3 times. Pass means a trigger rate of 0.5 or more.
- Split 60/40 into train and validation, iterate the **description** up to 5 times, and keep the best validation score.

Should trigger:
- "which model should I use to migrate this monorepo"
- "is Grok 4.7 better than Sol for coding"
- "cheapest decent model for 10k extractions"
- "what's the best computer-use model right now"
- "give me the current LLM leaderboard"
- "what should my subagents run on"
- …

Should not trigger:
- "switch this code from the OpenAI SDK to Anthropic's"
- "what's a transformer"
- "fix this failing test"
- "how do I set the model in Claude Code settings.json"
- …

Tooling:
- **Claude:** `claude plugin eval` (v2.1.269+), with `evals/<case>/prompt.md` and a `tool_used` grader (`tool: Skill`, `input_match`). Each case runs 3 times with the plugin and 3 times without, and reports the difference. In CI: `--json --threshold --max-cost-usd`.
- **Cross-runtime:** promptfoo's `skill-used` / `not-skill-used` assertions over the Claude Agent SDK, Codex SDK and OpenCode SDK providers, `--repeat 3`.
- **Optimizer:** anthropics/skills `skill-creator` `scripts.run_loop` can automate the description loop.

### 9.2 Behavior eval

Five real questions from the brief, graded by rubric (LLM grader in `claude plugin eval`):

1. "Migrate 400k lines + a model living in the browser for QA."
   - Must name Opus 5.5 for the migration and Astra for browser QA.
   - Must give the cheap-worker option with its caveat.
   - Must cite the as-of date.
   - Must not invent numbers.
2. "Just give me the leaderboard."
   - Must quote `tables/overall.md` rows verbatim with the date.
   - Must not produce a ranking from memory.
3. "Is Mythos good?"
   - Must say it is gated and not covered.
4. "Best open-weights coder I can self-host?"
   - Must mention the license caveats.
5. "Compare Astra max and Sol medium on OSWorld."
   - Must flag the effort mismatch and the cross-lab comparability problem.

Also test at **Haiku, Sonnet and Opus** tiers, as Anthropic's best-practices doc says.

---

## 10. Testing the pipeline

Following the "integration tests from recorded real data" rule:
- **Fixtures are real recorded payloads**, captured once on day 2 and trimmed to the allowlisted rows: the Epoch zip subset, LMArena rows JSON, `models.json`, a tau2 manifest plus two submissions, two Terminal-Bench submissions, and Steel `osworld2.json`.
  - This session's research downloaded most of them into a temporary scratchpad. Re-record them on day 2 rather than relying on that path.
- **`test_render_snapshot.py`:** syrupy snapshots of every table from the fixtures. A renderer change shows up as a readable diff.
- **`test_provenance.py`:** inject an Epoch `_external` row with `Source=artificialanalysis.ai` and assert it never renders and the run fails if it would. Also assert that no OpenRouter `benchmarks.*` field ever reaches the snapshot.
- **`test_missing_expected.py`:** delete `grok-4.7` from the models.dev fixture and assert the nightly exits non-zero **and writes nothing**.
- **`test_determinism.py`:** render twice and assert byte-identical output. Shuffle the input order and assert the output is still identical.
- **`test_skill_frontmatter.py`:** name 64 characters max and equal to the folder name; description 1024 characters max; only spec fields; SKILL.md under 500 lines.
- A **live smoke** job (`workflow_dispatch` only) runs the real fetchers without writing anything, to catch upstream shape changes on demand.

---

## 11. Build sequence (brief's five days, corrected)

**Day 1: repo and prose.**
- Create `model-field-guide` (public, MIT). Add the layout from §5, `SKILL.md` from §6.2, and the frontmatter from §6.1.
- Write prose files for the 4–6 models you know best: Opus 5.5, Fable 5.1, Astra, Sol, GLM-5.3, Grok 4.7. Start from the research notes in Appendix B, rewritten in your own voice with `status: provisional` where under 2 weeks old.
- Write `pick-by-job.md` v0.
- Write `DATA-LICENSES.md`.

**Day 2: data by hand.**
- Record fixtures (§10).
- Write `pipeline/models.yaml` with the alias map for all 21 models. This is the slowest part: open each source and find each model's id string.
- Render `tables/coding.md` and `tables/computer-use.md` by hand-running `render.py` on fixtures until you like the columns.

**Day 3: automation.**
- Build out all fetchers, `normalize`, `diff`, `staleness` and `issues`.
- Tests from §10.
- Add `nightly.yml` on a branch, with `workflow_dispatch` to exercise it.
- Create the labels.
- Merge. The first scheduled run happens the next morning.

**Day 4: install and trigger tuning.**
- Install into Claude Code via the marketplace and into Codex.
- Run the trigger eval (§9.1) and iterate the description.
- Run the five behavior questions (§9.2).

**Day 5: polish and pin.**
- Changelog formatting.
- README install matrix (§8).
- Complete `pick-by-job.md` and write the remaining prose files (the `provisional` ones can be short).
- Pin `snapshot-YYYY-MM-DD` in Agent Code.

**Ongoing:**
- About 20 minutes after each lab drop: add the model to `models.yaml` and write a provisional prose file.
- About 5 minutes a day skimming `changelog.md`.
- Clear `stale-prose` issues weekly.

**Phase 2 (only if wanted):**
- OpenRouter Datasets usage table (needs a key; CC BY).
- Our own speed probes (needs provider keys and money).
- Vendor-reported table with an explicit label, from models.dev `benchmarks[]` (with AA entries filtered out).

---

## 12. Risks and open decisions

| Risk / decision | Mitigation / recommendation |
|---|---|
| **No speed column in v1** | Say so in `price-context.md`. Point to the optional OpenRouter MCP (§6.6). Phase-2 probes. |
| LMArena names are free text and shift | The alias list in `models.yaml` carries multiple names. An unmatched frontier-looking name opens a "possible alias" issue instead of failing. |
| Terminal-Bench repo may be incomplete vs tbench.ai | Use it as-is, labelled "submissions in repo". Revisit if Harbor Hub publishes an open export. |
| Steel data is mostly vendor-reported | Separate section headed "vendor-reported, not independently verified", with the `sourceUrl` per row. |
| OSWorld upstream has no license | We consume it through Epoch (CC BY with an upstream caveat) and Steel (MIT). These are factual scores. Documented in `DATA-LICENSES.md`. Low risk, but it's your call. |
| Epoch schema changes (new CSVs, renamed columns) | Strict parsing makes the run fail loudly and yesterday's data is kept. `sources.yaml` pins which files we read. |
| Launch-day prose is mostly vendor claims | `status: provisional` plus a 14-day `review_by`. |
| AA tables would be nicer | Only via a Commercial contract. Don't. |
| Skill doesn't auto-trigger | The eval loop on day 4. The description explicitly says the model's memory is out of date. |
| Name | `model-field-guide` is free on GitHub today. Alternatives: `pick-a-model`, `frontier-field-guide`. `which-llm` is taken twice. |
| Public vs private repo | Recommend **public**. The whole data stack is redistributable, which was the point of dropping AA. |

---

## Appendix A: key sources

- AA Data Platform Terms v1.1: https://artificialanalysiscdn.com/legal/ProDataPlatformTerms.pdf · tiers: https://artificialanalysis.ai/data-api · API docs: https://artificialanalysis.ai/data-api/docs
- Epoch: https://epoch.ai/benchmarks/use-this-data · https://epoch.ai/data/benchmark_data.zip · https://github.com/epoch-research/epochai
- LMArena: https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset
- models.dev: https://models.dev/models.json · https://github.com/anomalyco/models.dev
- tau2-bench: https://github.com/sierra-research/tau2-bench · Terminal-Bench: https://github.com/harbor-framework/terminal-bench · Steel: https://github.com/steel-dev/leaderboard
- LiteLLM: https://github.com/BerriAI/litellm · OpenRouter terms: https://openrouter.ai/terms · OpenRouter Datasets (CC BY): https://openrouter.ai/docs/api/api-reference/datasets/daily-token-totals-for-top-50-models.md · OpenRouter MCP: https://openrouter.ai/docs/guides/overview/mcp-server
- ARC terms: https://arcprize.org/terms · llm-stats: https://llm-stats.com/developer · SWE-bench license: https://github.com/SWE-bench/swe-bench.github.io
- Agent Skills spec: https://agentskills.io/specification · client guide: https://agentskills.io/client-implementation/adding-skills-support · descriptions: https://agentskills.io/skill-creation/optimizing-descriptions · evals: https://agentskills.io/skill-creation/evaluating-skills
- Claude Code: https://code.claude.com/docs/en/skills · https://code.claude.com/docs/en/plugin-marketplaces · https://code.claude.com/docs/en/plugin-evals · best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Codex: https://developers.openai.com/codex/skills · OpenCode: https://opencode.ai/docs/skills/ · Cursor: https://cursor.com/docs/context/skills · Gemini CLI: https://geminicli.com/docs/cli/skills/ · Copilot: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills · `gh skill`: https://cli.github.com/manual/gh_skill_install · `npx skills`: https://github.com/vercel-labs/skills · promptfoo: https://www.promptfoo.dev/docs/guides/test-agent-skills/
- GitHub Actions: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows · https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows · https://github.blog/changelog/2026-06-11-bot-created-pull-requests-can-run-workflows-if-approved/ · git scraping: https://simonwillison.net/2020/Oct/9/git-scraping/
- Prior art: https://github.com/romancircus/sota-tracker-claw · https://github.com/leoncuhk/awesome-llm-bench · https://github.com/ariobarin/which-llm · https://github.com/richard-gyiko/which-llm · https://github.com/itsual/frontier-atlas · https://github.com/richardadonnell/model-watch · skill-rot study: https://arxiv.org/abs/2607.00911
- AA methodology criticism: https://the-decoder.com/artificial-analysis-overhauls-its-intelligence-index-after-gpt-6-astra-scoring-drew-skepticism/

## Appendix B: street-consensus notes (seed for prose; rewrite in your own voice)

Summarized from the landscape research, with sources.

- **Claude Opus 5.5** (2026-09-22; `claude-opus-5-5`; $4/$20; efforts low…max, default medium)
  - Shines: idiomatic, concise, follows instructions better than Opus 5. Codex converts are coming back (Every).
  - Fails: **at max effort it thinks until it hits the 128K output cap on trivial prompts** (Willison: "effectively useless" at max). Unconstrained, it runs indefinitely. Misses deadline-bound deliverables.
  - Use at medium–xhigh.
  - Independent vs vendor: AA measured HLE and TB4 below Anthropic's own figures.
  - Breaking API changes: thinking is always on, forced `tool_choice` errors, and text between tool calls moves into `thinking` blocks. That last one matters to Agent Code.
  - Sources: anthropic.com/claude-opus-5-5 · simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/ · every.to vibe check
- **Claude Fable 5.1** (2026-09-01; $10/$50)
  - Shines: strongest for hard long-horizon engineering (Every, Zvi); simplifies code.
  - Fails: slow and expensive. Security and bio requests get handed off to Opus 4.8. Overshoots explicit limits. Spawns too many subagents at max.
  - Sources: every.to/vibe-check/fable-5-1-vibe-check · thezvi 2026-09-05
- **GPT-6 Astra** (2026-09-03; $10/$50)
  - Shines: computer use ("basically solved", Zvi); runs for hours in apps; 3D and Blender; very token-efficient (about 27K tokens per AA task). Every called it the best writing model.
  - Fails: stops arbitrarily, overcomplicates, "slop" aesthetic, weaker product instincts than Fable. Its ARC-AGI-3 99.9% depends on the harness.
  - Sources: thezvi.substack.com/p/gpt-6-astra-can-do-ambitious-things · every.to/vibe-check/gpt-6-astra-vibe-check
- **GPT-6 Sol** (2026-09-22; $2/$10)
  - Shines: price-performance on coding and code review. Willison's new Codex default.
  - Fails: intelligence flat vs GPT-5.6 Sol; GDPval regressed.
  - Source: the-decoder
- **GPT-6 Luna** ($0.10/$0.50)
  - Shines: bulk work and subagents.
  - Fails: high hallucination rate; weak on factual recall.
- **Grok 4.7** (2026-09-21; $2/$6; 500K context)
  - Shines: cheap for its tier; lowest hallucination rate measured; live X search.
  - Fails: "second-tier" on GDPval and CursorBench (Decrypt); 2× the tokens of 4.6; slow time to first token.
- **GLM-5.3** (2026-08-14; weights 2026-08-28; custom license, not MIT)
  - Shines: big post-training gain (Terminal-Bench 3.0 went from 4.6 to 28.3); good security review with few false positives; "decide once, execute" style; cheap plan that works in Claude Code and OpenCode.
  - Fails: text only; repetitive creative output. Your brief's "goes feral on a wrong hypothesis" wasn't independently sourced in this research, so keep it as your own observation.
- **Kimi K3**
  - Shines: leads Frontend Code Arena; largest open-weights model.
  - Fails: 36% trap-task failure rate; Semgrep precision 0.684 on large codebases.
- **Gemini 3.8 Flash**
  - Shines: cheap; native video, audio and PDF input.
  - Fails: 13.3 s time to first token (eesel), heavy thinking-token use, weak on Terminal-Bench 4.0 and OSWorld. Price doubles on 2027-01-01.
  - Gemini 3.5 Pro is still unreleased.
- **DeepSeek V4 Pro / V4.1 Flash**
  - Shines: very cheap, off-peak pricing, 384K output.
  - Fails: agentic gains are not independently reproduced.
- **Qwen3.8-Max**
  - All strengths are vendor claims (OSWorld-Verified 86.1).
  - Treat as provisional.
- **MiMo-V2.6-Pro** (released today; MIT)
  - Top open-weights model on AA (46).
  - Launch-day, so treat as provisional.
