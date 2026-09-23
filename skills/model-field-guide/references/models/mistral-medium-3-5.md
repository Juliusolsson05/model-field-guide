---
id: mistral-medium-3-5
display: Mistral Medium 3.5
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# Mistral Medium 3.5 — the self-hostable European all-rounder

**Feel:** A sensible dense model you can run on a handful of GPUs — solid, not frontier.

**Shines:**
- One 128B dense model replacing Mistral's separate general, reasoning (Magistral) and coding (Devstral) lines (vendor).
- Self-hostable on as few as four GPUs; open weights under a modified MIT license.
- 256K context, vision input, function calling, structured outputs (vendor docs).
- Powers Mistral's Vibe remote coding agents.

**Falls over:**
- Five months old and not at the frontier; strong SWE-bench Verified claim is vendor-reported.
- Little independent head-to-head evidence against current Chinese open models.
- "Modified MIT" has conditions — read them; it is not plain MIT.

**Reach for it when:** EU data-residency or on-prem requirements, a dense model that's simpler to serve than trillion-parameter MoEs, general agent work at moderate cost.

**Avoid when:** you need top-end coding or reasoning; very long context (>256K).

**Effort:** reasoning mode toggle (on/off).

**Evidence:**
- [Mistral model card](https://docs.mistral.ai/models/model-cards/mistral-medium-3-5-26-04) (vendor) — context, price, license
- [Mistral Vibe announcement](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/) (vendor)
- [Hugging Face weights](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B) (vendor)
- [MindStudio overview](https://www.mindstudio.ai/blog/what-is-mistral-medium-3-5-open-weight-agent-model) (independent)
