# Exactly 2,910 saturated 14-point (4,5)-sets with h = 8 up to affine equivalence
CLAIM-TYPE: certificate (exhaustive enumeration with exact realization)
TYPE: certificate
STATUS: submitted
DEPENDS ON: K3-K6 [published]; K7 [published] (F7-free, imposed in the enumeration); K30 [verified-here] (monotone midpoints); K31-K33 [verified-here] (medial triangle and the forbidden cores with <= 4 edges, used as pre-filters: 159,110 of the 205,529 patterns were discarded by them without being realized; each core is a proved forced relation, independently re-derived in experiments/referee/catalogue-n8); K8 [published] (Henning-Yeo: for n=14, tau=6 it gives m >= 11; the case m = 11 is NOT covered by this certificate). The pipeline is the one certified in L002 (C DFS e757/c/ordered_dfs, prefix-split driver e757/ordered_dfs_split.py, exact realizer experiments/20261014-1005-census-dfs/fastreal.py, affine normalization as in L002).

## Statement
Up to affine equivalence there are exactly 2,910 sets $A\subset\mathbb{R}$ with $|A|=14$, $A$ a (4,5)-set, $h(A)=8=f(14)$ and $m=12$ three-term APs (saturated). Each is affinely rigid. $A_{\rm base}$ is one of them. (Whether non-saturated extremal 14-point sets, necessarily with $m=11$, exist is left open here; if none exists, 2,910 is the total number of extremal 14-point classes.)

## Proof
1. (Reduction.) As in L002: the AP pattern of a saturated 14-point (4,5)-set with $h=8$ is a class-O pattern (linear, $F_7$-free, injective midpoints, K30) on 14 vertices with 12 edges and $\alpha\le8$.
2. (Enumeration.) The prefix-split C DFS (depth-3 prefixes, 2,537 of them, one representative per reflection orbit) enumerates all such patterns: 205,529 up to reflection, 113,454,008,923 nodes, 277,501 CPU-seconds, resumable across five container restarts (per-prefix outputs with done-markers; experiments/20261014-1005-census-dfs/n14/results/n14_m12_TOTAL.json). The same split driver reproduces the certified n=12 count 2,226,490 (L002) exactly.
3. (Pre-filters and exact realization.) 119,844 patterns are medial-triangle-free (K31); 46,419 of those avoid every forbidden core with <= 4 edges; 34,995 avoid all 287 cores. The 46,419 survivors of the <= 4-edge filter were decided exactly by fastreal.py (fallback to realize_exact used 0 times): 2,910 realizable (all pass the full core library; all rigid by the M-matrix argument of L002); the rest fail exactly (order-infeasible 41,751 + 11,378 excluded by a longer core; forced repeated difference 846 + 13; forced extra AP 912 + ...; see summary.json). Every realized set re-checked: (4,5), AP pattern equal to the stored edges, $h=8$.
4. (Classes.) Rigid realizable patterns up to reflection correspond one-to-one to affine classes: 2,910. A_base's pattern and affine class are among them. The frozen judge passed 50/50 random sets (PASS NO-IMPROVEMENT, h=8).

## Computer-verified steps
experiments/20261014-1005-census-dfs/ (README.md: commands; n14/results/n14_m12_TOTAL.json; n14/results/post/summary.json, filter_counts.json, judge_spotcheck.txt; postprocess.py). Engine e757/c/ordered_dfs.c (commit d2f70f5 plus the prefix-split option), driver e757/ordered_dfs_split.py, tests/test_census_counts.py.

## Sanity checks
f(14)=8 (K24); A_base recovered; no class with h<8.

## Falsifier report
Not applicable (exhaustive enumeration); independent verification requested from the referee.
