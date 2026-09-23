---
id: minimax-m3
display: MiniMax M3
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# MiniMax M3 — cheap open multimodal, cautious by design

**Feel:** Cheap, long-context, multimodal open model that would rather abstain than guess.

**Shines:**
- Frontier-level coding claims for an open model (vendor SWE-Bench Pro result).
- 1M context with sparse attention that keeps long-context serving fast (vendor).
- Native text, image and video from pretraining.
- Very low hallucination rate on AA's knowledge benchmark — because it declines to answer most questions it's unsure of (AA).
- Small active parameter count (~23B of 428B) makes self-hosting cheaper than Kimi/MiMo/DeepSeek Pro.

**Falls over:**
- The flip side of caution: low accuracy on closed-book knowledge questions (AA).
- Released June 2026 — now well behind the September open-weights leaders on independent indexes.
- `minimax-community` license, not MIT/Apache — check commercial terms.

**Reach for it when:** cheap self-hosted multimodal or long-document workers; tasks where "I don't know" beats a confident guess.

**Avoid when:** you need the strongest open model (MiMo-V2.6-Pro, GLM-5.3, Kimi K3); closed-book factual Q&A.

**Effort:** thinking enabled / adaptive / disabled.

**Evidence:**
- [MiniMax launch post](https://www.minimax.io/blog/minimax-m3) (vendor)
- [Hugging Face model card](https://huggingface.co/MiniMaxAI/MiniMax-M3) (vendor) — license, thinking modes
- [Artificial Analysis article](https://artificialanalysis.ai/articles/minimax-m3) (independent; link only)
