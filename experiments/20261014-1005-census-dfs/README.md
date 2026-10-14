# Exhaustive (12,10,alpha<=7) census via the C DFS  [verified-here unless noted]

Question: exact number of abstract and realizable extremal structures (n=12, m=10 edges, alpha<=7), replacing the
time-limited CP-SAT enumeration (experiments/20261014-0610-extremal-census, 30,559 solutions, unfinished).

## Method / commands (all from repo root; one process each; machine shared, load ~5)
1. Enumerate class O (linear, midpoint-injective, K30 monotone, F7-free) with exactly 10 edges and alpha<=7:
   `e757/c/ordered_dfs n=12 T=7 m_min=10 m_exact=10 f7=1 mode=enum progress=0` (build: `bash e757/c/build.sh`).
   EXHAUSTED: 187,004,404 nodes, 2,226,490 solutions (both reflections listed), 287.7 s, timed_out=0.
   Stream: results/n12_m10_all.jsonl.gz (one edge list per line).
2. `filter.c` (independent C re-statement of K30, K31 and core embedding, same semantics as
   e757.cpsat_model.core_hit/constraint_violations; verified identical to the Python on 2,989 solutions; cores from
   data/forbidden_ordered_n7.json + n8.json via dump_cores.py -> cores.txt). Reflection-dedupe = keep es <= refl(es).
   Output results/n12_m10_filtered.txt.gz (flags k30 k31 c4 call + edges).
3. `realize_all.py`: exact realization of every O' pattern (K31 + cores with <=4 edges = the CP-SAT census class).
   `fastreal.py` = exact Fraction solve of the rigid AP system (rank n-2), same reasons/order of checks as
   realize_exact (checked identical on 2,500 patterns, 0 mismatches; 0 patterns needed the fallback to realize_exact).
   Affine normalisation as in the earlier census.py (translate to 0, divide by gcd, min with reflection).
4. Judge spot check: 50 random realized sets, `python3 judge/judge.py` on temp claim files: 50/50 PASS NO-IMPROVEMENT, h=7
   (results/judge_spotcheck.txt).
5. `crosscheck.py`: every one of the 30,559 CP-SAT solutions (29,228 up to reflection) occurs in the DFS output: 0 missing.

## Counts
| item | count |
|---|---|
| O solutions (labelled, both reflections) | 2,226,490 |
| O up to reflection | 1,113,245 (no reflection-symmetric solution) |
| ... K31 medial-free | 754,235 |
| ... + cores with <=4 edges (O', CP-SAT class) | 395,039 |
| ... + ALL 287 cores (n=6,7,8) | 313,774 |
| realizable (exact) | 54,243 (all rigid, all h=7, all (4,5)-sets; all inside the all-cores set) |
| affine classes (incl. reflection) | 54,243 |
| unrealizable (of the 395,039) | 340,796 = order-infeasible 321,304 + forced extra AP 10,803 + forced repeated difference 8,689 |

Of the 340,796 unrealizable patterns, 81,265 (= 395,039 - 313,774) are also excluded by the longer (5-6 edge) cores
(order-infeasible 78,299; extra AP 1,282; repeated difference 1,684): consistent, none of the realizable ones is excluded.
Record-beating sets: 0 (all h=7, 7*7 = 49 >= 48).
Known sets: all five (data/small_records.json 12, 12b, 12c; core.KNOWN omega examples 1, 2) are among the affine classes.

## Exhaustiveness and the statement
(12,9,alpha<=7) in class O: `ordered_dfs n=12 T=7 m_min=9 m_exact=9 f7=1` EXHAUSTED, 425,209,182 nodes, 607 s,
**0 solutions** (m9/run_m9.sh). Henning-Yeo (published) gives m>=9 for alpha<=7, n=12; m<=10 = n-2.
So every 12-point (4,5)-set with h=7 has a pattern in the m=10 list. Assuming the published F7-freeness / Henning-Yeo and the
repo's K30/K31/core necessary conditions (all derived/verified here):

**The number of 12-point (4,5)-sets with h=7, up to affine equivalence (x -> qx+t, including reflection), is 54,243.**
(Patterns are rigid, so each realizable pattern is exactly one affine class.)

## (14,12,alpha<=8) timing
10 min run (n14/run.log): 245,428,224 nodes, 2,821 solutions so far, only inside the first branch, 409k nodes/s under load.
Knuth-style estimator (`mode=estimate`, n14/estimate_seed*.txt): 8.3e10 +- 1.7e10 (2000 probes), 1.04e11 +- 1.1e10 (6000 probes) calls.
Calibration: the same estimator gives 1.8e8 for (12,10) vs actual 1.87e8. => 55-70 h single process at 0.4-0.65M nodes/s:
NOT launched (limit 6 h). Needs ~4x pruning or a prefix-split over >= 12 cores.

## Tests
tests/test_census_counts.py: C DFS == Python DFS == CP-SAT native enumeration (K30, F7-free, no K31) for (7,5,5)=10,
(8,6,5)=260, (8,6,6)=286 by default; with E757_SLOW=1 also (9,7,6)=8570 and (10,8,6)=79,488 (slowtest/run.log).

## Follow-up: parallel prefix-split census for (14,12,alpha<=8)  [launched; not finished]
Code: `mode=prefixes depth=k` and `pre=i-k,...` options in e757/c/ordered_dfs.c; driver e757/ordered_dfs_split.py
(P niced processes, per-prefix `.jsonl.gz` + `.done` markers, resumable); post-processing postprocess.py (filter.c is now
parametric in N; cores_n14.txt via dump_cores.py).
Validation: k=2 split of (12,10,alpha<=7) gives 107 prefixes and exactly 2,226,490 solutions (187,004,606 nodes);
postprocess.py on that split output reproduces 1,113,245 / 754,235 / 395,039 / 313,774 / 54,243 realizable /
54,243 classes, 50/50 judge PASS (postprocess_validation_n12/). Tests: tests/test_census_counts.py
(`test_prefix_split_small` always; `test_prefix_split_n12_m10` with E757_SLOW=1).
Launch (2026-10-14 11:21 UTC): `bash scripts/start_job.sh experiments/20261014-1005-census-dfs/n14 24 python3 -m e757.ordered_dfs_split 14 8 12 3 3 experiments/20261014-1005-census-dfs/n14/results --refl --nice 10`
(depth 3 = 2537 prefixes, P=3, `--refl` keeps one representative per reflection orbit). Resume after a restart: rerun the same
command (finished prefixes are skipped). When n14/results/n14_m12_TOTAL.json exists run
`python3 experiments/20261014-1005-census-dfs/postprocess.py 14 8 12 experiments/20261014-1005-census-dfs/n14/results n14_m12 3`.
Expected enumeration cost 8e10-1e11 nodes = 36-44 CPU-hours at 0.65M nodes/s (unloaded); 3 niced workers got only ~25% CPU
each while the sweep and another census ran, so expect finish ~03:00-06:00 UTC on 2026-10-15 if cores free up after
~13:30 UTC (the 24 h limit ends 11:21 UTC on 10-15; rerun to resume). Post-processing estimate from (12,10) rates:
filter ~0.2 ms per raw solution, realization ~2-4 ms per O' pattern / P; with ~1e6 solutions this is well under an hour.
