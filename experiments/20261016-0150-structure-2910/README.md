# Structural census of the 2,910 saturated extremal 14-point classes

Tag: [verified-here] (exact integer/bitmask computation on every class; no heuristics).

Feeds: K47 (kb/known_results.md; LEDGER row K47; results/FINAL_REPORT.md R10). Regression test: tests/test_structure_2910.py (test_three_classes_match_stored_rows re-runs three classes, indices 0, 1000 and 2440, and compares them with the stored rows; test_summary_distributions checks the stored summary distributions).

## Question
Descriptive statistics for the 2,910 affine classes of saturated (m=12) 14-point (4,5)-sets with h=8
(K45, `data/census_n14_m12_classes.jsonl.gz`): degrees, counts of maximum Sidon sets / minimum
transversals, symmetry, cut vertices, extremal 12-point subsets, Lemma 1 (gl_tight_structure.md),
span, and universal vertices (Lemma U1 / K46).

## Method
`stats.py`, single process. Vertices are rank indices 0..13. For each class:
- sanity: stored edges equal `ap_edges` of the stored set; `is_45_set`; alpha and tau.
- all 2^14 subsets are tested by numpy bitmask for independence (no edge inside) and for being a
  transversal (meets every edge). A max-closure (zeta) transform gives alpha of every induced sub-hypergraph,
  hence h of all 13- and 12-point subsets (h = alpha since the sets are weak Sidon).
- reflection: reflected edge set {(13-c,13-b,13-a)} compared with the edge set (the classes are rigid, so
  equal rank-order patterns <=> affinely equivalent to the mirror image). Also counts distinct
  canonical forms min(pattern, mirror pattern).
- cut vertex, weak: delete v from every edge (edges shrink) and test connectivity of the other 13 points;
  strong: delete v and all edges through it, test connectivity of the other 13 points.
- G_L (edges {l(j),j}) and G_R (edges {j,r(j)}): connectivity and bipartition class sizes.
- span: coordinates divided by the gcd (all gcds are 1); max coordinate = largest element with min 0.

Command (runtime 12.9 s wall, 1 core):
`nice -n 15 python3 experiments/20261016-0150-structure-2910/stats.py`
Output: `results.json` (`summary` + 2,910 per-class `rows`, incl. set, degree sequence, gaps).

## Results (all 2,910 classes)
Consistency: edges match set, `is_45_set` true, alpha = 8, no independent 9-set, tau = 6 (no transversal of size <6), G_L/G_R are spanning trees (saturated, connected): 2,910/2,910. The census patterns are all distinct up to reflection.

| quantity | distribution |
|---|---|
| max degree | 3: 700; 4: 2,210 (never 5, never <=2) |
| degree sequence | 3^8 2^6: 700; 4 3^6 2^7: 1,270 (A_base type); 4^2 3^4 2^8: 940 |
| degree-1 vertices | 0 in every class (min degree 2) |
| # maximum Sidon subsets (= # minimum transversals, complements) | 137: 141; 139: 700; 143: 569; 144: 560; 147: 472; 149: 253; 150: 215 (range 137..150) |
| mirror-symmetric classes | 0 (all 2,910 asymmetric; no two are mirror images) |
| cut vertices (weak: edges shrink) | none in all 2,910 |
| cut vertices (strong: incident edges deleted) | 0: 700; 1: 1,129; 2: 1,081 (an artefact: a degree-2 vertex pair of edges isolating a point); weak is the standard notion |
| 13-point subsets | h(A-p) = 8 for all 14 p, in every class |
| 12-point subsets | h(A-p-q) = 8 for all 91 pairs, in every class: **0 classes** contain an extremal 12-point subset (h=7) |
| Lemma 1 | G_L and G_R colour classes are {6,7} in 2,910/2,910 |
| vertices in every maximum Sidon subset | 0 in all 2,910 classes (Lemma U1 confirmed) |
| max coordinate (min 0, primitive) | min 314, median 790, max 3,960; A_base 1,056 |
| gap sequences | 2,910 distinct (also mod reversal) |

A_base (row index 2440 in results.json): degree sequence 4 3^6 2^7, 143 maximum Sidon subsets, no weak cut vertex,
asymmetric, no 12-point subset with h=7: agrees with START_HERE section 6.

## Conclusion
Every saturated extremal 14-point class is 2-connected-like (no weak cut vertex), has minimum degree 2 and
maximum degree 3 or 4 (K44 allows 5, never attained), has 137-150 maximum Sidon sets, is mirror-asymmetric
(so the 2,910 classes correspond to 5,820 labelled order-pattern/oriented sets), satisfies Lemma 1 exactly, and
has no vertex common to all maximum Sidon subsets. Notably none contains a 12-point (4,5)-set with h=7:
every 12-point subset already has h=8, so the saturated 14-point records do not arise by adding two points to a
12-point record (K48/L006 proves the same for every extremal 14-point set, including a non-saturated (14,11) one if one exists, Q11). Number of maximum Sidon sets equals the number of minimum transversals by complementation
(the table counts them independently, via the independent-set and the transversal bitmasks, and they agree).
