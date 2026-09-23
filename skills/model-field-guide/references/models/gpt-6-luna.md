---
id: gpt-6-luna
display: GPT-6 Luna
reviewed: 2026-09-22
review_by: 2026-10-06
status: provisional
superseded_by: null
---
# GPT-6 Luna — the bulk worker

**Feel:** Absurdly cheap and competent at structured work — just don't ask it what it remembers.

**Shines:**
- Price: among the cheapest models OpenAI has shipped, about half of GPT-5.6 Luna (Willison).
- Fast and competent at SQL and web-dev tasks in Willison's agent demo.
- Bulk extraction, classification, subagent fan-out.

**Falls over:**
- Factual recall: AA's hallucination benchmark still shows a very high rate at `max`, even after improving on 5.6 Luna (reported, AA; link only).
- Knowledge-work deliverables regressed versus 5.6 Luna (GDPval-AA, via The Decoder).
- Intelligence index flat versus its predecessor — the win is price, not capability.

**Reach for it when:** high-volume structured tasks where the answer is in the input (extraction, transforms, SQL over given schemas), cheap subagents under a stronger lead.

**Avoid when:** closed-book factual questions, research summaries without sources, anything where a confident wrong answer is costly.

**Effort:** `none`…`max`. OpenAI claims strong computer-use numbers at `max` — vendor claim, unverified.

**Evidence:**
- [Simon Willison, 2026-09-22](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/) (independent)
- [The Decoder](https://the-decoder.com/openais-gpt-6-sol-and-luna-cut-prices-in-half-but-barely-move-the-needle-on-performance/) (independent)
- [Artificial Analysis: GPT-6 Luna](https://artificialanalysis.ai/models/gpt-6-luna) (independent; link only — hallucination rate)
