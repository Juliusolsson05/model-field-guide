---
id: claude-sonnet-5
display: Claude Sonnet 5
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# Claude Sonnet 5 — the everyday agent, with a hidden token bill

**Feel:** Near-Opus-4.8 quality at mid-tier sticker price — but it talks more than the price suggests.

**Shines:**
- Everyday agentic coding, multi-file refactors, browser research (independent reviews).
- Knowledge work: vendor and reviewers report it edging Opus 4.8 on GDPval-AA.
- Default model on Claude Free/Pro, so it is what many non-developers actually meet.

**Falls over:**
- New tokenizer maps the same text to more tokens (Anthropic says up to ~1.35×), and it writes longer — reviewers measured per-task cost landing above Opus 4.8 despite the lower per-token price.
- Now sits awkwardly between Opus 5.5 (cheaper per token than before, much stronger) and Haiku/Luna-class models for bulk.
- Anthropic deliberately reduced its cyber capability relative to Opus.

**Reach for it when:** you are already on Claude and want a solid default for routine agent work, or you're on a consumer plan where it's the default.

**Avoid when:** long high-effort autonomous loops where the token bill matters; hard problems (Opus 5.5); bulk extraction (Haiku 4.5 / Luna).

**Effort:** adaptive; keep effort modest for routine work — cost scales fast at high effort.

**Pricing note:** Anthropic made the $2/$10 launch price permanent (edit dated 2026-08-10); some third-party posts still cite a later increase. Check `tables/price-context.md`.

**Evidence:**
- [Anthropic launch post](https://www.anthropic.com/news/claude-sonnet-5) (vendor) — tokenizer, pricing edit
- [Spectrum AI Lab review](https://spectrumailab.com/blog/claude-sonnet-5-review-2026) (independent) — per-task cost finding
- [CodeRabbit review](https://www.coderabbit.ai/blog/claude-sonnet-5-review) (independent)
- [TechCrunch launch coverage](https://techcrunch.com/2026/06/30/anthropic-launches-claude-sonnet-5-as-a-cheaper-way-to-run-agents/) (independent, press)
