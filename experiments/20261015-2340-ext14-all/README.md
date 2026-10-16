# 2-point extensions of all 2,910 saturated extremal 14-point (4,5)-sets  [verified-here]

Status: evidence folder of certificate L005 (results/proofs/L005-ext14-all-two-point-extensions.md; K46 in kb/known_results.md; LEDGER row K46/L005). Referee ACCEPT x2 (results/reviews/L005-ext14-all-two-point-extensions__referee__20261016T013746Z.md and results/reviews/L005-ext14-all-two-point-extensions__referee__20261016T013731Z.md) after one text-only NEEDS-WORK round (results/reviews/L005-ext14-all-two-point-extensions__referee__20261016T011417Z.md); scout NOVELTY: CLEAR (results/reviews/L005-ext14-all-two-point-extensions__scout__20261016T002432Z.md); regression test tests/test_ext14_all.py (re-runs the per-class routine on classes 0 and 2440). The brute-force cross-check is described at the end of this file.

Question: for each class A in data/census_n14_m12_classes.jsonl.gz (n=14, m=12, h=8), is there a
(4,5)-set B = A u {x,y} (x,y real, not in A) with h(B) <= 9? Such a B would be a 16-point record (9/16 < 4/7).

Method: exactly the case analysis T0/T1a/T1b/T2 of results/proofs/L001-abase-two-point-extensions.md,
generalised from experiments/20261014-0640-abase-extensions/extend.py. Per class:
- A is scaled by 4, so every T1 candidate (midpoints/endpoints of pairs of A u {x}, x in P_x) is an integer (asserted); T2 intersection
  points use Fractions scaled to a common denominator. All checks are integer/Fraction arithmetic.
- h(A)=8 recomputed (all 2,910 classes), all maximum 3-AP-free 8-subsets enumerated: their number and the points lying in all of them (T2 pre-check).
- T1a: h(A u x)+1 for every admissible single extension x (A u x a (4,5)-set). T1b: all candidate pairs {x,y}; (4,5) tested exactly
  on every 4-set containing x or y; for each (4,5) pair a 3-AP-free (checked Sidon) 10-subset is searched (h<=10 is trivial); if none, exact alpha.
- T2: 42 lines (14 points x 3 roles), hypergraph H(A)+{a,x,y} on 16 vertices, 10-subset searched (else exact alpha);
  the pairwise line-intersection points are tested exactly for (4,5) and, if (4,5) and not already in T1, h computed.
- Any h<=9 would be written to RECORD_CANDIDATES.txt (none was).

Command: `bash scripts/start_job.sh experiments/20261015-2340-ext14-all 4 python3 experiments/20261015-2340-ext14-all/extend_all.py data/census_n14_m12_classes.jsonl.gz experiments/20261015-2340-ext14-all 2`
(nice 15; no randomness). A_base test: `python3 extend_all.py x x 1 --abase-test` (1.2 s).
Runtime: 1844 s wall clock with 2 processes (about 1.0 CPU-hour).

## Acceptance (A_base)
Output on {0,136,...,1056}: |P_x|=223, 50 single (4,5) extensions, 11,774 T1 pairs, 1,743 (4,5) T1b pairs all with h=10,
42 T2 lines all alpha=10, 498 T2 intersection points, 0 of them (4,5), 143 maximum Sidon subsets: matches L001 exactly.
The same numbers appear in the census class with index 2440 (found by its numbers) of results.json.

## Results (results.json; per-class rows also in results.jsonl)
- Classes processed: 2,910 (all fully through T1a, T1b, T2); h(A)=8 for all.
- Single (4,5) extensions: 141,153 in total (32 to 61 per class). (4,5) 2-point extensions in T1b/T2-intersections: 4,970,208 total (854 to 2,496 per class).
- min h over all extensions (T1a/T1b/T2): 10 for every class. Histogram {10: 2910}. Classes with h<=9: 0. No record candidates.
- All 2,910*42 T2 line hypergraphs have alpha = 10; no T2 line-intersection point is a (4,5)-set in any class.
- T2 pre-check (a point of A lying in all maximum Sidon subsets): false for every class (0/2910); number of maximum Sidon subsets ranges 137 to 150.

## Conclusion
For every one of the 2,910 saturated extremal 14-point classes, every (4,5) two-point extension has h = 10 (ratio 5/8).
No 16-point (4,5)-set contains a saturated extremal 14-point set with h <= 9. [verified-here] (subject to the L001 case analysis;
this does not cover extensions by 4+ points, nor non-saturated 14-point sets with h=8, Q11.)

## Independent brute-force cross-check [verified-here]
Script `bruteforce_sample.py` (plain integers + numpy integer arrays; the brute-force part imports neither e757 nor extend_all; extend_all is
imported only afterwards to compare counts). Classes: indices {0, 2440} u {73k : k=1..39} (41 classes; 2440 = A_base). Per class: A is doubled
(half-integers become integers), window = integers in [min - span/4, max + span/4] (span of the doubled set; the full window was fast enough, no
shrinking). ALL pairs x<y in the window with x,y not in A are enumerated; a pair is (4,5) iff every 4-subset containing x or y has >= 5 distinct
differences (single condition for x and y, then all {x,y,a,b}). For every (4,5) pair a 3-AP-free 10-subset of A u {x,y} is certified through
bitmasks over the maximum 8-subsets of A (c+{x,y} AP-free iff c+x, c+y AP-free and no AP uses both x,y); the bitmask logic is re-verified
explicitly (size 10, subset of A u {x,y}, 3-AP-free, Sidon) for every pair that has an AP through both x and y and for every 997th pair
(502,942 explicit verifications in total; 0 fallbacks to exhaustive 10-subset search were needed).
Command: `nice -n 15 python3 experiments/20261015-2340-ext14-all/bruteforce_sample.py --procs 2` (log bruteforce_sample.log, output
bruteforce_sample_results.json). Runtime 700 s wall (11 min 40 s, 2 processes at nice 15; no randomness).

Result: 105,720,197 (4,5) pairs in total over the 41 classes, 0 failures (every (4,5) pair has a 10-subset that is 3-AP-free and Sidon, so h >= 10;
h <= 10 is the trivial bound h(A)+2). Single extensions: for every class the brute-force set of (4,5) singles in the window that form an AP with two
points of A equals exactly the set of extend_all's n_single_45 candidates lying in the window (as sets, 41/41). extend_all's singles outside the window:
629 in total (all other singles are inside; 0 are non-half-integers in the doubled coordinates, i.e. none is a quarter-integer). Counts may differ
by candidates outside the window only; the n_single_45 column is the stored value (= recomputed value in every class).
Caveat: the grid is half-integers (original coordinates); T1b partners y that are quarter-integers (midpoints of x and a point of A) are not
on the grid and are not covered by this check; the stored T1b counts are therefore not compared pair by pair, only the singles are.

| class | window (original coords) | brute (4,5) singles in P_x, in window | stored n_single_45 | (4,5) pairs | pairs with an AP through x,y | failures | singles match |
|---|---|---|---|---|---|---|---|
| 0 | [-185.5, 927.5] | 25 | 39 (14 outside window, 0 non-half-integer) | 1244612 | 6575 | 0 | yes |
| 73 | [-174.5, 873.5] | 38 | 54 (16 outside window, 0 non-half-integer) | 1012386 | 5076 | 0 | yes |
| 146 | [-130.5, 653.5] | 38 | 55 (17 outside window, 0 non-half-integer) | 451261 | 2562 | 0 | yes |
| 219 | [-162, 810] | 33 | 49 (16 outside window, 0 non-half-integer) | 793877 | 4237 | 0 | yes |
| 292 | [-174, 870] | 34 | 46 (12 outside window, 0 non-half-integer) | 1009202 | 5368 | 0 | yes |
| 365 | [-269.5, 1347.5] | 31 | 43 (12 outside window, 0 non-half-integer) | 3134123 | 12019 | 0 | yes |
| 438 | [-205, 1025] | 33 | 47 (14 outside window, 0 non-half-integer) | 1497961 | 6602 | 0 | yes |
| 511 | [-97, 485] | 32 | 47 (15 outside window, 0 non-half-integer) | 171527 | 954 | 0 | yes |
| 584 | [-173, 865] | 36 | 48 (12 outside window, 0 non-half-integer) | 1031628 | 5476 | 0 | yes |
| 657 | [-213.5, 1067.5] | 32 | 47 (15 outside window, 0 non-half-integer) | 1748377 | 8025 | 0 | yes |
| 730 | [-510.5, 2552.5] | 35 | 52 (17 outside window, 0 non-half-integer) | 14155354 | 31286 | 0 | yes |
| 803 | [-209, 1045] | 34 | 48 (14 outside window, 0 non-half-integer) | 1566860 | 6879 | 0 | yes |
| 876 | [-164.5, 823.5] | 30 | 47 (17 outside window, 0 non-half-integer) | 873066 | 4638 | 0 | yes |
| 949 | [-179, 895] | 25 | 40 (15 outside window, 0 non-half-integer) | 1076362 | 5681 | 0 | yes |
| 1022 | [-155.5, 777.5] | 32 | 45 (13 outside window, 0 non-half-integer) | 750951 | 4143 | 0 | yes |
| 1095 | [-141, 705] | 36 | 53 (17 outside window, 0 non-half-integer) | 550640 | 3066 | 0 | yes |
| 1168 | [-179, 895] | 31 | 47 (16 outside window, 0 non-half-integer) | 1029060 | 4945 | 0 | yes |
| 1241 | [-173.5, 868.5] | 43 | 61 (18 outside window, 0 non-half-integer) | 923690 | 4168 | 0 | yes |
| 1314 | [-199.5, 998.5] | 36 | 53 (17 outside window, 0 non-half-integer) | 1370034 | 5989 | 0 | yes |
| 1387 | [-508.5, 2542.5] | 39 | 51 (12 outside window, 0 non-half-integer) | 14392913 | 31845 | 0 | yes |
| 1460 | [-407.5, 2037.5] | 39 | 56 (17 outside window, 0 non-half-integer) | 8489844 | 22569 | 0 | yes |
| 1533 | [-232, 1160] | 31 | 47 (16 outside window, 0 non-half-integer) | 2100627 | 8544 | 0 | yes |
| 1606 | [-203, 1015] | 34 | 48 (14 outside window, 0 non-half-integer) | 1575044 | 7354 | 0 | yes |
| 1679 | [-169, 845] | 33 | 49 (16 outside window, 0 non-half-integer) | 957158 | 5222 | 0 | yes |
| 1752 | [-161.5, 807.5] | 31 | 46 (15 outside window, 0 non-half-integer) | 821652 | 4302 | 0 | yes |
| 1825 | [-181, 905] | 33 | 51 (18 outside window, 0 non-half-integer) | 1028126 | 4659 | 0 | yes |
| 1898 | [-364, 1820] | 32 | 50 (18 outside window, 0 non-half-integer) | 6375253 | 18611 | 0 | yes |
| 1971 | [-165, 826] | 40 | 56 (16 outside window, 0 non-half-integer) | 817336 | 3907 | 0 | yes |
| 2044 | [-186.5, 932.5] | 32 | 49 (17 outside window, 0 non-half-integer) | 1165079 | 5476 | 0 | yes |
| 2117 | [-504, 2520] | 40 | 57 (17 outside window, 0 non-half-integer) | 13778493 | 30095 | 0 | yes |
| 2190 | [-189, 945] | 29 | 45 (16 outside window, 0 non-half-integer) | 1163299 | 5493 | 0 | yes |
| 2263 | [-242, 1210] | 39 | 57 (18 outside window, 0 non-half-integer) | 2289555 | 8748 | 0 | yes |
| 2336 | [-205, 1025] | 33 | 47 (14 outside window, 0 non-half-integer) | 1518908 | 6967 | 0 | yes |
| 2409 | [-244, 1220] | 35 | 49 (14 outside window, 0 non-half-integer) | 2330126 | 8979 | 0 | yes |
| 2440 | [-264, 1320] | 39 | 50 (11 outside window, 0 non-half-integer) | 2918899 | 10549 | 0 | yes |
| 2482 | [-153, 765] | 26 | 44 (18 outside window, 0 non-half-integer) | 648655 | 3512 | 0 | yes |
| 2555 | [-223, 1115] | 34 | 48 (14 outside window, 0 non-half-integer) | 1866974 | 7968 | 0 | yes |
| 2628 | [-218.5, 1092.5] | 38 | 54 (16 outside window, 0 non-half-integer) | 1732789 | 7025 | 0 | yes |
| 2701 | [-228.5, 1142.5] | 30 | 41 (11 outside window, 0 non-half-integer) | 2031196 | 8285 | 0 | yes |
| 2774 | [-215, 1076] | 30 | 48 (18 outside window, 0 non-half-integer) | 1639960 | 6663 | 0 | yes |
| 2847 | [-216.5, 1082.5] | 30 | 46 (16 outside window, 0 non-half-integer) | 1687340 | 6946 | 0 | yes |
