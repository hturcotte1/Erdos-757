# Exact counts of saturated extremal (4,5)-sets for n = 6..11 (and infinitude of the non-saturated families)
CLAIM-TYPE: certificate (exhaustive enumeration with exact realization)
TYPE: certificate
STATUS: ACCEPTED by referee round 3 (results/reviews/L003-census-small-n-extremal-sets__referee__20261014T213511Z.md); revised after rounds 1-2; editorial fixes after the round-3 ACCEPT (title qualified with 'saturated', tags and a 'not load-bearing' note on K24/K29, 'near the given realization'), per the round-3 Problems E1 to E3
DEPENDS ON: K3-K6 [published] ((4,5) implies weak Sidon; h = alpha of the AP hypergraph; injective midpoints never at the extremes, so m <= n-2; linearity); K7 [published] (F7-free; imposed in the enumeration); K30 [verified-here] (monotone midpoints); K31-K33 [verified-here] (medial triangle and the forbidden cores with <= 4 edges, used by the pipeline as pre-filters at n=11: 3,263,957 of the 4,935,851 canonical saturated patterns were discarded by them without being realized; the referee's unfiltered recount over all 2,195,189,896 K30 midpoint maps at n=11 confirms the same 466,961 classes, results/reviews/L003-*__referee__20261014T181449Z.md); K8 [published] (Henning-Yeo, used to skip m below its minimum at n=10, 11); K24 [derived-here] / K29 [verified-here] (f(6..11) = 4,5,5,6,6,7; not load-bearing: f(6..11) also follows from the published bound plus the sets found here). The pipeline is the one certified in L002.

## Statement
For n = 6, 7, 8, 9, 10, 11 the number of affine classes of SATURATED (m = n-2) n-point (4,5)-sets with h = f(n) is
1, 4, 66, 1,262, 6,644, 466,961 respectively. For every n in 6..11 there also exist realizable non-saturated extremal patterns (m < n-2). The AP equations of such a
pattern have rank <= m <= n-3, so its realizations form a family of positive dimension modulo x -> qx+t, and each such
pattern gives infinitely many affine classes. Hence, up to affine equivalence, the extremal n-point (4,5)-sets are:
- infinitely many for 4 <= n <= 11 (for n = 4, 5: {0,1,2,x} and {0,1,2,x,3x}, any real x > 4);
- exactly one for n = 1, 2, 3;
- exactly 54,243 for n = 12 (L002: every extremal pattern is saturated, none at m = 9), the smallest n >= 4 with finitely
  many affine classes.

## Proof
1. (Reduction.) As in L002: an n-point (4,5)-set with h = f(n) has an AP pattern in class O (linear, F7-free,
   injective midpoints, K30) with alpha <= f(n) and 1 <= m <= n-2.
2. (Enumeration.) For each n and each m from the Henning-Yeo minimum (K8) to n-2 (all m at n <= 9), the C DFS (e757/c/ordered_dfs; the prefix-split driver with P=1 only for (11,9)) enumerates all
   class-O patterns with exactly m edges and alpha <= f(n); counts (labelled and up to reflection) and the
   Henning-Yeo minimum m are in experiments/20261014-1430-small-counts/README.md and results/summary.json.
3. (Exact realization, saturated case.) For n <= 10 every saturated pattern is decided exactly (fastreal.py / realize_exact); at n = 11 the K31 and <= 4-edge-core pre-filters were applied first and the surviving patterns decided exactly (the discarded ones are unrealizable by K31-K33, and both referee rounds' unfiltered recounts confirm the count);
   realizable saturated patterns are rigid (L002, M-matrix argument) and, up to reflection, in bijection with the
   affine classes; each realized set re-checked to be a (4,5)-set with the stored AP pattern and h = f(n); judge
   spot checks: 20/20 per n over the realized sets (mostly non-saturated ones) and 50/50 saturated sets at n=11, m=9; the
   referees' own spot checks (12/12, 26/26) cover saturated sets at every n.
4. (Non-saturated case.) For each 6 <= n <= 11 at least one non-saturated pattern is realizable (exact counts for n <= 10;
   for n = 11 a sample of 300 patterns per m with 251/257/216 realizable at m = 6/7/8); a realizable pattern with
   m < n-2 has a solution space of dimension >= 1 after normalization, and a generic point near the given realization is again a
   (4,5)-set with the same pattern (the failing points lie on finitely many proper subspaces), so it yields infinitely
   many affine classes. The n=8 record set (m=5) is such a case; the n=10 record set is one of the 6,644 saturated classes.

## Computer-verified steps
experiments/20261014-1430-small-counts/ (README.md: commands, timings, per-(n,m) counts; results/summary.json);
tests/test_small_counts.py (re-derives n=8 and n=10 and checks the record sets are among the classes).

## Sanity checks
f(n) values K24/K29; the n=8 and n=10 record sets recovered; no class with h < f(n).

## Falsifier report
Not applicable (exhaustive enumeration); L002's independently verified pipeline.
