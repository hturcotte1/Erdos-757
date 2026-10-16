# Extremal sets and extremal subsets, n = 6..12  [verified-here]

Question: does an extremal (4,5)-set A (h(A) = f(n)) contain an extremal (n-2)-point subset (h(A\X) = f(n-2), |X| = 2) or an
extremal (n-1)-point subset (h = f(n-1))? Extends K47 (no saturated extremal 14-set contains an extremal 12-set) and K48/L006 to smaller n.
f(4..12) = 3,4,4,5,5,6,6,7,7.

Method (exact, integers): for each stored integer set A, compute its 3-APs (a+c = 2b) as bitmasks, enumerate all 3-AP-free subsets of size
f(n-k)+1 (k = 1, 2). Since h(A\X) >= f(|A\X|) always, A\X is extremal iff X meets (is a transversal of) every 3-AP-free (f(n-k)+1)-subset.
h(A) = f(n) is re-asserted for every class (no 3-AP-free (f(n)+1)-subset). Validation: `tests/test_extremal_subsets.py` compares against brute force
`e757.core.alpha` on deletions, and recomputes stored numbers.

Command (repo root): `nice -n 5 python3 experiments/20261016-0840-extremal-subsets/stats.py --out experiments/20261016-0840-extremal-subsets/results.json --procs 2`.
Runtime about 131 s wall (2 processes). No randomness. Log: `run.log`.

Data used: n = 6..10 all `n<n>_m<m>_real.json.gz` in `experiments/20261014-1430-small-counts/results/` (one integer representative per realizable pattern);
n = 11: m = 9 from the 418 `n11/results/post/real_*.json.gz` (all 466,961 saturated classes; this directory is git-ignored and absent from a clean clone, so `stats.py` can rebuild that row only after the L003 n = 11 pipeline in `experiments/20261014-1430-small-counts/run_all.sh` has been re-run; `tests/test_extremal_subsets.py` does not use it, and the row's output is stored in the tracked `results.json`), m = 6,7,8 from the `n11_m*_sample_real.json.gz` (first 300 DFS-order patterns only);
n = 12: `realized_n12.json.gz` (all 54,243 classes).

## Results (all realized classes at each size)
Saturated (m = n-2) rows are complete censuses (finite, rigid). Non-saturated rows (m < n-2) are infinite families; each stored pattern has ONE integer
representative and the property is a property of the AP pattern (the sub-pattern determines h of the subset), so these rows count patterns, not affine classes;
for n = 11, m <= 8 they are a biased sample.

| n | f(n) | f(n-1) | f(n-2) | saturated classes | with extremal (n-2)-subset | with extremal (n-1)-subset | non-saturated patterns stored | with ext. (n-2) | with ext. (n-1) |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 4 | 4 | 3 | 1 | 1 | 1 | 28 | 28 | 28 |
| 7 | 5 | 4 | 4 | 4 | 4 | 4 | 504 | 504 | 504 |
| 8 | 5 | 5 | 4 | 66 | 66 | 66 | 698 | 698 | 698 |
| 9 | 6 | 5 | 5 | 1,262 | 1,262 | 1,237 | 54,450 | 54,450 | 23,062 |
| 10 | 6 | 6 | 5 | 6,644 | 6,625 | 6,644 | 7,105 | 6,056 | 7,105 |
| 11 | 7 | 6 | 6 | 466,961 | 466,961 | 178,655 | 724 (sample) | 724 | 46 |
| 12 | 7 | 7 | 6 | 54,243 | 26,852 | 54,243 | none exist (K43) | - | - |

Distribution of the number of extremal deleted pairs (saturated classes): n = 10: 0:19, 1:82, 2:889, 3:2150, 4:2079, 5:1146, 6:279;
n = 12: 0:27,391, 1:12,587, 2:12,074, 3:2,191; n = 11: from 12 to 30 pairs (of 55) for every class, never 0 (full per-(n,m) distributions in `results.json`, keys `dist_pairs`, `dist_singles`).
Distribution of extremal single deletions at n = 11 (saturated): 0:288,306, 1:171,248, 2:7,407. (Odd n: f(n-1) = f(n)-1, so a one-point deletion is extremal only when it
drops h.)

Consistency check (f(n-1) = f(n) at even n): at n = 6, 8, 10, 12 every one-point deletion of every stored class is extremal (`all_singles_extremal` true in every even-n source, 100%).
(For m = n-2 rows at n = 6, 8 likewise.)

Record sets of `data/small_records.json` (n <= 12): all have extremal (n-2)-subsets (e.g. the n = 12 set has 3 deleted pairs, 12b and 12c have 2 each; the n = 10 record has 3).

Example (n = 12, saturated class, positive case): A = [0, 18, 19, 36, 38, 53, 58, 106, 116, 194, 330, 544]; deleting the elements at sorted indices [8, 11] gives the 10-point set
[0, 18, 19, 36, 38, 53, 58, 106, 194, 330] with h = 6 = f(10).

## Conclusion
"Extremal sets are not two-point extensions of extremal sets" is NOT a general pattern at small n: at n = 6..9 and 11 every stored class has an extremal (n-2)-subset,
at n = 10 99.7% of saturated classes (6,625 of 6,644; 85% of the m = 7 family representatives) and at n = 12 49.5% (26,852 of 54,243; 27,391 have none). The property first fails to be universal at n = 10 and the
fraction drops at n = 12; K47 (0 of 2,910 saturated classes at n = 14), K48/L006 (no extremal 14-point set at all, saturated or not, contains an extremal 12-point set) and K46/L005 (n = 16: no 16-point set with h <= 9 contains a saturated extremal 14-point set; the non-saturated case, Q11, is open) are thus consistent with a downward trend as n approaches the wall,
but this is only 3 data points for even n [heuristic]. The counts above are [verified-here] for the stored classes; non-saturated rows are pattern counts of one representative each.
