# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-14 05:05
Phase/track: Phase 1 -> f(16) decision (relaunched after container restart 04:40 UTC); Track L design started
Clock: journal/START_TIME_UTC = 2026-10-13T23:06:40Z; budget 72 h (GOAL.md)

## Best verified results
- Upper: c* <= 4/7 via A_base, n=14, h=8 [published, Ma-Tang 2026]
- Lower: c* >= 9/17 [published, Ma-Tang 2026 via Henning-Yeo 2021]
- Exact f(n) for n <= 15, n = 17 (START_HERE section 5) [derived-here]
- K30 monotone midpoints, K31 no medial triangle [verified-here] (kb/known_results.md)
- Census of ordered midpoint patterns n<=7 with 44 minimal forbidden cores [verified-here] (K32)
- Abstract constant c_hyp(n) (ordered, linear, F7-free, no K30/K31) = f(n) for n=5..15 [verified-here, n=13..15 modulo HY]
  (experiments/20261013-2257-chyp-table/table.md)

## Running jobs / agents (relaunched 04:50 UTC; the container restarted at 04:40 and killed all jobs)
- CP-SAT worker: n=16 T=9 as a RESUMABLE case split (edge of vertex 1 x m in {13,14}) -> experiments/20261014-0450-n16-cases/results/*.json; then sweep n=18,20,22,23,25.
- worker: HY slack landscape of O' and realizable class, n<=14 -> experiments/20261014-0500-slack-landscape
- worker: independent recheck of the Q8 falsification -> experiments/referee/q8/report.md
- DONE: n=8 catalogue (ACCEPTED by verifier, K33); Q8 NONE-FOUND (experiments/falsify/q8-omega-inequality); LP fit (experiments/20261014-0020-lp-fit); DFS engine (small-n cross-check only; n=16 needs ~1e14 nodes).
- Annealer stopped (best h=10 at n=16 over 28k realizable sets).

## Live hypotheses
- [heuristic] Realizability is not the bottleneck at n=16 (21% of random linear saturated maps are (4,5)-sets); alpha is.
- [conjecture] c_hyp(16) with K30 = 10, i.e. f(16) = 10. If so, the ordered class O' may beat 9/17 asymptotically -> abstract Track L theorem.
- [community]+[heuristic] Q8 (7 tau(K) <= 3|R| + 2e_2 + 4e_1) survived ~570M states; with D empty it is h >= 4n/7, so all data is consistent with c* = 4/7 (which forces f(16)=10). Framework: kb/methods/trackL_inductive_framework.md.
- [heuristic] Transversal reformulation: tau = min set T such that every midpoint j is in T or has a parent l(j) or r(j) in T (parent maps l<j<r; G_L, G_R are rooted forests).

## Next 3 actions
1. n=16 case split: if all 30 cases UNSAT -> f(16)=10 modulo HY (certificate needs an independent encoding, e.g. pysat with a different alpha encoding, cross-checked at n<=12). If SAT -> realize exactly.
2. Slack landscape -> pick an intermediate Q8-type target (a,b,c,d) with 3/7 < b/a < 8/17; falsify; then prover attempt with the forbidden cores.
3. Checkpoint every 2 h (e757-checkpoint); all long jobs resumable.
