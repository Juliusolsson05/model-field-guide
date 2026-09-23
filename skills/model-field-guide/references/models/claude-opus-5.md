---
id: claude-opus-5
display: Claude Opus 5
reviewed: 2026-09-22
review_by: 2026-10-22
status: legacy
superseded_by: claude-opus-5-5
---
# Claude Opus 5 — legacy; use Opus 5.5

**Feel:** Near-Fable-5 intelligence at Opus prices, with a stiffer voice than its successor.

**Why legacy:** Opus 5.5 (2026-09-22) is cheaper per token, reported to perform near Fable 5.1, and fixes the communication-style complaints (Willison, Every).

**Shines (historically):**
- Strong on complex reasoning, hard coding and long unattended agent runs (independent reviews).
- Adaptive thinking and 1M context became the Opus default with this release.

**Falls over:**
- On routine work (short drafts, classification, boilerplate) it didn't meaningfully beat Sonnet 5 or Haiku 4.5 (eesel review).
- Heavier token use than Fable 5.1 (Every noted Fable 5.1 uses about half Opus 5's tokens).

**Reach for it when:** a pinned workflow depends on its exact behavior, or your harness hasn't adapted to Opus 5.5's API changes (thinking always on, forced `tool_choice` rejected). Plan the migration.

**Avoid when:** starting anything new.

**Effort:** `low`…`max`; thinking can be disabled only at `high` or lower.

**Evidence:**
- [Anthropic launch post](https://www.anthropic.com/news/claude-opus-5) (vendor) — released 2026-07-24
- [eesel review](https://www.eesel.ai/blog/claude-opus-5-review) (independent)
- [Simon Willison on Opus 5.5](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/) (independent) — successor comparison
