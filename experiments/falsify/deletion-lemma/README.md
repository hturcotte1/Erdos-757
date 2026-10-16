# Falsification of Lemma Delta' (deletion version), kb/notes/extension_lemmas.md   [verified-here on data; lemma derived-here]

Command: `nice -n 5 python3 run.py` (about 2 minutes; numpy only, all arithmetic integer / Fraction). Output: results.json.
Pairs: for every set and every pair p<q, h(A-p-q) is computed exactly from the true AP hypergraph (recomputed from the integer set) by a
subset-DP over all 2^n masks. "ext" = h(A) = f(n) and h(A-p-q) = f(n-2) = f(n)-1.

## 4. Hand derivation
tau = n - h(A) = n - f(n). If h(A-p-q) = f(n)-1 then tau' = (n-2) - (f(n)-1) = tau - 1.
H-p-q is linear and F7-free (sub-hypergraph) on n-2 vertices with m' = m - deg p - deg q + eps edges (edges through p or q are removed;
an edge containing both is counted twice in deg p + deg q, hence +eps; two distinct APs cannot share both p and q by linearity).
Henning-Yeo: 17 tau' <= 5(n-2) + 3 m'. So 17 tau - 17 <= 5n - 10 + 3m - 3d, d := deg p + deg q - eps, hence
3d <= 5n + 3m + 7 - 17 tau, i.e. d <= m - (17 tau - 5n - 7)/3.  CORRECT.
Numbers: (14,12,6): 17*6-70-7 = 25, 12-25/3 = 3.67 -> 3. (12,10,5): 85-60-7 = 18, 10-6 = 4. (16,14,7): 119-80-7 = 32, 14-32/3 = 3.33 -> 3.
(16,13,7): 13-32/3 = 2.33 -> 2.  All four quoted values correct. (Note: this is just Henning-Yeo restated, so the data test checks arithmetic,
the (h, f(n-2)) bookkeeping, and the linear/F7-free hypotheses, not new combinatorics.)

## Results (violations: 0 everywhere)
| data | sets | bound | sets with ext pair | distribution of d over ext pairs |
|---|---|---|---|---|
| n=12 m=10 tau=5, all 54,243 classes | 54,243 | 4 | 26,852 | d=2: 11,944; d=3: 31,364 (max 3 <= 4) |
| n=10 m=8 tau=4, all 6,644 saturated | 6,644 | 13/3 (<=4) | 6,625 | d=2: 1,494; d=3: 22,536 |
| n=8 m=6 tau=3, all 66 saturated | 66 | 14/3 (<=4) | 66 | d=2: 29; d=3: 439; d=4: 166 (tight) |
| bonus n=10 m=7 (7,105 patterns, one realization each) | | 10/3 (<=3) | 6,056 | d=2: 12,112 |
| bonus n=8 m=5 (698) | | 11/3 (<=3) | 698 | d=2: 2,258; d=3: 1,663 |
| bonus n=9 m=7 (1,262) / m=6 (20,938), f(7)=5 | | 22/3 / 19/3 | all | max d = 5 / 4 (bounds 7 / 6) |
| n=14 m=12 tau=6, 2,910 classes | 2,910 | 11/3 (<=3) | 0 | none (K47 reproduced: all pairs leave h=8) |

n=12, pairs NOT leaving h=6 (h(A-p-q)=7, no constraint): d=3: 269,509; d=4: 1,284,281; d=5: 1,698,008; d=6: 275,295; d=7: 9,637
(pairs leaving h=6: 43,308 in total; no pair ever leaves h=5). Note extremal pairs have d in {2,3} only, so the n=12 bound 4 is not tight (slack 1).
n=14: all 264,810 pairs leave h=8. Adjacent degree-2 pairs: 18,330 total over the 2,910 classes, ALL with d = 3 (= the bound 3, so the
lemma permits them yet none works). Distribution of d over all pairs at n=14: 3: 18,330; 4: 78,481; 5: 124,290; 6: 39,924; 7: 3,068; 8: 717.
