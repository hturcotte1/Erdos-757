# Exactly 54,243 twelve-point (4,5)-sets with h = 7 up to affine equivalence
CLAIM-TYPE: certificate (exhaustive enumeration with exact realization)
TYPE: certificate
STATUS: submitted
DEPENDS ON: K8 [published] (Henning–Yeo: 17 tau <= 5n + 3m for linear F7-free 3-uniform H); K4-K7 [published] (h = alpha of the AP hypergraph; injective midpoints; linearity; F7-freeness); K30 [verified-here] (monotone midpoints, one-line proof); K31 [verified-here] (medial triangle forbidden; used only as a filter, not for completeness); the forbidden cores (K32-K33) are used only as a pre-filter whose rejections are re-confirmed by exact realization failing on the same pattern class... see Step 3.

## Statement
Up to affine equivalence (translation, scaling, reflection) there are exactly 54,243 sets $A\subset\mathbb{R}$ with $|A|=12$ that are (4,5)-sets with largest Sidon subset of size $h(A)=7=f(12)$. Each has exactly $m=10$ three-term APs and is affinely rigid (determined by its AP pattern).

## Proof
1. (Reduction to patterns.) For a 12-point (4,5)-set with $h=7$: $\tau=5$ and K8 gives $85\le60+3m$, so $m\ge9$; K5 gives $m\le10$. Its AP pattern in rank order is an ordered midpoint hypergraph that is linear (K6), $F_7$-free (K7), has injective midpoints (K5) and satisfies K30. Class O := all such patterns.
2. (Enumeration.) The exact C DFS `e757/c/ordered_dfs` enumerates every pattern of class O on 12 vertices with exactly $m$ edges and $\alpha\le7$: for $m=10$ it finds 2,226,490 labelled patterns (187M nodes, 288 s), 1,113,245 up to reflection; for $m=9$ it finds 0 patterns (425M nodes, 607 s). Cross-check: all 30,559 patterns found independently by CP-SAT native enumeration (experiments/20261014-0610-extremal-census) occur in the DFS output.
3. (Filters and exact realization.) 754,235 of the 1,113,245 patterns are free of medial triangles (K31) and 395,039 of those avoid every forbidden core with at most 4 edges; the discarded patterns are not realizable by K31/K32-K33 (each core is a proved forced relation). Every one of the 395,039 remaining patterns is decided by `e757.realizability.realize_exact` (exact rational arithmetic): 54,243 are realizable (all rigid since $m=n-2$; each realization checked to be a (4,5)-set with exactly this AP pattern and $h=7$); the rest fail exactly (321,304 order-infeasible, 10,803 forced extra AP, 8,689 forced repeated difference).
4. (Counting classes.) Realizable patterns are affine invariants of their (rigid) realizations, and reflection has been quotiented out, so the 54,243 realizable patterns are in bijection with the affine classes of 12-point (4,5)-sets with $h=7$. The five previously known sets (data/small_records.json '12', the two omega sets, the third set of START_HERE §6; three of them inequivalent) are among the classes. The frozen judge passed 50 random sets (PASS NO-IMPROVEMENT, h=7).

## Computer-verified steps
experiments/20261014-1005-census-dfs/ (README.md with commands and timings; results/); e757/c/ordered_dfs.c; e757/realizability.py; tests/test_census_counts.py (DFS and CP-SAT enumeration agree on (9,7,alpha<=6) and (10,8,alpha<=6)).

## Sanity checks
f(12)=7 [derived-here, K24]; the three inequivalent known 12-point sets are recovered; no class has h<7 (impossible by HY) and none has h>7 by construction.

## Falsifier report
Not applicable (exhaustive enumeration); the CP-SAT cross-check (30,559 of 30,559 found) plays that role.
