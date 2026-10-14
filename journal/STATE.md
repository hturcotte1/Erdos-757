# STATE (overwrite at every checkpoint; keep under 60 lines)

Status: running
Last updated (UTC): 2026-10-14 07:00
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
- n=15 streams (class O', alpha<=9): m'=9, m'=10 no solution yet (UNSAT would give deg<=3 in any 16-point extremal H), m'=11 2,282+ solutions; 2 h limit ends ~08:00 (experiments/20261014-0550-n16-layered/results).
- Extremal census chain: (12,10,alpha<=7) >= 25,484 abstract solutions so far (3 known realizable classes); then (14,12), (15,13) (experiments/20261014-0610-extremal-census).
- worker: exact re-derivation of K13 (no 2-point extension of A_base reaches h=9) -> experiments/20261014-0640-abase-extensions.
- falsifier (background tail): full-core classification of the abstract Q8 violators.
- DONE this block: GL-tight structure lemmas (kb/notes/gl_tight_structure.md, falsifier NONE-FOUND); K35-K38; FINAL_REPORT living draft; D15-D16.

## Live hypotheses
- [heuristic] Realizability is not the bottleneck at n=16 (21% of random linear saturated maps are (4,5)-sets); alpha is.
- [verified-here] f(n) = ceil(n/2)+1 = HY bound for 6<=n<=15 and 17; HY = ceil(n/2)+1 up to n=23. Trivial GL bound tight at even n<=14. Two live hypotheses: (H1) HY stays tight at even n up to 22 (records at 16..22, c* <= 6/11) vs (H2) a wall at n=16 (f(16)=10, consistent with c*=4/7 and Q8). n=16 decides.
- [verified-here] Q8 holds on all realizable data (K34) but FAILS for the abstract class O even with K30/K31/<=4-edge cores (K38); every abstract violator contains a >=5-edge core. So c*=4/7 (if true) needs the deep forbidden configurations. Framework: kb/methods/trackL_inductive_framework.md.
- [heuristic] Three independent methods (CP-SAT, glucose/cadical, annealing) never found an abstract alpha<=9 hypergraph at n=16, while n<=14 witnesses are found in seconds: the abstract class probably has none (f(16)=10), but no certificate is reachable with SAT in this run (D15).
- [heuristic] Transversal reformulation: tau = min set T such that every midpoint j is in T or has a parent l(j) or r(j) in T (parent maps l<j<r; G_L, G_R are rooted forests).

## Next 3 actions
1. Harvest at ~08:00: m'=9/10 UNSAT? (-> degree bound lemma for 16-point extremal H), census counts at (12,10) and (14,12), extension certificate K13 -> [verified-here].
2. Track L: LP-fit the best inductive (a,b,c,d) on abstract vs realizable data to state exactly what is provable without cores; then decide whether a prover attempt on a weaker Q8-type target with cores is worth it.
3. Checkpoint every 2 h; keep FINAL_REPORT current; budget end 2026-10-16 23:06 UTC.
