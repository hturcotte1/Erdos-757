RESULT: COUNTEREXAMPLE

# Q8 on ABSTRACT ordered midpoint hypergraphs: 7 tau(K) <= 3|R| + 2 e_2 + 4 e_1

Tags: [verified-here] for exact counts; NONE-FOUND parts are [heuristic] evidence only.

## Statement tested
Q8 for abstract hypergraphs (not necessarily realizable), D independent, R = V \ D, K = minimal traces e \ D, plus the
special case tau(H) <= 3n/7 (D empty). Class O = linear, F7-free, each j the midpoint of at most one edge.
O'(full) = O + K30 + K31 + all 287 forbidden cores in data/forbidden_ordered_n{7,8}.json.

## Counterexample (exact; `counterexample.json`, verified by independent Python brute force in `verify.py`)
n = 12, edges (i<j<k, j midpoint):
[0,1,10] [0,2,11] [1,3,5] [1,4,7] [3,6,9] [3,7,10] [4,5,6] [4,9,10] [6,10,11] [7,8,9]; D = {2,8} (independent).
Traces K: 8 triples [0,1,10] [1,3,5] [1,4,7] [3,6,9] [3,7,10] [4,5,6] [4,9,10] [6,10,11] and 2 pairs [0,11], [7,9].
tau(K) = 5, |R| = 10, e_1 = 0, e_2 = 2: 7*5 = 35 > 3*10 + 2*2 = 34.
Class: in O, and satisfies K30, K31 and every core with <= 4 edges (it is a member of the census stream, which imposes
core_max_edges=4), but it VIOLATES a 6-edge core (diff core on vertices 1,3,4,5,6,7,9,10) so it is NOT in O'(full).
It is not realizable (`realize_exact`: order-infeasible / forced extra AP).
Hence: Q8 is FALSE on abstract O (and on O + K30 + K31 + small cores), but this is not a counterexample for O'(full).
Same-class counterexamples: 60 distinct hypergraphs among the first 18,180 census solutions (n=12, m=10, alpha<=7), each
with a violating D of size 2 (slack -1: e2=2, e3=8, tau=5, R=10). All 60 were run through `realize_exact` (all
non-realizable) and `has_core` (all violate a full core). List: `violations_step1.json`.

## Scope and results
1. Census `experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl`: 18,180 hypergraphs (snapshot; the
   stream was still growing, 25,484 at the end), all independent D with |D|<=2 (1,436,220 states): 60 violations (above),
   4,980 equalities. Random 300 hypergraphs, ALL 3^12 deletion/avoidance states (115.4M states): 1 hypergraph with a
   violation (index 17976, D={0,11}, slack -1; violates a full core), 5.4M equalities. (`step1.py`, `step1b.py`)
2. `witnesses.json`, all 57 `op` and 46 `real` witnesses: n<=12 all 3^n states, n=13,14 all |D|<=3: 10.3M states, 0 violations,
   min slack 0. (`step2.py`)
3. Fresh enumeration with `enumerate_solutions` (limit 300, 300 s, solver-order so clustered, not random): class O at
   (10,8,6),(11,9,7),(12,10,7),(13,11,8): 300 each, LIMIT, 0 violations (n<=12 all 3^n states, n=13 |D|<=3); (14,12,8):
   TIMEOUT, only 14 solutions (not tested beyond that file, see gen_O_14_12_8_s0.json). Class O' (full cores): TIMEOUT
   with 179/45/7 solutions at n=10/11/12, 0 violations; n=13,14 not produced in the time. (`step3_gen.py`, `step3_test.py`)
4. tau <= 3n/7 (D empty), abstract: feasible_alpha_le(14, 7, class O, forbid_f7, 300 s, 2 workers, machine loaded) returned
   UNKNOWN (timeout), not UNSAT as hoped; (n=16, T=9) also UNKNOWN (300 s). Heuristic only. By Henning-Yeo (17*7 = 119 > 5*14 + 3*12 = 106)
   no n=14 hypergraph with tau=7 exists in O, so this special case is not threatened. Never violated in any data.

## Q8 slack distribution at D empty (3n + 0 - 7 tau)
Census (12,10,alpha<=7), all 25,484 hypergraphs: slack = 1 exactly (tau = 5; 3*12-35 = 1), never 0 or negative.
Generated O: (10,8,6): slack 2 (300/300); (11,9,7): 5; (12,10,7): 1; (13,11,8): 4. Slack 0 at D empty needs n=14, tau=6
(A_base: 94,544 equality states overall in the realizable data); not reached in abstract O data here.
Hence at D empty Q8 is tight only at (14,12,6) among all data; the abstract failure is entirely at |D|>=1 with pairs.

## Conclusion
Q8 as an inductive statement for the abstract class O is refuted; its truth for O'(full) or for realizable sets is untested
beyond these data (no violation found there). Evidence that realizability/cores beyond 4-edge cores matter: every
violation violates a 6-edge core and is non-realizable.

Note: `classify_all.py` (full-core classification of the whole census, to count how many census members lie in O'(full))
had not finished when this report was written; no result from it is claimed. An earlier 200-hypergraph test: 156/200 pass the full cores.
