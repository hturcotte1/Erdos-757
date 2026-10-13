# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-13 23:05
Phase/track: Phase 0 -> Phase 1 (engines + census); Track U1 annealing started in background
Clock: journal/START_TIME_UTC (created by the first `bash scripts/status.sh`); budget is in GOAL.md

## Best verified results
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]
- Lower: c* >= 9/17 [published, Ma-Tang 2026 via Henning-Yeo 2021]
- Exact f(n) for n <= 15, n = 17 (START_HERE section 5) [derived-here]

## Running jobs / dispatched subagents (2026-10-13 23:00)
- worker: e757/cpsat_model.py (ordered-midpoint CP-SAT, lazy alpha cuts) + c_hyp(n) table, experiments/20261013-2257-chyp-table/
- worker: e757/realizability.py (exact order LP + Farkas certificates, forced-relation detection, IIS) + forbidden library n<=7, experiments/20261013-2257-forbidden-library/
- worker: e757/anneal.py + long annealing job at n=16 (h<=9), experiments/20261013-2257-anneal16/ (best.json, logs/)
- scout: digests of Gyarfas-Lehel 1995 and Henning-Yeo papers into kb/notes/; novelty baseline review

## Live hypotheses
- [conjecture] c_hyp(16) (abstract ordered-midpoint class) may already be 10; if so f(16)=10 follows abstractly.
- [heuristic] realizability failures for saturated linear maps are mostly order/coincidence, rarely (4,5); alpha is the bottleneck.

## Next 3 actions
1. Read subagent summaries; combine cpsat_model + realizability into the n=16 CEGAR decision procedure (Q1).
2. From the c_hyp table decide whether arithmetic is needed (Q5); start Track L design from HY proof structure.
3. Checkpoint (e757-checkpoint skill), then first Track L block: falsifier on candidate inequalities.
