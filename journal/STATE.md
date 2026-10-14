# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-14 05:55
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

## Running jobs / agents
- CP-SAT worker: LAYERED n=16 search (deletion-of-max lemma: enumerate O' on 15 vertices with alpha<=9, m'=9..13, then extend by vertex 15) -> experiments/20261014-0550-n16-layered/ (resumable streams). Direct 30-case split abandoned (all cases TIMEOUT 3000 s).
- worker: independent pysat encoding of O' (e757/sat_indep.py) for the certificate + single-case timing.
- DONE: slack landscape n<=14 (experiments/20261014-0500-slack-landscape): tau_max(n,n-2) = n/2-1 at even n<=14 in O' AND realizable; realizable = O' in every resolved cell.
- DONE: Q8 confirmed (K34); n=8 catalogue (K33); LP fit; DFS engine (small-n cross-check only).

## Live hypotheses
- [heuristic] Realizability is not the bottleneck at n=16 (21% of random linear saturated maps are (4,5)-sets); alpha is.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17; HY = ceil(n/2)+1 up to n=23. Trivial GL bound tight at even n<=14. Two live hypotheses: (H1) HY stays tight at even n up to 22 (records at 16..22, c* <= 6/11) vs (H2) a wall at n=16 (f(16)=10, consistent with c*=4/7 and Q8). n=16 decides.
- [community]+[heuristic] Q8 (7 tau(K) <= 3|R| + 2e_2 + 4e_1) survived ~570M states; with D empty it is h >= 4n/7, so all data is consistent with c* = 4/7 (which forces f(16)=10). Framework: kb/methods/trackL_inductive_framework.md.
- [heuristic] Transversal reformulation: tau = min set T such that every midpoint j is in T or has a parent l(j) or r(j) in T (parent maps l<j<r; G_L, G_R are rooted forests).

## Next 3 actions
1. Layered n=16: read counts of 15-vertex extremal structures per m'; if small, finish the extension; realize every abstract n=16 solution exactly (record or f(16)=10).
2. Certificate path: pysat second encoding cross-checks the n=15 counts; then verify-claim (type C) for whatever n=16 yields.
3. Draft results/FINAL_REPORT.md as a living document at the next checkpoint; Track L target choice after n=16.
