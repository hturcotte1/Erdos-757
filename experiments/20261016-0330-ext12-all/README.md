# Two-point extensions of all 54,243 extremal 12-point (4,5)-set classes  [verified-here]

Question: for each of the 54,243 classes of census L002 (experiments/20261014-1005-census-dfs/results/realized_n12.json.gz;
n=12, m=10, h=7), is there a (4,5)-set B = A u {x,y} (x,y real, not in A) with h(B) <= 8? Such a B would be a 14-point extremal set,
by K47 necessarily non-saturated (m=11): a positive answer to Q11.

Method: extend12_all.py is extend_all.py of experiments/20261015-2340-ext14-all (L005) with n=12, target h(B) <= 8 (trivial bound h(A)+2 = 9).
Exact integer/Fraction arithmetic; A scaled by 4. Case analysis of L001/L005: T0 (no new AP: h=9); T1a (x in P_x, (4,5) single
extension, y generic: h = h(A u x)+1, computed exactly); T1b (every (4,5) pair x in P_x, y in cand(A u x); a 3-AP-free (Sidon-checked) 9-subset
is searched, else exact alpha); T2 (36 lines {a,x,y}, 12 points x 3 roles: exact alpha of H(A)+edge on 14 vertices, plus the pairwise line
intersection points tested for (4,5), none was); per class also h(A)=7 recomputed, number of maximum Sidon subsets, and the T2 pre-check
(a vertex in all maximum Sidon subsets). Optimisation vs L005: ndist has a 4-point fast path (verified identical on 15 classes).
No randomness. Case-analysis completeness is inherited from L001/L005 (not re-proved here).

Command: `bash scripts/start_job.sh experiments/20261016-0330-ext12-all 5 python3 experiments/20261016-0330-ext12-all/extend12_all.py experiments/20261014-1005-census-dfs/results/realized_n12.json.gz experiments/20261016-0330-ext12-all 3`
(nice 5, 3 processes; the job was restarted once after 280 classes with the faster ndist, it resumes from results.jsonl; output identical for the
15 classes compared). Runtime: 12,668 s wall in the final run (about 3.5 h; total about 10.6 CPU-hours; slowed by the 4-worker DFS and by the brute-force check running concurrently).
Acceptance check on known sets: `python3 extend12_all.py x x 1 --known`.

Status: evidence folder of certificate L006 (results/proofs/L006-ext12-all-two-point-extensions.md; K48 in kb/known_results.md; LEDGER row K48/L006). Referee ACCEPT x2 (results/reviews/L006-ext12-all-two-point-extensions__referee__20261016T081040Z.md and results/reviews/L006-ext12-all-two-point-extensions__referee__20261016T083111Z.md) after one text-only NEEDS-WORK round (results/reviews/L006-ext12-all-two-point-extensions__referee__20261016T073619Z.md); scout NOVELTY: CLEAR (results/reviews/L006-ext12-all-two-point-extensions__scout__20261016T070619Z.md). Regression test: tests/test_ext12_all.py.

Tracked outputs: summary.json (totals), bf_known.log and bf_random.log, bruteforce_sample_results.json and bruteforce_sample_results_random.json, and, outside this folder, data/ext12_all_rows.jsonl.gz (the 54,243 per-class rows). The uncompressed results.json (summary + all per-class rows), results.jsonl (same rows), progress.txt and run.log are git-ignored and exist only on the machine that ran the job.

## Results (totals in summary.json; per-class rows in data/ext12_all_rows.jsonl.gz = results.jsonl)
- Classes processed 54,243, h(A)=7 for all (asserted). No RECORD_CANDIDATES.txt exists: no extension with h <= 8 found.
- min h over all T1a/T1b/T2 extensions: 9 for every class (histogram {9: 54243}); all 55,105,041 evaluated values (T1a, T1b, T2 lines) equal 9.
- Single (4,5) extensions: 1,887,566 in total (21 to 46 per class). (4,5) T1b pairs: 51,264,727 in total (424 to 1,395 per class). T2 line-intersection (4,5) points: 0
  (19,247,288 intersection points tested). All 54,243 x 36 T2 line hypergraphs have alpha = 9.
- Number of maximum Sidon subsets: 48 to 63 per class. T2 pre-check (vertex in every maximum Sidon subset): false for all 54,243 classes.

## Acceptance
(1) Known sets of data/small_records.json (keys 12, 12b, 12c = the third set and the two omega sets), `--known`:
| set | max Sidon | singles (4,5) | T1b (4,5) pairs | T2 line alpha | min h | core vertex |
|---|---|---|---|---|---|---|
| 12 {0,269,...,575} | 62 | 34 | 893 | 9 | 9 | none |
| 12b omega | 60 | 35 | 933 | 9 | 9 | none |
| 12c omega | 60 | 36 | 974 | 9 | 9 | none |
(2) Brute force (bruteforce_sample.py; plain integer enumeration of ALL integer pairs x<y in the window [min-span, max+span] in x4 coordinates, (4,5) tested from scratch,
new APs of B found directly; then compared with extend12_all): the 3 known sets and 3 random classes (seed 757: 12070, 25977, 34895). In all 6: the set of (4,5) singles in P_x equals
extend12_all's (in window), the brute T1b (4,5) pair set (pairs with a new AP through a P_x point and the other point in an AP) equals extend12_all's T1b set restricted to the window
(715-975 pairs per class over the six stored classes; 106-130 further extend12_all pairs lie outside the window; an earlier seventh run on class 8532 with a smaller window [-127, 635] (256 in-window pairs, 377 outside, match true) survives only in git history, `git show a982863:experiments/20261016-0330-ext12-all/bruteforce_sample_results.json`, and is not part of these ranges), brute-force h of all T1b pairs is 9, and a 2,000-pair sample of
the 24k-37k T2-type (4,5) pairs all have h = 9. Brute (4,5) pair counts 9.6M to 20.3M per class. Logs bf_known.log, bf_random.log; json bruteforce_sample_results*.json
(bruteforce_sample_results.json is the known-sets run). Caveat: the brute force imports extend12_all only for the h routine (h_exact_B) and for the comparison.

## Conclusion
For every one of the 54,243 extremal 12-point classes of L002, every (4,5) two-point extension has h = 9 (>= 9, trivial upper bound h(A)+2 = 9). So no extremal
12-point set extends by two points to a 14-point (4,5)-set with h <= 8. [verified-here] (subject to the L001 case analysis, and to the completeness of the L002 census of 12-point extremal classes).
Consequence: every 14-point (4,5)-set with h = 8 has no 12-point subset with h = 7 (such a subset would be an extremal class of L002; a 12-point (4,5)-set has h >= 7 = f(12)),
for saturated (K47, observed) and non-saturated (this sweep) 14-point sets alike. Q11 itself (existence of a 14-point m=11 set with h=8) is not answered; only that any such set has all 12-point subsets with h >= 8. [verified-here]
