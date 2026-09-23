---
id: gemini-3.8-flash
display: Gemini 3.8 Flash
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# Gemini 3.8 Flash — cheap multimodal, slow to start

**Feel:** Cheap, clever on paper, and oddly slow to say its first word.

**Shines:**
- Native video, audio and PDF input at a low price.
- Specialized reasoning (biology research, finance/legal) and raw output speed once it starts (independent reviews).
- Beats Gemini 3.7 Flash on every benchmark Google published (vendor).

**Falls over:**
- Time to first token: AA measured about 13 s, several times the class median (via eesel).
- Uses substantially more output (thinking) tokens than peers on the same tasks, eroding the price advantage.
- Weak on independently run agentic coding (Terminal-Bench 4.0) and computer use (OSWorld).
- Built on 3.7 Flash, not a new base; Google itself says to stay on 3.7 Flash for efficiency-first workloads.
- Introductory price doubles on 2027-01-01.

**Reach for it when:** cheap multimodal ingestion (video, audio, long PDFs), batch jobs where latency doesn't matter.

**Avoid when:** interactive/chat latency matters; computer or browser use; agentic coding; budgets planned past 2026.

**Effort:** low / medium / high thinking. Watch thinking-token spend at `high`.

**Evidence:**
- [Google launch post](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) (vendor)
- [eesel review](https://www.eesel.ai/blog/gemini-3-8-flash) (independent) — TTFT, token use, price change
- [9to5Google launch coverage](https://9to5google.com/2026/09/02/gemini-3-8-flash-launch/) (independent, press)
