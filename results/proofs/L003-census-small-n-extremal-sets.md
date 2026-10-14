# Exact counts of extremal (4,5)-sets for n = 6..11
CLAIM-TYPE: certificate (exhaustive enumeration with exact realization)
TYPE: certificate
STATUS: submitted
DEPENDS ON: K3-K6 [published] ((4,5) implies weak Sidon; h = alpha of the AP hypergraph; injective midpoints never at the extremes, so m <= n-2; linearity); K7 [published] (F7-free; imposed in the enumeration); K30 [verified-here] (monotone midpoints); K24/K29 [derived/verified-here] (f(6..11) = 4,5,5,6,6,7). The pipeline is the one certified in L002.

## Statement
For n = 6, 7, 8, 9, 10, 11 the number of affine classes of SATURATED (m = n-2) n-point (4,5)-sets with h = f(n) is
1, 4, 66, 1,262, 6,644, 466,961 respectively. For every n in 6..11 there also exist realizable non-saturated
extremal patterns (m < n-2; their solution spaces have positive dimension, so each gives infinitely many affine
classes of sets); hence the set of all extremal n-point (4,5)-sets is infinite for n <= 11, and n = 12 is the first
size at which it is finite (L002: 54,243, no pattern at m = 9).

## Proof
1. (Reduction.) As in L002: an n-point (4,5)-set with h = f(n) has an AP pattern in class O (linear, F7-free,
   injective midpoints, K30) with alpha <= f(n) and 1 <= m <= n-2.
2. (Enumeration.) For each n and each m, the C DFS (e757/c/ordered_dfs, prefix-split driver with P=1) enumerates all
   class-O patterns with exactly m edges and alpha <= f(n); counts (labelled and up to reflection) and the
   Henning-Yeo minimum m are in experiments/20261014-1430-small-counts/README.md and results/summary.json.
3. (Exact realization, saturated case.) Every saturated pattern is decided exactly (fastreal.py / realize_exact);
   realizable saturated patterns are rigid (L002, M-matrix argument) and, up to reflection, in bijection with the
   affine classes; each realized set re-checked to be a (4,5)-set with the stored AP pattern and h = f(n); judge
   spot check 20/20 for each n (50/50 at n=11, m=9).
4. (Non-saturated case.) For each n <= 11 at least one non-saturated pattern is realizable (exact counts for n <= 10;
   for n = 11 a sample of 300 patterns per m with 251/257/216 realizable at m = 6/7/8); a realizable pattern with
   m < n-2 has a solution space of dimension >= 1 after normalization, and a generic point of it is again a
   (4,5)-set with the same pattern (the failing points lie on finitely many hyperplanes), so it yields infinitely
   many affine classes. The n=8 record set (m=5) is such a case; the n=10 record set is one of the 6,644 saturated classes.

## Computer-verified steps
experiments/20261014-1430-small-counts/ (README.md: commands, timings, per-(n,m) counts; results/summary.json);
tests/test_small_counts.py (re-derives n=8 and n=10 and checks the record sets are among the classes).

## Sanity checks
f(n) values K24/K29; the n=8 and n=10 record sets recovered; no class with h < f(n).

## Falsifier report
Not applicable (exhaustive enumeration); L002's independently verified pipeline.
