# Data

- Store censuses and search outputs as gzipped JSON lines: `data/<name>_n<k>.jsonl.gz`.
- Use one object per line, with exact values (ints, or strings "p/q").
- Keep every file under 50 MB; split by n if needed.
- Describe each file in this README: generator script, command, date, counts, schema.

## Files
(listing completed 2026-10-16)

- `ext12_all_rows.jsonl.gz` (added 2026-10-16, 2.4 MB): one row per affine class of the 54,243 extremal 12-point (4,5)-sets of certificate L002 (K41), with the results of the two-point-extension sweep of certificate L006 (K48: within the L001/L005 case analysis, whose completeness is inherited and not re-proved, every (4,5) two-point extension has h = 9). The `class` field of a row is the index of that class in the list `realized_n12.json.gz` of `experiments/20261014-1005-census-dfs/results/`, and `set` is its sorted integer representative (equal to sorted(that record's `set`) in every row). Rows are NOT in class order: they are stored in the order the parallel sweep finished them (`imap_unordered`; identical to the git-ignored `results.jsonl`), and each class 0 to 54,242 occurs exactly once. Keys: `class`, `set`, `hA` (7 in every row), `n_max_sidon` (48 to 63), `in_all_max_sidon` ([] in every row), `t2_precheck` (false in every row), `Px_size` (candidate points x forming a new 3-AP with two points of A, before the (4,5) filter), `n_single_45` ((4,5) single extensions, 21 to 46), `t1_pairs` (candidate T1b pairs examined before the (4,5) filter), `n_t1b_45` ((4,5) T1b pairs, 424 to 1,395), `t2_lines` (36), `t2_line_h` ([9]), `t2_isect_pts`, `t2_isect_45` (0), `hist` (histogram of h over the evaluated T1a, T1b and T2 values), `min_h` (9 in every row), `records` ([] in every row), `n_2ext` (= `n_t1b_45` + `t2_isect_45`), `secs` (wall seconds for the class). Totals over the rows: 1,887,566 single and 51,264,727 T1b (4,5) extensions, 19,247,288 line-intersection points (none a (4,5)-set), 55,105,041 evaluated h values (all equal to 9), min h = 9 in all 54,243 classes. Generator: `experiments/20261016-0330-ext12-all/extend12_all.py` (exact command in that README; its uncompressed `results.json` and `results.jsonl` are git-ignored, this file is the tracked copy of the rows, `summary.json` there holds the totals). Pinned by `tests/test_ext12_all.py`. Tag: [verified-here].

- `ext15_sets.jsonl.gz` (added 2026-10-17, 333 KB; byte-identical to `experiments/20261017-0210-ext15-hunt/data/ext15_sets.jsonl.gz`): 2,337 distinct realizable non-saturated extremal 15-point (4,5)-sets, all with h = alpha = 9 = f(15) (1,589 with m = 12 APs, 748 with m = 11; saturated would be m = 13), distinct up to reflection of the AP pattern, one random realization per pattern (each pattern is a positive-dimensional family). Found by sampling the ordered C DFS at (15, alpha <= 9, m) and realizing exactly, so the sample is NON-uniform and says nothing about the number of such classes. One JSON object per line; keys: `set` (sorted primitive integers with minimum 0, up to 53 bits), `edges` (rank triples), `m`, `deg_seq`, `n_max_sidon`, `universal` ([] in every row), `n_ext_admissible` (63 to 109), `ext_degx_dist` ({"1": n_ext_admissible} in every row), `min_h_ext` (10 in every row), `cover_min` (smallest size of a set of pairs covering all maximum Sidon 9-subsets, searched up to size 14 - m: 3 for the m = 11 rows, null for the m = 12 rows, i.e. no cover of size <= 2), `n_min_covers` (0 for m = 12), `covers` ([] for m = 12), `n_record_ext` (0 in every row), `src` (pattern file of origin), and, in the 748 m = 11 rows only, `cover_ext` ({patterns, prefiltered, realizable, sets}; `realizable` is 0 and `sets` is [] in every row). Generator: `experiments/20261017-0210-ext15-hunt/hunt.py` (commands in that README; `stats.py` writes results.json). The first m = 11 and first m = 12 sets were judged: results/claims/C001-ext15-m11-example.json and C002-ext15-m12-example.json (n = 15, h = 9, ratio 3/5, no improvement). Tag: [verified-here] (exact realization and h checks; not referee-reviewed); the sampling is [heuristic]. K50, D26.

- `forbidden_ordered_n7.json`: ordered linear midpoint-injective AP patterns for n<=7: per-n class counts
  (realizable / order-infeasible / forced extra AP / forced repeated difference) and the 44 minimal forbidden
  cores (S, relation) up to reflection. Schema: cores[]: {n, kind in order|extra_ap|diff, edges [[i,j,k]], relation}.
  Generator: `experiments/20261013-2257-forbidden-library/enumerate.py 7 data/forbidden_ordered_n7.json`
  (e757.realizability), 2026-10-13. Tag: [verified-here].

- `small_records.json`: extremal (4,5)-sets attaining f(n) for n = 8, 10, 11, 12 (three inequivalent), 14, exact integers.
  Generator: `e757/ordered_search.py`, 2026-10-13; checked by `judge/judge.py`; pinned by `tests/test_known_facts.py::test_small_records`.
  Schema: `{"description", "sets": {key: {"set": [ints], "n", "h", "m" (number of 3-APs)[, "source"]}}}` with keys "8", "10", "11", "12", "14" (A_base, Ma-Tang 2026),
  "12b", "12c" (omega issue #9804). Tag: [verified-here] (K29).
- `forbidden_ordered_n8.json`: same schema as the n7 file, for n = 8 only: 46,281 ordered patterns and the 243 new minimal
  forbidden cores at n = 8 (4 to 6 edges; 287 = 44 + 243 cores in total for n <= 8). Generator:
  `experiments/20261014-0005-forbidden-n8/` (K33), 2026-10-14. Tag: [verified-here].
- `census_n14_m12_classes.jsonl.gz` (added 2026-10-15): the 2,910 affine classes of saturated 14-point (4,5)-sets with
  h = 8 and m = 12 (certificate L004, K45). One JSON object per line: `n`, `m`, `h`, `set` (exact integer realization,
  sorted) and `edges` (the labeled AP triples as indices into the sorted set). Concatenation of
  `experiments/20261014-1005-census-dfs/n14/results/post/real_*.json.gz` (that directory has been tracked since commit 0bb4ae7; only the per-prefix DFS streams `n14/results/n14_m12_prefix_*`, in its parent directory, are git-ignored; this file is the consolidated JSONL copy of the `real` records in those files). Spot check at creation: 5 random lines re-checked with `e757.core` (is_45 true, h = 8), and A_base occurs.
  Tag: [verified-here].
- `census_n14_m12_summary.json` (added 2026-10-15): filter counts (205,529 -> 119,844 -> 46,419 -> 34,995 patterns),
  unrealizability reasons, 50/50 judge spot check, and the DFS totals (113,454,008,923 nodes, 277,501 CPU-s), copied from
  `.../n14/results/post/summary.json` and `.../n14/results/n14_m12_TOTAL.json`. Tag: [verified-here].

## Census data that lives under experiments/ (not duplicated here)
- n = 14 two-point extensions (K46, L005): `experiments/20261015-2340-ext14-all/results.json` (keys `summary` and `classes`, one row per class of
  `census_n14_m12_classes.jsonl.gz` in the same order; 141,153 (4,5) single-point extensions and 4,970,208 (4,5) two-point extensions with both new points in new 3-APs (case T1b) in total, minimum h = 10 in all cases including the one-edge lines (T2), over all 2,910 classes; per-class rows also in `results.jsonl`). Independent brute-force cross-check on 41 classes: `bruteforce_sample_results.json`
  (all pairs on a bounded half-integer grid window; 105,720,197 (4,5) pairs, 0 failures). Tracked. [verified-here]
- n = 14 structure census (K47): `experiments/20261016-0150-structure-2910/results.json` (keys `summary` and `rows`; 2,910 rows in census order with degree
  sequence, number of maximum Sidon subsets, symmetry, cut vertices, gaps). Tracked. [verified-here]
- n = 13, saturated (m = 11): NO census exists. The attempt was stopped as infeasible (D22, Q12); only the partial counts are kept, in
  `experiments/20261015-2330-census-n13/partial_summary.json` (8 of 1,811 prefixes, 54,717,717 class-O patterns up to reflection; the pattern streams were deleted). [verified-here: partial counts]
- n = 12, 54,243 classes (K41, L002): `experiments/20261014-1005-census-dfs/results/realized_n12.json.gz` (list of 54,243
  records) and `n12_m10_all.jsonl.gz` (all 2,226,490 labeled patterns). Tracked.
- n = 6..11 saturated counts (K43, L003): `experiments/20261014-1430-small-counts/results/` (per-(n,m) pattern files and
  `summary.json`). The raw n = 11 pipeline directory `n11/results` is git-ignored; its summary
  `results/n11_m9_postprocess_summary.json` is tracked. [verified-here]
- Extremal (n-2)- and (n-1)-point subsets, n = 6..12 (K49): `experiments/20261016-0840-extremal-subsets/results.json` (keys `F`, `per_source`, `per_size`, `small_records`: counts and distributions per (n, m)). Tracked; its n = 11, m = 9 input (`experiments/20261014-1430-small-counts/n11/results/post/real_*.json.gz`, 418 files) is git-ignored. [verified-here]
- n = 14, m = 11 (the non-saturated case; CLOSED on 2026-10-17 by certificate L007 / K51: no such extremal 14-point set exists, so 2,910 is the complete count of affine classes of extremal 14-point sets (inherits the L004 completeness caveat: the enumeration's completeness was re-checked on 28% of the prefixes plus consistency checks, not by a full second enumeration) and Q11 is closed): partial DFS output in `experiments/20261014-1005-census-dfs/n14m11dfs/results/`
  (git-ignored; resumable job, stopped at 1,081 of 3,437 depth-3 prefixes per the last progress line of its (git-ignored) run.log; 1,087 `.done` markers were on disk at the time of this audit, and every finished prefix has 0 solutions and no timeout; it was superseded by L007 and no claim rests on it). [verified-here: L007; the partial DFS is [heuristic], no claim]
- Class lists and hit lists of the I11 induction (certificates L007-L012, K51-K56) are not duplicated here: see `experiments/20261017-0300-n16-via-i11/` (`G_R12_AP.txt`, `G_B_classes49.txt`, hit lists), `experiments/20261017-0615-n17-n18-via-i11/` (`C14_classes.json`, `G17_classes.json`), `experiments/20261017-0705-n19-n20-via-i11/` (`X18_deg3_classes.json`, `post_*.json`, hit files), `experiments/20261017-0825-n21-n22-via-i11/` (`post_*.json`, `results.json`; its `*.txt` class lists are git-ignored), `experiments/prover/L012/route4_classes.txt.gz` (the 699 degree-4 classes of the cell (23,21,10)) and the `reproduce.sh` of `experiments/prover/L007` to `L012`. The bulkiest outputs of L010 to L012 are in git-ignored `out/` directories and are regenerated by those scripts; the re-run outputs of L007 to L009 are in tracked `rerun/` directories. [verified-here]
