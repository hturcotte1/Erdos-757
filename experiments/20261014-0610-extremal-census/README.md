# Partial CP-SAT censuses of extremal ordered patterns at (n, m, alpha) = (12, 10, <=7), (14, 12, <=8), (15, 13, <=9)

SUPERSEDED. The exhaustive censuses are in experiments/20261014-1005-census-dfs (certificates L002 for n = 12,
L004 for n = 14). This folder holds the earlier, time-limited CP-SAT enumerations. Written 2026-10-15 from the files
present (`census.py`, `run_chain.sh`, `run.log`, `results/`, `results_sets_n*.json`). `run.log`, `job.pid`,
`results/*_progress.json` and `results/*_solutions.jsonl` are git-ignored, so the solution streams (3.5 MB, 0.2 MB,
2.7 MB) exist only on the machine that ran the job; the tracked files are `results/*_partial_census.json`,
`results/n14_realizable_sets_partial.json`, `results/log12.txt` and `results_sets_n12.json` / `results_sets_n14.json`.

## Question
How many abstract class-O' extremal patterns (ordered, linear, midpoint-injective, F7-free, K30, K31, forbidden cores
with at most 4 edges) with exactly m = n-2 edges and independence number <= f(n) exist, and how many of them are
exactly realizable as (4,5)-sets? In particular, are extremal sets at n = 12 and n = 14 plentiful, and do any of
them beat 4/7 (they cannot at these n; this is a sanity and data-collection run)?

## Method (docstring of `census.py`)
Stage 1: `e757.cpsat_model.enumerate_native(N, T, M, ...)` enumerates all solutions (eager alpha and F7 clauses),
with a time limit; each solution is reduced to its canonical representative under reflection (`min(edges, reflected
edges)`). Stage 2: `realize_exact` on every canonical solution; realizable ones are turned into integer sets,
re-checked with `e757.core.alpha` and `is_45_set`, normalised affinely (translate min to 0, divide by gcd, lexicographic
minimum of the set and its reflection). Rigid patterns (AP-equation rank N-2) give exactly one affine class. A census
is marked finished (`*_census.json`) only if the enumeration status is EXHAUSTED; otherwise `*_partial_census.json`.

## Exact command
`run.log` header: `# started 2026-10-14T06:13:59Z max 6h`,
`# command: bash experiments/20261014-0610-extremal-census/run_chain.sh`. The chain runs
`python3 census.py 12 7 10 3600`, `census.py 14 8 12 7200`, `census.py 15 9 13 7200` (from the repo root, with
`PYTHONPATH=.`). Relaunch line (from the script header):
`bash scripts/start_job.sh experiments/20261014-0610-extremal-census 6 bash experiments/20261014-0610-extremal-census/run_chain.sh`.
`run_chain.sh` waits for a directly launched `census.py 12 7 10` run before starting; `results/log12.txt` (written 07:31) is
probably the console output of that directly launched run (the folder does not say so explicitly).

## Results (all TIMEOUT; none exhaustive) [verified-here for the counts, exact arithmetic and exact realization]
| (N, T, M) | enumeration status | raw solutions | classes up to reflection | exactly realizable | rigid | affine classes | unrealizable reasons | record-beating |
|---|---|---|---|---|---|---|---|---|
| (12, 7, 10), `results/n12_m10_partial_census.json` (3600 s, 8.5 solutions/s) | TIMEOUT | 30,559 | 29,228 | 4,448 | 4,448 | 4,448 | order-infeasible 23,272; forced extra AP 802; forced repeated difference 706 | none |
| (12, 7, 10), earlier run `results/log12.txt` | TIMEOUT | 26,974 | 25,924 | 3,980 | 3,980 | 3,980 | order-infeasible 20,613; forced extra AP 708; forced repeated difference 623 | none |
| (14, 8, 12), `results/n14_m12_partial_census.json` (7200 s, 0.2 solutions/s) | TIMEOUT | 1,474 | 1,409 | 146 | 146 | 146 | order-infeasible 1,178; forced repeated difference 44; forced extra AP 41 | none |
| (15, 9, 13), `results/n15_m13_progress.json` | progress file says RUNNING at 3956.7 s | 16,944 in the progress file (16,985 lines in the stream) | not processed | not processed | | | | |

For all realizable sets `all_h_equal_T` and `all_45` are true in the two census JSONs (h = 7 resp. 8, every set
passes `is_45_set`). `results/n14_realizable_sets_partial.json` holds 157 realizable 14-point integer sets (146 after
identifying reflections), `results_sets_n12.json` 4,448 sets and `results_sets_n14.json` 146 sets.
`known_sets` in the census JSONs reports that none of the known 12-point sets (three distinct sets, listed under five keys in the JSON) and neither `record_14` nor A_base
occurs among the enumerated patterns: the partial enumerations are samples of the extremal patterns, not covers.
No n = 15 census file exists: the chain was stopped by hand while the n = 15 stage was still enumerating
(journal/LOG.md, entry that launches the prefix-split job: "Stopped the CP-SAT census chain ... the (15,13) partial
count was of marginal value").

Comparison with the exhaustive census [verified-here, from experiments/20261014-1005-census-dfs]: at (12, 10, <=7)
the true numbers are 1,113,245 patterns up to reflection and 54,243 realizable classes (so the partial run above found
about 8% of the realizable classes); at (14, 12, <=8) the true number of saturated 14-point extremal classes is 2,910
(so the partial run found 146 of them). The "about 8%" is the ratio 4,448/54,243 computed in this README.

## Conclusion
Purpose achieved as a first look: extremal sets are plentiful at n = 12 and n = 14 (kb/known_results.md K40 uses the
3,980 figure of the earlier n = 12 run; K42 uses 1,474 / 157 / 146 for n = 14), and no record-beating set appeared.
The counts are lower bounds only (time-limited); the exact numbers are K41 (54,243) and K45 (2,910), both from the
DFS census. K36 (kb/known_results.md) also cites this folder.

## Open issues
- `results/log12.txt` (26,974 solutions) and `n12_m10_partial_census.json` (30,559) are two different time-limited runs of
  the same case; the folder does not say why the second run enumerated more in the same 3600 s limit.
- Exact stop time of the n = 15 stage is not recorded (the last write to `n15_m13_progress.json` is 11:57 on 2026-10-14).
