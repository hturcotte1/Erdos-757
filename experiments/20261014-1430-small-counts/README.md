# Exact counts of extremal (4,5)-sets (h = f(n)), n = 6..13  [verified-here unless noted]

Question: for each n, how many n-point (4,5)-sets with h(A) = f(n) exist up to affine equivalence (x -> qx+t, reflection included)?
f(6..13) = 4,5,5,6,6,7,7,8 (START_HERE section 5).

## Method (same as L002, results/proofs/L002-census-12-point-extremal-sets.md)
For each n and each m from 1 to n-2 (below the Henning-Yeo minimum m_HY = ceil((17(n-f)-5n)/3) as well, to see the zeros):
1. `e757/c/ordered_dfs n=N T=f(n) m_min=m m_exact=m f7=1 mode=enum`: all class-O patterns (linear, injective midpoints, K30 monotone,
   F7-free) with exactly m edges and alpha <= f(n). (Any (4,5)-set with h = f(n) has its AP pattern in this list; for m < n-2 some points are not midpoints.)
2. Every pattern up to reflection is realized exactly: `fastreal.realize_fast` (Fraction Gauss-Jordan) for m = n-2 (rigid), else
   `e757.realizability.realize_exact` (exact LP order-feasibility + forced extra AP / forced repeated difference tests + exact generic point).
   Every realization re-checked with `e757.core.is_45_set` and `e757.core.alpha` (h = f(n) always; `all_h_eq_f` in the JSONs).
3. Saturated m = n-2: pattern is rigid (AP rank n-2) so realizable patterns up to reflection = affine classes (distinct normalised sets counted, same number).
   Non-saturated m < n-2: a realizable pattern has solution space of dimension 2 + k, k >= 1 free parameters ("free params" column), and the realizability
   conditions are open, so it contains infinitely many affine classes: **infinite family** [derived-here]. Only pattern counts are reported there.
4. n = 11, m = 9 (4.9M patterns up to reflection) is done with the L002 pipeline: `ordered_dfs_split` (depth 2, 83 prefixes, P=1) +
   `experiments/20261014-1005-census-dfs/postprocess.py` (C filter K30/K31/cores<=4 edges, then exact realization of the survivors; the filters are proved necessary
   conditions, K31-K33). n = 12: the L002 census is reused, not rerun (m=10: 2,226,490 patterns, 54,243 classes; m=9: 0 patterns).

Commands (repo root, one niced process each): `python3 experiments/20261014-1430-small-counts/counts.py N [m...]` (n <= 10, all m),
`dfscount.py N m...` (streaming DFS counts), `bash experiments/20261014-1430-small-counts/run_all.sh` (n=9,10 m=6..8, the n=11 pipeline, n=11 samples),
`judge_spot.py`, `make_table.py` (-> results/summary.json). Seeds: judge spot check `random.seed(757)`; no other randomness (realize_exact uses its fixed Random(0)).

## Results
Patterns: labelled (both reflections) / up to reflection (class O, alpha <= f(n)); "realizable" = realizable patterns up to reflection.
Rows with no pattern at all are omitted except the first zero below m_HY.

| n | f(n) | m_HY | m with patterns | m | labelled | up to refl. | realizable | free params k | affine classes |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 4 | 2 | 2,3,4 | 2 / 3 / **4** | 9 / 46 / 2 | 6 / 23 / 1 | 6 / 22 / **1** | 2 / 1 / 0 | infinite family; saturated: **1** |
| 7 | 5 | 1 | 2..5 | 2 / 3 / 4 / **5** | 63 / 631 / 348 / 10 | 33 / 320 / 175 / 5 | 33 / 313 / 158 / **4** | 3 / 2 / 1 / 0 | infinite; saturated: **4** |
| 8 | 5 | 4 | 5,6 | 5 / **6** | 1832 / 260 | 916 / 130 | 698 / **66** | 1 / 0 | infinite (m=5, 698 patterns); saturated: **66** |
| 9 | 6 | 2 | 3..7 | 3 / 4 / 5 / 6 / **7** | 208 / 5256 / 74,212 / 69,535 / 8570 | 110 / 2628 / 37,151 / 34,771 / 4296 | 110 / 2536 / 30,866 / 20,938 / **1262** | 4 / 3 / 2 / 1 / 0 | infinite; saturated: **1262** |
| 10 | 6 | 6 | 7,8 | 7 / **8** | 36,210 / 79,488 | 18,105 / 39,765 | 7105 / **6644** | 1 / 0 | infinite (m=7, 7105 patterns); saturated: **6644** |
| 11 | 7 | 5 | 6..9 | 6 / 7 / 8 / **9** | 208,880 / 8,891,530 / 26,228,370 / 9,871,248 | 104,440 / 4,445,884 / 13,114,258 / 4,935,851 | >=251 / >=257 / >=216 (first 300 each, see below) / **466,961** | 3 / 2 / 1 / 0 | infinite (some non-saturated patterns realizable); saturated: **466,961** |
| 12 | 7 | 9 | 10 only | **10** | 2,226,490 | 1,113,245 | **54,243** | 0 | **finite: 54,243** (m=9: 0 patterns; L002) |
| 13 | 8 | 7 | not computed | | | | | | not computed (see below) |

Zeros: n=6 m=1; n=7 m=1; n=8 m=1..4 (m_HY=4); n=9 m=1,2; n=10 m=6 (m_HY=6) and m<6 by Henning-Yeo (not enumerated); n=11 m=5 (m_HY=5); n=12 m=9 (L002).
So the smallest m with any class-O pattern is m_HY+1 for n = 7..12 (m_HY itself for n = 6); the Henning-Yeo bound is never attained at n >= 7 (n=7: m_HY clamped to 1).

Observations
- Non-saturated extremal sets exist (hence infinitely many classes) for every n = 6..11, **but not for n = 12**: all 54,243 extremal 12-point sets are saturated and rigid,
  so for n=12 the number of affine classes is finite and equals 54,243 (L002). The n=8 record set of data/small_records.json has m=5 APs (in the 1-parameter family), the n=10 record has m=8 (one of the 6644 saturated classes), the n=11 record m=8.
- Saturated counts 1, 4, 66, 1262, 6644, 466,961, 54,243 for n = 6, 7, 8, 9, 10, 11, 12: not monotone (n=11 has the slack f(11)=7 = f(12), n=12 is Henning-Yeo-tight).
- n=11, m=9 pipeline: 4,935,851 patterns up to reflection -> 3,269,771 K31-free -> 1,671,894 after cores<=4 -> **466,961 realizable** (all rigid, all (4,5)-sets, all h=7,
  all inside the all-cores set, 0 fallbacks, 0 record-beating); unrealizable 1,204,933 = order-infeasible 1,067,660 + forced extra AP 72,327 + forced repeated difference 64,946.
  The DFS raw count 9,871,248 equals the unsplit count of dfscount.py.
- n=11, m<9 realizability: the counts of realizable patterns are NOT computed (the m=8 DFS output alone has 13.1M patterns up to reflection; realize_exact costs ~14-25 ms each = ~50 h).
  Instead the **first 300 patterns in DFS order** were realized exactly per m (a biased sample, not a count): 251/300, 257/300, 216/300 realizable (m = 6, 7, 8), all with h = 7.
  This shows non-saturated extremal families exist at n=11; the table's ">=" entries are only these sample counts.
- n=13: **not done**. Knuth-style estimates of DFS calls (mode=estimate, 1500 probes): m=11: 2.3e10 +- 0.3e10 (about 10 h of one process at 0.65M nodes/s,
  producing probably 1e8+ raw patterns, then filtering/realization of several more hours), m=7..10: 0.8-1.2e11 each. The n=14 prefix-split job has priority on the CPU, so n=13 was not launched.
  A pruning DFS with incremental realizability (or a compiled realizer) would be needed.
- Judge spot check (20 random realized sets per n, pooled over all m with realized sets; for n=11 from the 900 sampled non-saturated ones): n=6..11 all 20/20
  `PASS NO-IMPROVEMENT`, h = f(n) (results/judge_spot_n*.txt). n=11 m=9 additionally 50/50 (results/n11_m9_judge_spotcheck50.txt); n=12: 50/50 (L002).

## Timings (single process, nice 10, machine shared with the n=14 job)
n<=9: seconds to ~9 min (n=9 m=5/m=6 realization 540 s / 507 s). n=10: DFS 2 s, realization 370 s (m=7) / 54 s (m=8).
n=11: DFS counts 137 s (m=5), 139 s (m=6), 337 s (m=7), 565 s (m=8), 204 s (m=9); m=9 pipeline: split DFS 262 CPU-s, filter 1567 s, realization 3262 s (418 batches of 4000).

## Files
results/n*_m*.json (per-(n,m) exact results; `_sample` = first-300 samples), results/n*_m*_real.json.gz (realized sets), results/dfs_n*_m*.json (DFS counts),
results/summary.json (aggregate), results/n11_m9_*.json/txt (pipeline summary; raw pipeline dir n11/results is gitignored), results/judge_spot*.
tests/test_small_counts.py re-derives the n=8 and n=10 saturated counts (260/130/66; 79,488/39,765/6644) and checks that the n=8 (m=5, non-saturated pattern realizable) and n=10 (m=8, saturated class) record sets are among the extremal patterns/classes.

Tags: all counts [verified-here] (exact C enumeration + exact rational realization); the necessary conditions used by the n=11 pipeline filter are K30-K33 [verified-here];
"infinite family" is [derived-here] (positive-dimensional open solution set); n=13 estimates are [heuristic].
