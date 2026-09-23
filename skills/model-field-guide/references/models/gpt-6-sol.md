---
id: gpt-6-sol
display: GPT-6 Sol
reviewed: 2026-09-22
review_by: 2026-10-06
status: provisional
superseded_by: null
---
# GPT-6 Sol — GPT-5.6 Sol at half the price

**Feel:** Same brain as GPT-5.6 Sol, half the bill — a price move more than a capability move.

**Shines:**
- Price-performance for coding, code review and long-horizon implementation when the target is clear (inherited from 5.6 Sol's reputation).
- Willison made it one of his default models in Codex on launch day.
- Independent indexes put its intelligence level with GPT-5.6 Sol at roughly half the per-task cost (AA via The Decoder).

**Falls over:**
- Capability is flat versus GPT-5.6 Sol — gains on some evals, regressions on others.
- Knowledge-work deliverables regressed at `max`: shorter outputs that more often omit required pieces (GDPval-AA, reported by The Decoder).
- OpenAI's launch benchmark selection omitted knowledge-work and agentic-coding evals — read vendor charts skeptically.

**Reach for it when:** you want a strong, cheap coding/review default in the OpenAI stack; worker model under an Opus 5.5 / Astra lead.

**Avoid when:** writing, decks and knowledge-work deliverables (Opus 5.5, Astra, Fable 5.1); computer use at the top end (Astra).

**Effort:** `none`…`max`. For deliverables, check output completeness at `max` rather than assuming more effort = better.

**Evidence:**
- [Simon Willison, 2026-09-22](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/) (independent)
- [The Decoder: prices halved, performance barely moved](https://the-decoder.com/openais-gpt-6-sol-and-luna-cut-prices-in-half-but-barely-move-the-needle-on-performance/) (independent)
- [Artificial Analysis article](https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier) (independent; link only)
- Launch-day: re-review once coding-agent evals land.
