---
id: kimi-k3
display: Kimi K3
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# Kimi K3 — the open-weights front-end builder

**Feel:** The biggest open model ever, great at pretty web UIs, shaky once the repo gets big.

**Shines:**
- Frontend/web UI: #1 in Frontend Code Arena at launch (Lambert).
- Strongest open-weights model at its July launch by broad agreement; weights public since 2026-07-27.
- Simple coding tasks: close to Opus 4.8 in hands-on testing (MindStudio).

**Falls over:**
- Large codebases: Semgrep found its security-scan quality collapsed on their largest enterprise-style repo despite competitive aggregates.
- Trap-designed complex tasks: failed far more often than Opus 4.8 in independent testing (roughly a third of trap tasks).
- 2.8T parameters — self-hosting is a serious infrastructure project.
- Custom license terms (not plain MIT/Apache); read before commercial self-hosting.

**Reach for it when:** frontend/UI generation, landing pages, component work; open-weights needs where you can afford the hardware.

**Avoid when:** large-repo coding, security review at scale, tricky multi-step work without supervision.

**Effort:** low / high / max (per models.dev seed data).

**Evidence:**
- [Nathan Lambert, Interconnects](https://www.interconnects.ai/p/kimi-k3-the-open-weights-escalation) (independent)
- [Semgrep: strong on paper, weak on precision](https://semgrep.dev/blog/2026/kimi-k3s-code-security-results-lack-precision/) (independent)
- [MindStudio real-world coding review](https://www.mindstudio.ai/blog/kimi-k3-real-world-coding-review) (independent) — trap-task failure rate
