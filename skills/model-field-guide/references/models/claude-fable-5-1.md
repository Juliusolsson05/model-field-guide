---
id: claude-fable-5-1
display: Claude Fable 5.1
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# Claude Fable 5.1 — the hard-problem specialist

**Feel:** The model you hand the scary, long, ambiguous job to and walk away from for an hour — at a premium price.

**Shines:**
- Hardest long-horizon engineering: reviewers found it makes messy half-migrated systems coherent and simplifies code (Every, Zvi).
- Delegated knowledge work (decks, research write-ups) that comes back finished (Every).
- Top of independent knowledge-work evals such as GDPval-AA at launch (reported by Decrypt/AA).
- Orchestrates subagents well, delegating bounded lanes to cheaper Claude models.

**Falls over:**
- Slow and expensive; with free rein it burns far more tokens than Fable 5 (Zvi's readers report a big jump).
- Security and biology requests can be silently rerouted to another model by safety classifiers (cyber → Opus 4.8); false positives reported, especially in subagents (Claude Code issues).
- Given long source documents and room to elaborate, it can over-produce and invent (Every's quote-extraction example).
- Overshoots explicit limits; spawns many subagents at high effort.

**Reach for it when:** the task is genuinely hard, long-horizon, and worth paying for; architecture rework; unattended multi-hour runs.

**Avoid when:** security research, exploit or bio work (classifier handoff); cost-sensitive loops; tight-brief extraction where fidelity matters more than insight — Opus 5.5 is now close enough for most coding.

**Effort:** `high` as the default for substantial work, `medium` for cheaper passes, `xhigh`/`max` only when the problem justifies it (community consensus summarized by Zvi).

**Evidence:**
- [Every vibe check](https://every.to/vibe-check/fable-5-1-vibe-check) (independent)
- [Zvi — Mythos 5.1 and Fable 5.1: Capabilities](https://thezvi.substack.com/p/claude-mythos-51-and-fable-51-capabilities) (independent)
- [Claude Code issue #91923](https://github.com/anthropics/claude-code/issues/91923) (independent, user report) — subagent model switch
- [Decrypt on Grok 4.7](https://decrypt.co/378824/xai-launches-grok-4-7) (independent) — Fable leading GDPval-AA
