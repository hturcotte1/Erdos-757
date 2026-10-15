# Timings of the ordered-midpoint DFS (Python vs C) and a node-count estimate for n = 16

All numbers below are copied from the files in this folder (`results.json`, `estimate_n16.txt`, `rate_n16.txt`,
`run.log`). The README was written afterwards (2026-10-15) from those files; nothing was re-run.
Note: `run.log` and `job.pid` are git-ignored (see `.gitignore`), so `run.log` exists only in the working copy
of the machine that ran the job; its content is quoted here.

## Question
How fast is the exhaustive DFS over ordered midpoint hypergraphs (class O: linear, midpoint-injective, monotone
K30 midpoints, optionally F7-free) with the minimum independence number, in the pure-Python engine
`e757/ordered_dfs.py` versus the C engine `e757/c/ordered_dfs.c` (wrapper `e757/ordered_dfs_c.py`)? Is a direct
enumeration of n = 16 (alpha <= 9) conceivable?

## Method
`run_timings.py` calls `min_alpha(n, forbid_f7=...)` (Python, n = 5..10) and `run(n=n, mode="min", f7=...)` (C,
n = 5..12) for f7 in {1, 0} and records the minimum alpha found, one optimal edge list, the number of DFS nodes and
the wall-clock seconds. The n = 16 estimate uses the Knuth-style random-descent estimator of the C engine
(`mode=estimate`, see the usage line in `e757/c/ordered_dfs.c`); the rate probe is a 60-second enumeration run at
n = 16. Float-free: all objects are integer edge lists.

## Exact command
`run.log` header: `# started 2026-10-14T00:57:48Z max 0.5h`,
`# command: python3 experiments/20261014-0005-ordered-dfs/run_timings.py` (from the repo root; writes `results.json`).
The commands that produced `estimate_n16.txt` and `rate_n16.txt` are NOT recorded in the folder (see open issues).

## Results (machine load at the time: `results.json["load"]` = 11.13, 12.00, 12.54 on 4 cores, so seconds are inflated)
Minimum alpha, DFS nodes, seconds. "F7" = F7-free enforced.

| n | alpha (F7) | alpha (no F7) | Python nodes / s (F7) | C nodes / s (F7) | C nodes / s (no F7) |
|---|---|---|---|---|---|
| 5 | 4 | 4 | 20 / 0.0 | 20 / 0.0 | 20 / 0.0 |
| 6 | 4 | 4 | 36 / 0.0 | 36 / 0.0 | 36 / 0.0 |
| 7 | 5 | 4 | 419 / 0.02 | 419 / 0.0 | 121 / 0.0 |
| 8 | 5 | 5 | 748 / 0.05 | 748 / 0.0 | 748 / 0.0 |
| 9 | 6 | 6 | 27,650 / 1.73 | 27,650 / 0.03 | 28,221 / 0.03 |
| 10 | 6 | 6 | 57,701 / 5.38 | 57,701 / 0.11 | 58,743 / 0.08 |
| 11 | 7 | 7 | not run | 4,322,495 / 6.8 | 4,402,249 / 6.16 |
| 12 | 7 | 7 | not run | 30,060,333 / 58.03 | 30,268,852 / 54.09 |

(Python timings for the no-F7 column at n = 9, 10: 1.42 s and 4.62 s.) Python and C visit identical node counts
for n <= 10 (same search tree). C is about 50x faster than Python at n = 10 and runs at roughly 0.5-0.65 million
nodes per second at n = 11, 12 under this load. The minimum alpha values reproduce 4, 4, 5, 5, 6, 6, 7, 7 for
n = 5..12 with F7-freeness (F7 matters only at n = 7, where alpha drops to 4) [verified-here; same values as
experiments/20261013-2257-chyp-table].

n = 16 (`estimate_n16.txt`, two estimator runs, 300 probes each):
- run 1: estimated DFS calls 5.804e13 (stderr 1.46e13), estimated surviving nodes 3.233e12;
- run 2: estimated DFS calls 1.18e14 (stderr 5.15e13), estimated surviving nodes 8.269e12;
- per-level estimates (nodes at depth 11 / 12): run 1: 2.14e12 / 5.59e11 (maximum at level 11); run 2: 3.67e12 / 4.13e12
  (maximum at level 12).
`rate_n16.txt`: load line `10.25 11.21 12.12 10/155 11013`, then two 60 s probes that both ended with
`timed_out=1`, `sols=0`: 4,009,984 nodes in one, 82,063,360 nodes in the other (still inside the level-2 / midpoint-2
branch of the search). The two probes differ by a factor of about 20 in speed; the folder does not say why.
[heuristic] (estimator variance is large: the two runs differ by a factor of two).

## Conclusion
[verified-here] for the timings and minimum alpha values at n <= 12 (C engine matches the Python engine node for
node up to n = 10). [heuristic] for the n = 16 numbers: a direct, unsplit enumeration needs on the order of 6e13 to
1.2e14 DFS calls, i.e. (dividing by 0.5 million nodes/s, an arithmetic step added in this README) about 1.2e8 to
2.4e8 CPU-seconds. A direct n = 16 search was therefore not attempted; later work used prefix-splitting at n = 14
(experiments/20261014-1005-census-dfs) and SAT/CP-SAT (experiments/20261014-0450-n16-cases,
experiments/20261014-0550-n16-layered). The engine itself underlies certificates L002, L003 and L004
(K41, K43, K45 in kb/known_results.md) but this folder only measured its speed.

## Open issues (could not be determined from the files)
- The exact arguments (T, m_min, m_exact, f7, progress, tl) of the n = 16 estimator and rate runs are not recorded.
- Why the two 60 s probes differ by about 20x in node count.
