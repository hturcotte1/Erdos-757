# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-14 17:20
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
- (14,12,alpha<=8) exact census: prefix-split C DFS, now 4 workers (relaunched 17:05; 235+/2537 prefixes done; resumable: README command); then postprocess.py -> certificate L004.
- referee: L003 (saturated extremal counts n=6..11: 1, 4, 66, 1262, 6644, 466961; infinite non-saturated families for n<=11).
- scout: novelty check of the census results (OEIS, arXiv) -> results/reviews/L002-*__scout__*.md.
- DONE: L001 ACCEPTED (K13), L002 ACCEPTED (K41: 54,243 twelve-point extremal sets; f(12)>=7 without HY), K30-K43; Track U closed (D15: n=16 undecidable with our tools; sweeps n=18..25 UNKNOWN).

## Live hypotheses
- [heuristic] Realizability is not the bottleneck at n=16 (21% of random linear saturated maps are (4,5)-sets); alpha is.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17; HY = ceil(n/2)+1 up to n=23. Trivial GL bound tight at even n<=14. Two live hypotheses: (H1) HY stays tight at even n up to 22 (records at 16..22, c* <= 6/11) vs (H2) a wall at n=16 (f(16)=10, consistent with c*=4/7 and Q8). n=16 decides.
- [verified-here] Q8 holds on all realizable data (K34) but FAILS for the abstract class O even with K30/K31/<=4-edge cores (K38); every abstract violator contains a >=5-edge core. So c*=4/7 (if true) needs the deep forbidden configurations. Framework: kb/methods/trackL_inductive_framework.md.
- [heuristic] Three independent methods (CP-SAT, glucose/cadical, annealing) never found an abstract alpha<=9 hypergraph at n=16, while n<=14 witnesses are found in seconds: the abstract class probably has none (f(16)=10), but no certificate is reachable with SAT in this run (D15).
- [heuristic] Transversal reformulation: tau = min set T such that every midpoint j is in T or has a parent l(j) or r(j) in T (parent maps l<j<r; G_L, G_R are rooted forests).

## Next 3 actions
1. L003 verdict -> LEDGER; novelty note into FINAL_REPORT.
2. When the n=14 census completes: postprocess, certificate L004 (exact number of 14-point extremal sets), referee.
3. Keep FINAL_REPORT current; checkpoint every 2-3 h; budget end 2026-10-16 23:06 UTC (clause C).
