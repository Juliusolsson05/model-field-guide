---
id: gemini-3.1-pro-preview
display: Gemini 3.1 Pro (preview)
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# Gemini 3.1 Pro (preview) — the aging Google flagship

**Feel:** Was a reasoning-benchmark leader in February; seven months later it's a strong-but-dated preview waiting on a successor.

**Shines:**
- Graduate-level science and abstract reasoning benchmarks at launch (vendor-reported GPQA Diamond and ARC-AGI-2 results).
- 1M context and native multimodal input.
- Tight fit with Google Workspace / Vertex AI; that is where independent reviewers found most of its value.

**Falls over:**
- Multi-step agentic coding: independent reviews show it trailing Claude and GPT on Terminal-Bench-style chained tasks.
- SQL / data reasoning is a weak spot in independent testing.
- 64K output cap, half of the current Claude/GPT output limits (secondary source).
- Still a preview: developers have reported quality drift in AI Studio over time.

**Reach for it when:** you are inside the Google stack, need Google-grade multimodal/long-document input, or are comparing against a known long-lived baseline.

**Avoid when:** agentic coding, long tool loops, very long outputs. Gemini 3.5 Pro is not released as of this review.

**Effort:** thinking levels (low/high). Launch benchmarks were at the highest level.

**Evidence:**
- [Gemini API model page](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview) (vendor)
- [LayerLens benchmark review](https://layerlens.ai/blog/gemini-3-1-pro-benchmark-review) (independent)
- [Git AutoReview coding review](https://gitautoreview.com/blog/gemini-3-pro-code-review) (independent) — output cap, Terminal-Bench gap
- [Google AI developer forum thread](https://discuss.ai.google.dev/t/gemini-3-1-pro-preview-got-significantly-worse/144157) (independent, user reports)
