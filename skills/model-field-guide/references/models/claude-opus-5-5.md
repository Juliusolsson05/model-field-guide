---
id: claude-opus-5-5
display: Claude Opus 5.5
reviewed: 2026-09-22
review_by: 2026-10-06
status: provisional
superseded_by: null
---
# Claude Opus 5.5 — the default serious coder

**Feel:** Fable-class work at Opus prices, with a much more readable voice than Opus 5 — but it will happily keep going until you stop it.

**Shines:**
- Clean, idiomatic code that follows instructions; early testers put it close to Fable 5.1 on most coding work (Every, Willison).
- Communication: the stiff Opus 5 register is gone; prose reads easily.
- Token efficiency per task is good at sane effort levels, which is where the price cut actually lands.
- Iterative, visual and prototyping work; Every liked it more than Astra/Sol for this.

**Falls over:**
- At `max` effort it can deliberate until it exhausts its output budget on trivial prompts and return nothing (Willison's SVG test).
- Unconstrained runs burn tokens; poor at deadline-bound deliverables — it adds extras instead of shipping the thing asked for (Every).
- Buries the main point in long answers; its self-review is not trustworthy on its own.
- API behavior changed from Opus 5 (thinking always on, forced `tool_choice` rejected, inter-tool text arrives as thinking) — harnesses that parse text between tool calls need updating. Vendor docs are the source of truth.

**Reach for it when:** big-repo coding, migrations, code review, lead agent in a multi-worker setup, anything you'd have given Fable 5.1 but want cheaper.

**Avoid when:** you need a hard stop on time/tokens and can't enforce one externally; trivial prompts at `max`; pure bulk work (use Luna/Haiku-class models).

**Effort:** `medium` for routine work, `high`/`xhigh` for hard coding and writing (Every's recommendation). Avoid `max` unless you set an explicit output budget.

**Evidence:**
- [Anthropic launch post](https://www.anthropic.com/claude-opus-5-5) (vendor)
- [Simon Willison, 2026-09-22](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/) (independent) — max-effort failure, made it a Claude Code default
- [Every vibe check](https://every.to/vibe-check/vibe-check-opus-5-5-is-pulling-our-codex-converts-back-to-claude) (independent) — strengths, deadline/runaway weaknesses, effort advice
- Launch-day only: expect this file to change after two weeks of real use.
