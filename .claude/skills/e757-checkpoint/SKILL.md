---
name: e757-checkpoint
description: Use every 2-3 hours of work, after any notable result, before switching tracks, and before a long background job. Saves state so a compaction, crash or restart loses nothing.
---

# Checkpoint

1. `bash scripts/jobs.sh`: note running jobs, and harvest finished ones into their experiment
   README.md.
2. Overwrite journal/STATE.md (keep it under 60 lines) with:
   - last updated (UTC) and the current phase/track;
   - best verified results (point to LEDGER rows);
   - running jobs (path, purpose, expected finish);
   - live hypotheses (tagged);
   - the next 3 concrete actions.
3. Append to journal/LOG.md:
   `## <UTC> <track> <title>`, then: tried / result / evidence path / decision.
4. If an approach died, add it to kb/dead_ends.md with evidence. If a reusable fact was verified,
   add it to kb/known_results.md with its test.
5. If e757/ changed: run `python3 -m pytest -q` and fix failures.
6. `git add -A && git commit -m "journal: checkpoint <short summary>" && git push`
   (use `git push -u origin HEAD` if there is no upstream).
7. Run `bash scripts/status.sh`.
