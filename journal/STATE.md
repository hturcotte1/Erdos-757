# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-14 00:15
Phase/track: Phase 1 (exact engines, census) -> f(16) decision; Track U1 annealing in background
Clock: journal/START_TIME_UTC = 2026-10-13T23:06:40Z; budget 72 h (GOAL.md)

## Best verified results
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]
- Lower: c* >= 9/17 [published, Ma-Tang 2026 via Henning-Yeo 2021]
- Exact f(n) for n <= 15, n = 17 (START_HERE section 5) [derived-here]
- K30 monotone midpoints, K31 no medial triangle [verified-here] (kb/known_results.md)
- Census of ordered midpoint patterns n<=7 with 44 minimal forbidden cores [verified-here] (K32)
- Abstract constant c_hyp(n) (ordered, linear, F7-free, no K30/K31) = f(n) for n=5..15 [verified-here, n=13..15 modulo HY]
  (experiments/20261013-2257-chyp-table/table.md)

## Running jobs / agents
- CP-SAT worker (resumed): adding K30/K31/core clauses to e757/cpsat_model.py; n=16 T=9 decision (m=13, m=14);
  sweep n=18,20,22,23,25 -> experiments/20261014-0030-n16-decision, experiments/20261014-0030-feasible-sizes
- Workflow wf_4cc1d757-a61: n=8 forbidden library + catalogue (experiments/20261014-0005-forbidden-n8);
  independent DFS engine e757/ordered_dfs.py (+C) for certificates (experiments/20261014-0005-ordered-dfs); each verified.
- Annealer n=16/18 (experiments/20261013-2257-anneal16/best.json): best exact h = 10 at n=16, 11 at n=18; no alpha<=9 state ever.

## Live hypotheses
- [heuristic] Realizability is not the bottleneck at n=16 (21% of random linear saturated maps are (4,5)-sets); alpha is.
- [conjecture] c_hyp(16) with K30 = 10, i.e. f(16) = 10. If so, the ordered class O' may beat 9/17 asymptotically -> abstract Track L theorem.
- [heuristic] Transversal reformulation: tau = min set T such that every midpoint j is in T or has a parent l(j) or r(j) in T (parent maps l<j<r; G_L, G_R are rooted forests).

## Next 3 actions
1. Read the n=16 decision; if UNSAT, certify f(16)=10 with the independent DFS (verify-claim skill, certificate type C). If SAT, realize all solutions exactly.
2. From the sweep n=18..25, mark each size as abstractly impossible (dead end for Track U at that n) or list candidates.
3. Track L block: use the n<=8 catalogue and the forbidden cores to design a discharging/deficiency inequality; falsify first.
