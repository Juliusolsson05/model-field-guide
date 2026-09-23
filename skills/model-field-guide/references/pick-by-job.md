# Pick by job

Last human pass: 2026-09-22

**How to read this.** Picks below are human judgment, written from dated reviews and our own use — they are opinions with reasons, not measurements. `tables/coding-agents.md` is measurement: the Artificial Analysis coding-agent leaderboard, refreshed nightly. It only measures coding agents; picks for other jobs are judgment. When a pick and a table disagree, say so and show both. Before recommending, open the model's file in `references/models/<id>.md` (check its `review_by` date) and the table named for the job. Many models here launched in September 2026; files marked `provisional` rest mostly on vendor claims.

Columns: **First** = best result regardless of cost · **Value** = most of the result for much less · **Cheap** = workers / bulk · **Avoid** = known bad fit · **Effort** = reasoning-effort advice · **Check** = the table to quote.

## Big-repo coding & migrations
- **First:** Claude Opus 5.5
- **Value:** GPT-6 Sol
- **Cheap:** GLM-5.3 (supervise: can lock onto a wrong hypothesis), DeepSeek V4.1 Flash
- **Avoid:** Kimi K3 on large codebases (Semgrep saw quality collapse on big repos); Gemini 3.1 Pro for long tool loops
- **Effort:** Opus 5.5 at `medium`–`xhigh`; **never `max` without an output budget** (it can think until it hits the cap). Sol at `high`.
- **Check:** `tables/coding-agents.md` (index, cost and time per task)

## Hardest reasoning / long-horizon engineering
- **First:** Claude Fable 5.1
- **Value:** Claude Opus 5.5 (reported near Fable on most work)
- **Cheap:** none recommended — cheap models fail quietly on this kind of work
- **Avoid:** Fable 5.1 for security or bio work (safety classifiers reroute the request to another model)
- **Effort:** Fable at `high` by default, `xhigh`/`max` only when the problem earns it; cap subagent count
- **Check:** `tables/coding-agents.md` (top of the index)

## Computer & browser use
- **First:** GPT-6 Astra
- **Value:** GPT-6 Sol; GPT-6 Luna at `max` is a vendor claim only
- **Cheap:** GPT-6 Luna (verify on your own flows)
- **Avoid:** Gemini 3.8 Flash (weak OSWorld, slow first token); Muse Spark 1.3 at `xhigh` (big gap to the unreleased `max`)
- **Effort:** quote the effort level for every OSWorld number. Vendor OSWorld harnesses differ across labs, so don't rank across labs from vendor numbers.
- **Check:** judgment only. The leaderboard measures coding agents, not computer use.

## Writing & knowledge work (docs, decks, analysis)
- **First:** split opinion — GPT-6 Astra (Every's best writing model) or Claude Opus 5.5 (most readable prose); Fable 5.1 for delegated multi-hour deliverables
- **Value:** Grok 4.7 (second on GDPval-AA at launch, cautious about facts), Claude Sonnet 5
- **Cheap:** none recommended for final copy
- **Avoid:** GPT-6 Sol / Luna at `max` for deliverables (outputs got shorter and drop required parts); Opus 5.5 on hard deadlines
- **Effort:** Opus 5.5 at `high`/`xhigh` with your own examples
- **Check:** judgment only. The leaderboard measures coding agents, not writing.

## Cheap bulk, extraction, subagents
- **First:** GPT-6 Luna
- **Value:** DeepSeek V4.1 Flash (open weights, off-peak pricing)
- **Cheap:** Gemini 3.8 Flash for batch only (13 s first-token latency, heavy thinking-token use), Claude Haiku 4.5 in Claude-only stacks
- **Avoid:** Luna for closed-book factual recall (very high hallucination rate reported by AA — say "reported", link only)
- **Effort:** lowest effort that passes your check; `none`/off for pure extraction
- **Check:** `tables/coding-agents.md` ("Best score for the money" section)

## Open weights / self-host
- **First:** GLM-5.3 (coding), MiMo-V2.6-Pro (MIT; launch-day, provisional)
- **Value:** DeepSeek V4 Pro weights (MIT); Mistral Medium 3.5 (dense 128B, four GPUs)
- **Cheap:** MiniMax M3 (~23B active), DeepSeek V4.1 Flash
- **Avoid:** assuming "open" means MIT — Kimi K3, GLM-5.3 and MiniMax M3 use custom licenses, Mistral is "modified MIT", Qwen3.8-Max weights aren't open at all
- **Effort:** n/a — depends on serving stack
- **Check:** `tables/coding-agents.md` (Opencode / Kimi Code / DeepSeek rows)

## Frontend / UI
- **First:** Kimi K3 (led Frontend Code Arena at launch)
- **Value:** Qwen3.8-Max (topped Code Arena WebDev after its 0902 update — preference votes, not task completion)
- **Cheap:** GLM-5.3
- **Avoid:** GPT-6 Astra if you care about taste (reviewers flagged a generic look) — but use Astra to *click-test* the UI
- **Effort:** default
- **Check:** judgment only. The leaderboard has no frontend-specific eval.

## Multimodal & long context
- **First:** Gemini 3.1 Pro (preview) for mixed media and long documents
- **Value:** Gemini 3.8 Flash (video, audio, PDF in) for batch
- **Cheap:** MiniMax M3 (self-host, image + video); MiMo-V2.6-Pro adds audio but is launch-day
- **Avoid:** GLM-5.3 (text only); Claude Haiku 4.5 (200K context); Mistral Medium 3.5 above 256K
- **Effort:** Flash at `low`/`medium` — `high` burns thinking tokens
- **Check:** judgment only.

## Real-time / X (Twitter) data
- **First:** Grok 4.7 (native live X search)
- **Value:** any strong model given a web-search tool — the advantage is Grok's X access, not reasoning
- **Cheap:** —
- **Avoid:** answering "what's happening now" from any model without a search tool
- **Effort:** `high`; `xhigh` for synthesis
- **Check:** judgment only.

## Agent Code: multi-pane fleets
- **Lead:** one Claude Opus 5.5 or GPT-6 Astra pane (Astra if the work involves driving apps/browsers)
- **Workers:** GPT-6 Sol or Grok 4.7 for real work; Luna, GLM-5.3 or DeepSeek V4.1 Flash for bulk lanes
- **Avoid:** Fable 5.1 or Opus 5.5 at `max` as workers (runaway tokens, extra subagents); Opus 5.5 panes on older harness code — its API changes move text between tool calls into thinking blocks
- **Effort:** lead at `high`, workers at `medium` or lower; give every pane a token/time budget
- **Check:** `tables/coding-agents.md` (cost and time per task for the workers)
