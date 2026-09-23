---
id: muse-spark-1.3
display: Muse Spark 1.3
reviewed: 2026-09-22
review_by: 2026-10-22
status: settled
superseded_by: null
---
# Muse Spark 1.3 — Meta's value frontier model

**Feel:** Frontier-adjacent at a very low cost per task — as long as you use the tier you can actually get.

**Shines:**
- Cost per task: the broadly available `xhigh` configuration was measured by AA as among the cheapest per task at its intelligence level (via VentureBeat).
- Longer tool-based work in one thread; Meta reports fewer tool calls and tokens than 1.2 (vendor).
- 1M context; ships in Muse Code and the Meta Model API.

**Falls over:**
- The headline results come from a `max` configuration still in safety testing and not broadly available.
- Gap between `xhigh` and `max` is small on some evals but large on computer use (OSWorld 2.0), per VentureBeat.
- Per-token price unchanged but agentic tasks consume more input, so per-task cost rose versus 1.2.
- Meta ships a new Muse Spark roughly monthly; notes age fast.

**Reach for it when:** cost-sensitive agentic or research work where you'd otherwise pick GPT-6 Sol or Gemini Flash, and you can test on your own tasks.

**Avoid when:** you need computer use (the gap to `max` is large); you need an ecosystem of mature integrations.

**Effort:** `xhigh` is the generally available setting; don't quote `max` scores as if you can deploy them.

**Evidence:**
- [Meta AI Research launch post](https://research.meta.ai/blog/introducing-muse-spark-1-3) (vendor)
- [VentureBeat: best results from a model developers can't use yet](https://venturebeat.com/technology/meta-says-muse-spark-1-3-has-frontier-performance-but-its-best-results-come-from-a-model-developers-cant-broadly-use-yet) (independent)
- [Artificial Analysis article](https://artificialanalysis.ai/articles/muse-spark-1-3) (independent; link only)
- API id `muse-spark-1.3` is UNVERIFIED — check `pipeline/models.yaml`.
