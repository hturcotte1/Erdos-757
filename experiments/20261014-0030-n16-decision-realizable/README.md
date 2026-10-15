# n = 16, T = 9 via realizability-CEGAR (m in {13, 14}): run killed by a container restart, NO RESULT

Written 2026-10-15 from the only files present: `run.log` (git-ignored) and `job.pid` (git-ignored). The folder has
no script and no result file.

## Question
Same as experiments/20261014-0030-n16-decision, but with the CEGAR engine `solve_realizable` (each failure of
`realize_exact` becomes a learnt minimal core), so that UNSAT would be a statement about REALIZABLE hypergraphs
directly: is there a 16-point (4,5)-set with h <= 9 (ratio 9/16 < 4/7), with m in {13, 14} 3-APs?

## Method and exact command
`run.log`: `# started 2026-10-14T00:44:18Z max 2h`,
`# command: python3 experiments/20261014-0030-n16-decision/run_realizable.py 13 14 6500 2`
(arguments M_MIN=13, M_MAX=14, TIME=6500 s, WORKERS=2). The script is `experiments/20261014-0030-n16-decision/run_realizable.py`:
`solve_realizable(16, 9, m_min=13, m_max=14, eager=True, monotone=True, medial=True, cores=<n<=8 library>,
core_lit_budget=1_000_000)`; it would have written `results/realizable_n16_T9_m13_14.json` (inside the n16-decision
folder). The job pid file contains 5786.

## Result
None. `run.log` contains only the two header lines (no `DONE` line) and no result JSON was ever written. The job was
one of the background jobs that died in the container restart around 04:40 UTC on 2026-10-14 without saving anything
(journal/LOG.md, entry 2026-10-14T04:50Z: "all background jobs died (n=16 CP-SAT decision m=13/m=14, realizable-CEGAR,
sweep at n=18) with no results saved").

## Conclusion
No scientific conclusion. [heuristic] status of the question it targeted (does a realizable 16-point set with h <= 9
exist?) is unchanged: it remains open. Later attempts: experiments/20261014-0450-n16-cases (4 of 30 cases, all
TIMEOUT), experiments/20261014-0550-n16-layered, experiments/20261014-1200-census-invariants and the sweep in
experiments/20261014-0030-feasible-sizes; see dead end D15 in kb/dead_ends.md (which cites other folders).

## Open issues
- The folder does not show whether the job was killed after 4 minutes or after 4 hours; only the LOG entry above says it
  died with the restart (the restart time is quoted there as "~04:40 UTC").
