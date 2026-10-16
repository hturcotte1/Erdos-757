# Inductive inequality fit: abstract vs realizable (Q8 family)

Question. For `a*tau(K) <= b|R| + c e_2 + d e_1` (a=1; Q8 = (3/7, 2/7, 4/7)), which (b,c,d) are consistent with
(A) ABSTRACT ordered hypergraphs (linear, F7-free, injective midpoints) and (B) REALIZABLE sets? What local
configurations survive the free moves (kb/methods/trackL_inductive_framework.md)?

## Method (all tuples exact: ints; LP optima exact in Fraction by vertex enumeration on the scipy-tight set, then re-verified)
- `tuples.c` = q8.c (falsifier, exact tau by branch and bound) modified to output the distinct tuples
  (tau(K), |R|, e2, e1) per hypergraph with one (S,D) example of minimal |D|. `common.py` wraps it. R = S \ D.
- Datasets (tag [verified-here] for counts):
  - REAL records: the 7 record sets (A_base, 2 omega 12-pt, rec8, rec10, rec11, rec12; rec14 = A_base), ALL 3^n (S,D) states
    (A_base: 3,253,568 valid states, 94,544 equalities, as in K34). REAL random: 300 saturated (4,5)-sets each at n=12, n=14
    (e757.anneal, seed 757), all independent D with |D|<=2.
  - ABS census: all 26,974 hypergraphs of experiments/20261014-0610-extremal-census/results/n12_m10_solutions.jsonl
    ((12,10,alpha<=7), core_max_edges=4), |D|<=2; ABS census500: 500 random of them, ALL independent D; ABS witnesses: 103
    (57 op + 46 real) from slack-landscape/witnesses.json, |D|<=2; ABS fresh: 200 each at (10,8,T=6),(11,9,7),(13,11,8) class O
    (`gen_fresh.py`, enumerate_solutions seed 1, solver order, so clustered not random), and class O' (K30, K31, all n<=8 cores;
    only 200/91/9 solutions within 300 s), |D|<=2.
  - Core status: `fastcores.has_core` (validated against constraint_violations) on a random sample of 6,413 census
    hypergraphs (incl. the 500): 4,898 (76%) pass the full library. (Full 26,974 classification not run: 0.13 s each, time budget.)
- Files: `fit.py` (tables), `lplib.py` (exact LP), `violators.py` (cores + local types), `fit_results.json`, `tables_fit.md`,
  `fit_output.txt`, `violators.json`, `local_types.json`, `*_tuples.jsonl.gz` (per hypergraph tuples with edges).
- Commands: `python3 build_realizable.py; python3 build_abstract.py {census,census_all500,witnesses,fresh}; python3 classify_census.py; python3 fit.py; python3 violators.py`.

## Results (full tables: tables_fit.md)
Minimal b ([verified-here] feasibility of the stated point on all tuples; optimality from exact vertex enumeration):

| dataset | min b, (c,d) fixed to Q8 = (2/7,4/7) | min b, c=2b/3, d=4b/3 | min b, c,d free in [0,2] |
|---|---|---|---|
| REAL records (all states) | 3/7 | 3/7 | 3/7 |
| REAL random n=12 / n=14 | 29/70 / 17/42 | 5/12 / 9/22 | 1/3 / 5/14 |
| ABS census (|D|<=2) and census500 (all D) | 31/70 = 0.4429 | 15/34 = 0.4412 | 5/12 |
| ABS witnesses, fresh O, fresh O' | 3/7 | 3/7 | 3/7, 2/5, 2/5 |
| ABS all | 31/70 | 15/34 | 3/7 |
| ABS census sample passing FULL cores (4,898) | 3/7 | 3/7 | 5/12 |
| ABS "O'-like" union (core-passing + op witnesses + fresh O') | 3/7 | 3/7 | 3/7 |

- The "c,d free in [0,2]" column is nearly vacuous (optimum has c=d=2, so only D=empty-type tuples bind: A_base gives 6/14=3/7);
  the informative columns are the fixed-(c,d) ones. [verified-here]
- Single violating tuple type in all abstract data: (tau,|R|,e2,e1) = (5,10,2,0): 35 > 34 (Q8 slack -1). It forces b >= 31/70 at
  (c,d)=(2/7,4/7). No violation of any kind in REAL (min slack 0; all 7 record sets, plus random sets with slack >= 1).
- Needed c,d at b=3/7: REAL records need c >= 2/7 (d free) and d >= 4/7 (c free): Q8 is a corner of the realizable feasible
  region (c=2/7 at d=4/7 exactly; at c=2/7 d>=4/7). Abstract (no core filter): c >= 5/14, and d=4/7 with c=2/7 impossible
  (infeasible for any d <= 2). Core-passing abstract: c >= 2/7, d >= 4/7 (census500), i.e. same as realizable.
- (b,c) tradeoff at d=4/7, minimal feasible c (exact): b = 3/7, 0.44, 0.45, 0.46, 8/17:
  - REAL records: 2/7, 6/25, 13/60, 31/150, 10/51 (0.286, 0.240, 0.217, 0.207, 0.196)
  - ABS all (incl. violators): 5/14, 3/10, 1/4, 43/200, 13/68 (0.357, 0.300, 0.250, 0.215, 0.191)
  - ABS O'-like union: 2/7, 6/25, 179/840, 141/700, 45/238 (0.286, 0.240, 0.213, 0.201, 0.189)
  Hence on abstract data a Q8-like inequality with (d=4/7) needs c=5/14 at b=3/7, and c=1/4 is enough only from b=0.45; the
  abstract-only excess disappears on the O'-like (core-passing) sets. [heuristic: finite samples]

## Violators vs the core library (task item 2) [verified-here]
- Across all abstract data (census all 26,974, census500, witnesses, fresh) there are 89 distinct hypergraphs having a Q8-violating
  state (all of type (5,10,2,0), |D|=2; the earlier snapshot had 60). Only ONE distinct violating tuple, so "20 tuples" do not exist;
  `violators.json` lists the hypergraphs (first 200) with their states.
- Survivors of the FULL core library (K30, K31 and all n<=8 forbidden cores): 0 of 89 (none violates K30/K31; all 89 violate a
  core, the smallest violated core has 5 edges for 19 of them and 6 for 70). So no abstract counterexample inside O' at n<=13 in
  this data (consistent with K38). Caveat: O' enumerations of fresh sets were tiny (200/91/9 solutions) and the census is only
  n=12, m=10.

## Free-move structure for (1, 3/7, 2/7, 4/7) (task item 3) [verified-here counts]
Vertex type = (e3(v), e2(v), e1(v)). Deletion is free iff 2e2+4e1 >= 4; avoidance is free iff e1 = 0 and e3+e2 <= 1.
Types neither deletable nor avoidable ("hard"): e1 = 0, e2 <= 1, e3+e2 >= 2, i.e. (2,0,0), (3,0,0), (4,0,0), ... , (1,1,0), (2,1,0), (3,1,0), ...
Observed hard types and counts (vertices of states with R nonempty):

| state family | states | irreducible states (all vertices hard) | (1,1,0) | (2,0,0) | (2,1,0) | (3,0,0) | (3,1,0) | (4,0,0) |
|---|---|---|---|---|---|---|---|---|
| abstract Q8-violators (slack -1), vertices | 91 (|R|=10) | 91 | 182 | 91 | 182 | 364 | 0 | 91 |
| abstract slack-0 example states, vertices in irreducible states | 8,617 | 7,478 (7,456 with |R|=11, i.e. the omega 12-pt D={v} pattern) | 6,991 | 26,037 | 8,008 | 38,016 | 1 | 3,153 |
| realizable: ALL equality states of the 7 records | 148,378 | 6 (|R|=8:2, 11:3, 14:1) | 2 | 22 | 12 | 25 | 0 | 2 |

- Every other vertex type in tight states is free ((0,0,1) singleton, (1,0,0) avoidable); 363,725 of 363,796 vertices of realizable
  tight states are (0,0,1).
- Take-away: in every irreducible state, the vertex types are exactly (3,0,0) ~40%, (2,0,0), (2,1,0), (1,1,0) ~10-20% each, (4,0,0) ~3-10%;
  abstract violators have the same type distribution as realizable irreducible tight states (violators: 40% (3,0,0), 20% (1,1,0), 20% (2,1,0),
  10% (2,0,0), 10% (4,0,0); realizable: 25/63, 2/63, 12/63, 22/63, 2/63). The local types therefore cannot separate abstract from realizable;
  the difference is global: irreducible tight states are generic in the abstract class (7,456 census hypergraphs have one with |R|=11)
  but occur in only 3 realizable states with |R|=11, plus A_base itself (|R|=14) and 2 at |R|=8.
  A discharging proof must handle (2,0,0),(3,0,0),(4,0,0),(1,1,0),(2,1,0),(3,1,0); (3,0,0) is the dominant type.

## Conclusion
- On realizable data Q8 is exactly the corner (b,c,d) = (3/7,2/7,4/7): no smaller b, c or d with the other two fixed is feasible (records),
  while random realizable sets are far from tight. [verified-here for the finite data; [heuristic] as a statement about all sets]
- The ABSTRACT class O (cores of <=4 edges) forces b >= 31/70 at the Q8 (c,d), through the single tuple (5,10,2,0); all 89 violating
  hypergraphs violate a core of 5-6 edges. The core-passing abstract sample reproduces the realizable region (b=3/7 OK). So a proof of
  Q8 cannot be arithmetic-free and cannot rely on cores of <=4 edges; it needs the 5- and 6-edge cores (see K38), which kill exactly the
  irreducible (5,10,2,0) states.
- Caveats: samples (census sample 6,413 of 26,974 for core status; fresh sets solver-clustered; O' fresh sets tiny); abstract data
  only n<=13; minimal b values are for these samples, not theorems.
