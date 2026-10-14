# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-14 10:05
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
- Sweep (realizability-CEGAR witness mode, 1 h/size, 3 workers): n=18 UNKNOWN; n=20 running; then 22, 23, 25 (experiments/20261014-0030-feasible-sizes/results).
- Census chain: (12,10) partial: 30,559 abstract / 3,980 realizable classes (K40); (14,12) running (2 h limit), then (15,13) (experiments/20261014-0610-extremal-census).
- worker (new): exhaustive (12,10) census with the C DFS engine (e757/c/ordered_dfs) + K31/cores filter + exact realization; (14,12) attempt.
- DONE: L001 ACCEPTED (K13 verified); K30-K40; GL-tight lemmas (falsifier clean); inductive fit (K39); Q8 abstract failure (K38).

## Live hypotheses
- [heuristic] Realizability is not the bottleneck at n=16 (21% of random linear saturated maps are (4,5)-sets); alpha is.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17; HY = ceil(n/2)+1 up to n=23. Trivial GL bound tight at even n<=14. Two live hypotheses: (H1) HY stays tight at even n up to 22 (records at 16..22, c* <= 6/11) vs (H2) a wall at n=16 (f(16)=10, consistent with c*=4/7 and Q8). n=16 decides.
- [verified-here] Q8 holds on all realizable data (K34) but FAILS for the abstract class O even with K30/K31/<=4-edge cores (K38); every abstract violator contains a >=5-edge core. So c*=4/7 (if true) needs the deep forbidden configurations. Framework: kb/methods/trackL_inductive_framework.md.
- [heuristic] Three independent methods (CP-SAT, glucose/cadical, annealing) never found an abstract alpha<=9 hypergraph at n=16, while n<=14 witnesses are found in seconds: the abstract class probably has none (f(16)=10), but no certificate is reachable with SAT in this run (D15).
- [heuristic] Transversal reformulation: tau = min set T such that every midpoint j is in T or has a parent l(j) or r(j) in T (parent maps l<j<r; G_L, G_R are rooted forests).

## Next 3 actions
1. Exact counts: exhaustive (12,10) abstract/realizable census (DFS); (14,12) if feasible. Record as verified counts.
2. Harvest sweep outcomes (n=20..25) and the (14,12)/(15,13) census streams; update FINAL_REPORT.
3. Track L: only if a concrete discharge idea for the (3,0,0) type with 5/6-edge cores appears; otherwise keep gathering exact structure data. Checkpoint every 2 h.
