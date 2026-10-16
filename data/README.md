# Data

- Store censuses and search outputs as gzipped JSON lines: `data/<name>_n<k>.jsonl.gz`.
- Use one object per line, with exact values (ints, or strings "p/q").
- Keep every file under 50 MB; split by n if needed.
- Describe each file in this README: generator script, command, date, counts, schema.

## Files
(listing completed 2026-10-15)

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
  `census_n14_m12_classes.jsonl.gz` in the same order; 141,153 (4,5) single-point and 4,970,208 (4,5) two-point extensions in total, minimum h = 10 in all
  2,910 classes; per-class rows also in `results.jsonl`). Independent brute-force cross-check on 41 classes: `bruteforce_sample_results.json`
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
- n = 14, m = 11 (the open non-saturated case): DFS output in `experiments/20261014-1005-census-dfs/n14m11dfs/results/`
  (git-ignored; resumable job, 130 of 3,437 prefixes done at 2026-10-16 01:15 UTC, every finished prefix has 0 solutions; at roughly 30 to 36 prefixes per hour it cannot finish within the budget, so there is no result and Q11 stays open). [heuristic: no claim]
