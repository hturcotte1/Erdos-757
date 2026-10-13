# GOAL (protected: the agent cannot edit this file)

BUDGET_HOURS: 72

`BUDGET_HOURS` is the hard stop. Edit it before launching (use 0.5 for a dry run). Elapsed time
counts from `journal/START_TIME_UTC`, which the first `bash scripts/status.sh` creates. Delete that
file to restart the clock.

## The /goal condition

In the Claude Code session, type `/goal ` and paste everything inside the box after it (it is
under the 4,000-character limit):

```text
Make verified progress on Erdős Problem #757 in this repository, following CLAUDE.md and kb/RESEARCH_PLAN.md. Base every verdict only on the most recent GOAL-STATUS block printed by running `bash scripts/status.sh` (a tool result in the conversation, not prose). The goal is met exactly when that block contains the line `GOAL_MET: YES`. The script computes that line itself. It requires judge_integrity OK, git clean and pushed, and one of: (A) upper_bound_success: YES, meaning a (4,5)-set judged `JUDGE: PASS NEW-RECORD` (largest Sidon subset below 4/7 of its size) whose latest referee review says `VERDICT: ACCEPT`; (B) lower_bound_success: YES, meaning a proof of c* >= r with r > 9/17 whose two latest referee reviews say `VERDICT: ACCEPT` and whose scout review says `NOVELTY: CLEAR`; or (C) budget_exhausted: YES together with final_report: present. Everything else is not met: plans, partial results, promising leads, ratios of 4/7 or more, unreviewed or rejected proofs, claims made in prose, `GOAL_MET: NO`, or a turn that ended without a fresh status block. When not met, say which clause is closest and tell Claude to continue the research plan, run real computations or proof work, and end the turn with `bash scripts/status.sh`. This goal is never impossible, because clause (C) is always reachable by continuing to work. Never return an impossible verdict.
```

## Why the condition is written this way

- The goal evaluator is a small model. It cannot run commands or read files, so it judges only
  what is in the conversation. The status script turns every success clause into one
  machine-computed line.
- An open problem could tempt the evaluator to call the goal "impossible", which would end the
  run. Clause (C) makes the condition always reachable, and the text says so explicitly.
- Every success path needs independent checking: the frozen judge for constructions, and
  referee/scout subagents for proofs.
