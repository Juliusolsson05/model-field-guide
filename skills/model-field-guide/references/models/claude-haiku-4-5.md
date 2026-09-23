---
id: claude-haiku-4-5
display: Claude Haiku 4.5
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# Claude Haiku 4.5 — the old reliable Claude worker

**Feel:** Fast, cheap-ish, predictable Claude — a generation old and it shows on hard tasks.

**Shines:**
- Low latency and high throughput for the many small calls an agent makes: file triage, summarization, tool routing.
- Well-trodden as a Claude subagent/worker model; behaves like the bigger Claudes in tool use.
- Long track record — few surprises in production.

**Falls over:**
- Clearly below Sonnet/Opus on hard reasoning and hard coding.
- 200K context, not 1M like the current frontier.
- Price per token is now roughly 10× GPT-6 Luna's; the cheap-tier crown has moved.

**Reach for it when:** you want a Claude-native cheap worker in a Claude-only stack, or need a stable, well-understood model for classification/routing.

**Avoid when:** price is the main driver (Luna, DeepSeek Flash, Gemini Flash are cheaper); long-context work; anything that needs real reasoning depth.

**Effort:** no effort ladder of note; keep extended thinking off for bulk work.

**Evidence:**
- [Anthropic Haiku page](https://www.anthropic.com/claude/haiku) (vendor)
- [OrcaRouter: GPT-6 Luna vs Haiku 4.5](https://www.orcarouter.ai/blog/gpt-6-luna-vs-claude-haiku-4-5) (independent) — price gap
- Released October 2025; everything here is long-settled community consensus.
