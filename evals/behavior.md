# Behavior checks (run by hand after changing SKILL.md or pick-by-job.md)

Ask each in a fresh agent session with the skill installed. Each must pass every bullet.

1. "I need to migrate 400k lines and also have a model live in the browser for QA."
   - Opus 5.5 (or Fable 5.1) for the migration, GPT-6 Astra for browser QA, with reasons.
   - Offers a cheap worker option with its caveat (GLM-5.3: supervise wrong-hypothesis loops).
   - Quotes a data-as-of date. Invents no numbers.
2. "Just give me the leaderboard."
   - Quotes rows from tables/coding-agents.md with the date and source; no ranking from memory.
3. "Is Claude Mythos good?"
   - Says it is not covered (gated model) instead of guessing.
4. "Best open-weights coder I can self-host?"
   - Names candidates from pick-by-job, mentions custom licences (Kimi, GLM).
5. "Cheapest setup that's still decent for coding?"
   - Uses the "Best score for the money" section, names agent + model + effort, and warns that the cheapest rows score much lower on Terminal-Bench.
