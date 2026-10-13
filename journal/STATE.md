# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: not started
Last updated (UTC): -
Phase/track: Phase 0
Clock: journal/START_TIME_UTC (created by the first `bash scripts/status.sh`); budget is in GOAL.md

## Best verified results
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]
- Lower: c* >= 9/17 [published, Ma-Tang 2026 via Henning-Yeo 2021]

## Running jobs
- none

## Live hypotheses
- (none yet)

## Next 3 actions
1. Run `bash scripts/preflight.sh`; read kb/RESEARCH_PLAN.md and kb/dead_ends.md.
2. Phase 1, P1.1: census of realizable labeled AP hypergraphs for n <= 10.
3. Make the ordered search fast enough for n=16 (compiled core or CP-SAT), then decide f(16).
