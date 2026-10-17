# The record cell (23,21,10): 23-point (4,5)-set with h = 13   RESULT: partial.  Degree-4 case EMPTY (no realizable pattern); maxdeg-3 case NOT decided.

[derived-here, computer-assisted; certified in part as L012 / K56 (results/proofs/L012-n23-record-no-degree-4.md; referee ACCEPT x3 on 2026-10-17: results/reviews/L012-n23-record-no-degree-4__referee__20261017T162634Z.md, __referee__20261017T172032Z.md, __referee__20261017T171553Z.md; scout NOVELTY: CLEAR): Theorems 1-3 there are the degree bound, the empty cells (23,19,10) and (23,20,10), and the 699 unrealizable degree-4 classes; the maximum-degree-3 case is open (Q14).]  Class C = linear, F7-free, e(S) <= |S|-2 on every subset (hereditary).  Assumed: HY; I11 on C for n <= 22 (L007-L011, ACCEPTED x3).
No realizable pattern found, so no RECORD_CANDIDATE.json and `new_claim.py` was not run.  This folder is committed (the large `out/` directory is git-ignored).

## 1. What I11 (n <= 22) gives for H = (23,21,10)  (confirms the coordinator's computation)
For every v: tau(H-v) in {9,10}; tau'=10 would need 110 <= 108-2d, false, so tau'=9 and slack(H-v) = 9-2d >= 0, d <= 4.  Sum of degrees 63 over 23 vertices, so max degree D in {3,4}
(D<=2 gives <=46).  D=4: delete a degree-4 vertex -> G=(22,17,9), slack 1 (maxdeg<=4; the 8 neighbours have G-degree <=3).  D=3: >=17 vertices of degree 3; delete one -> G=(22,18,9), slack 3.
Other 23-vertex cells with h=13: HY needs m>=19 and I11 (not proven at n=23) m>=21, so (23,19,10) and (23,20,10) are *violation* cells: (23,19,10) slack -3, deg<=2, sum deg 57>46: impossible;
(23,20,10) slack -1, deg<=3: route20 below: empty.

## 2. Engine (`engine.py`, `ext3.cpp`->`ext3d.cpp`, `parts.py`, `parts_bf.py`, `dedupe_fast.py`)
`cell(n,m,t,Delta)` = iso classes of connected F7-free e(S)-ok graphs (n,m), tau>=t (slack-determined), maxdeg<=Delta (3 or 4).  m<=10: direct DFS (`conn_dfs3`, maxdeg Delta).  Else: for each possible maximum degree d of X,
remove a max-degree vertex w; X-w has tau' = t-1 (or t if slack_X >= 3+2d), maxdeg<=d, components = connected cells *including isolated vertices (slack 3)* whose slack sums to slack(X-w); all component class
products are re-extended by w (`ext3d`: d disjoint pairs, endpoints of degree <= d-1, tau(X)>=t by min-cover killing, F7-free and Hall e(S)<=|S|-2 as pruning - valid because C is hereditary; connected results kept; iso dedupe by BLISS canonical form, igraph).
Partition lists: `parts.py` (slack-sum), verified against an independent brute force over (n_i,m_i,tau_i) (`parts_bf.py`, results_parts_check.json: (22,17,9;1) 4 partitions and (22,18,9;3) 5 partitions EQUAL, plus the earlier lists).
Validation of the engine: regression (14,12,6,D3)=2, (15,11,6,D3)=19, (17,13,7,D3)=6 classes (as in earlier folders, which used different code); for Delta=4: all 2,910 census classes of n=14 are isomorphic to one of
the 11 classes (14,12,6,D4), and all 54,243 realizable 12-point classes to one of the 221 classes (12,10,5,D4) (`consistency.py`).  ext3d: identical HIT sets to the first version on 3 graphs (1,836 hits); raw counts equal an independent numpy count
(d=3: 30 graphs 399=399 and 10 graphs 156=156; d=4: 2 graphs 778=778, `crosscheck_ext3.py`); reproduces the n=16 case counts (18 and 218 hits) of ext_vertex2.  (`ext3d` uses an incremental F7 test valid for F7-free inputs - all engine inputs are.)

## 3. Degree-4 case (route 4): G=(22,17,9), slack 1  [complete]
Partitions: [AP,(19,16,8)] [C10,(12,10,5)] [C14,(8,5,3)] [connected (22,17,9)].  Classes (Delta=4): (19,16,8) 956, (12,10,5) 221, C10 5, C14 11, (8,5,3) 2, connected (22,17,9) **95** (it needed the d=3 branch G'=(21,14,8) 299 classes and the d=4 branch G'=(21,13,8): connected (21,13,8,D4) has 0 classes).
2,178 graphs G (all non-isomorphic).  Re-insertion of a degree-4 vertex with tau>=10, F7-free, Hall-ok (two halves, 2 processes): 1,089 + 1,089 graphs, 4.4e9 + 6.2e9 kill nodes, 14,290 raw hits -> **699 isomorphism classes** of H (both halves give the same 699), 0 contain F7, all satisfy
e(S)<=|S|-2, all 699 admit an ordered injective midpoint labelling (SAT, `post.py`).
Exact realization (`realize_fast.py`, `finish_route.py`): since m = n-2 the AP system is rigid; for every injective assignment edge -> midpoint vertex (the two unmatched vertices are the extremes) solve x_j=(x_i+x_k)/2 and require distinct values and *exactly* the 21 edges as APs.
27,206,877 assignments over the 699 classes (per half; identical numbers in both runs), all systems solvable, 6,051,773 with distinct values, **0** with exactly the 21 APs (positive control: the A_base hypergraph gives 948 exact realizations from 1,596 assignments; minimal nonzero AP residual in a sample 8.5e-6 >> tolerance 1e-8).
=> **no 23-point (4,5)-set with h=13, m=21 and a point of AP-degree 4** (relative to the assumptions and code correctness).  Note that class C alone does NOT exclude it: 699 abstract patterns pass all hereditary filters and are only killed by realizability (every solution has extra APs).

## 4. (23,20,10)  (route20)  [complete]
deg<=3 (slack -1), G=(22,17,9) maxdeg<=3 (864 graphs from the same partitions), re-insertion of a degree-3 vertex with tau>=10: 84 finals, all killed by the Hall test: **empty**.

## 5. Maximum-degree-3 case (route 3): G=(22,18,9), slack 3  [NOT decided]
Partitions (5): [AP,(19,17,8)] [C14,(8,6,3)] [(21,18,9),isolated vertex] [(12,10,5),(10,8,4)] [connected (22,18,9)].  The big cells need further deletions that each raise the slack by 2 ((22,18,9)->(21,15,8) slack 5 ->(20,12,7) slack 7 ...), and the high-slack
cells are huge: (11,9,4,D3): 1,216 classes; (14,9,5,D3): 1,060; (15,12,6,D3): 10,617; (13,10,5,D3): 7.0M labelled graphs -> 6,683 classes (8 min); (14,10,5,D3): **57.9M labelled graphs** (5.4 GB, 646M DFS nodes) - and re-insertion products of such lists exceed 1e6 graphs.
A direct Knuth estimate for the ordered DFS (n=23, T=13, m=21, F7-free, maxdeg 3, reflection symmetry; 30 probes) gives ~2.5e24 +- 2e24 calls.  So the maxdeg-3 case (>=17 degree-3 vertices, sum deg 63) remains open here.  What remains: all 23-point saturated patterns with maximum degree exactly 3; a new idea (stronger hereditary filters such as K30/K31/cores inside the unordered engine, or an LP/realizability prune for near-saturated sub-patterns) is needed.

## For the referee
(1) the degree/slack derivation; (2) `parts.py` vs `parts_bf.py` lists for (22,17;1) and (22,18;3) and the engine's use of isolated vertices; (3) engine completeness: canonical-growth DFS, the d-vertex-removal argument (X-w has maxdeg<=d, endpoint degrees <= d-1), tau' in {t-1,t}; the consistency checks of Section 2; (4) `ext3d` (cover killing; F7/Hall pruning) and its cross-checks; (5) `realize_fast.py` (rigid saturated realization; the claim "all midpoint assignments" - injective maps edge->vertex with exactly two unmatched vertices - covers every realization of a saturated pattern up to reflection), tolerance 1e-8 vs minimal residual 8.5e-6.
Files: results.json, results_route4{a,b}_final.json, results_route20.json, results_parts_check.json, route4b.log (engine log of route 4), route4_stage1.log, route20.log, route3c.log, finish_route4{a,b}.log, out/ (hits, gz).
