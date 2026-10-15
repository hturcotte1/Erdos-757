# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-15 23:45
Phase/track: Phase 1 censuses + Track U witness sweeps; Track L data-driven design (no proof idea yet)
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
- (14,11,alpha<=8) exhaustive DFS (4 workers, 3437 prefixes, resumable; relaunch: python3 -m e757.ordered_dfs_split 14 8 11 3 4 experiments/20261014-1005-census-dfs/n14m11dfs/results --refl --nice 10 --tag n14_m11): decides whether non-saturated extremal 14-point sets exist (Q11).
- Documentation pass DONE (experiments READMEs + index; kb audit applied to START_HERE, LEDGER, FINAL_REPORT). PR #1 open to main; merge ~T-2h.
- DONE: L001-L004 ACCEPTED (K13, K41, K43, K45); K30-K45; novelty CLEAR (K30/K31, L002/L003); Track U closed (D15-D21); Track L: no proof idea.

## Live hypotheses
- [heuristic] Realizability is not the bottleneck at n=16 (21% of random linear saturated maps are (4,5)-sets); alpha is.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17; HY = ceil(n/2)+1 up to n=23. Trivial GL bound tight at even n<=14. Two live hypotheses: (H1) HY stays tight at even n up to 22 (records at 16..22, c* <= 6/11) vs (H2) a wall at n=16 (f(16)=10, consistent with c*=4/7 and Q8). n=16 decides.
- [verified-here] Q8 holds on all realizable data (K34) but FAILS for the abstract class O even with K30/K31/<=4-edge cores (K38); every abstract violator contains a >=5-edge core. So c*=4/7 (if true) needs the deep forbidden configurations. Framework: kb/methods/trackL_inductive_framework.md.
- [heuristic] Three independent methods (CP-SAT, glucose/cadical, annealing) never found an abstract alpha<=9 hypergraph at n=16, while n<=14 witnesses are found in seconds: the abstract class probably has none (f(16)=10), but no certificate is reachable with SAT in this run (D15).
- [heuristic] Transversal reformulation: tau = min set T such that every midpoint j is in T or has a parent l(j) or r(j) in T (parent maps l<j<r; G_L, G_R are rooted forests).

## Next 3 actions
1. Documentation pass (workflow running): experiment READMEs, index READMEs, kb audit -> apply START_HERE/open_questions/known_results updates myself.
2. If the (14,11) DFS completes: realize its patterns, finalize the n=14 count in L004/K45/report. Keep re-arming the session waiter; relaunch after restarts.
3. T-2h (2026-10-16 ~21:00 UTC): final checkpoint, FINAL_REPORT final version, merge PR #1 into main, run status.sh.
