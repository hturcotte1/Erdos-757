# Realizability-CEGAR witness searches at the record-feasible sizes n = 18, 20, 22, 23, 25 (all UNKNOWN)

Written 2026-10-15 from the files in this folder (`run_sweep.py`, `run_after_streams.sh`, `results/*.json`,
`run.log`). `run.log` and `job.pid` are git-ignored; the `results/*.json` files are tracked.

## Question
For the sizes where beating 4/7 is not excluded by Henning-Yeo (kb/00_START_HERE.md section 4: n = 18, 20, 22, 23,
25, ...), does the CEGAR solver `e757.cpsat_model.solve_realizable` find a (4,5)-set with h <= T, where T = h
needed (18: 10, 20: 11, 22: 12, 23: 13, 25: 14) and m = the number of 3-APs required by Henning-Yeo (START_HERE
table)? A SAT answer would be a record candidate (the script passes it to `scripts/new_claim.py`); UNSAT would be
a restricted nonexistence statement; UNKNOWN is neither.

## Method (from the docstring and code of `run_sweep.py`)
CP-SAT model of an ordered midpoint hypergraph with: linearity, midpoint injectivity, lazy F7-freeness, K30
(monotone midpoints), K31 (no medial triangle), forbidden cores from `data/forbidden_ordered_n7.json` and
`data/forbidden_ordered_n8.json` (literal budget 1,000,000), and alpha <= T encoded eagerly (n = 18: `eager=True`)
or in a hybrid way (n >= 20: `eager=20000`: a random sample of 20,000 (T+1)-subsets as clauses plus lazy cuts).
Every candidate hypergraph is passed to `realize_exact`; a failure is turned into a minimal core and learnt
(sound for every m). `m_exact` is fixed per case, `m_min = 0`. Cases are resumable (a case is skipped if its
results JSON exists). Time limit per case: 3600 s for n = 18, 20, 22; 1200 s (= 3600/3) for each of the three m
values at n = 23 and n = 25. 3 CP-SAT workers.

## Exact command
`run.log` header: `# started 2026-10-14T08:08:28Z max 9h`, `# command: bash experiments/20261014-0030-feasible-sizes/run_after_streams.sh`.
That script waits until no `layer1.py` process runs (the n = 15 layer-1 streams of experiments/20261014-0550-n16-layered),
then runs `python3 experiments/20261014-0030-feasible-sizes/run_sweep.py 3600 3` with `PYTHONPATH` set to the repo root.
(An earlier launch around 00:30 UTC on 2026-10-14 died in the 04:40 UTC container restart without saving results, see
journal/LOG.md entry 2026-10-14T04:50Z; `run_sweep.py` was written afterwards, at 04:47, with per-case resumable JSONs.
It is also invoked at the end of experiments/20261014-0450-n16-cases/run_all.sh, but that case split was abandoned after 4 cases, journal/LOG.md entry 2026-10-14T05:50Z.)

## Results (`results/*.json`; all status UNKNOWN)
| file | n | T | m | eager | wall s | alpha cuts | solver solves | F7 cuts | CEGAR rounds / learnt cores |
|---|---|---|---|---|---|---|---|---|---|
| n18_T10_m16.json | 18 | 10 | 16 | True | 3600.1 | 0 | 1 | 0 | 0 / 0 |
| n20_T11_m18.json | 20 | 11 | 18 | 20000 | 3600.0 | 0 | 1 | 0 | 0 / 0 |
| n22_T12_m20.json | 22 | 12 | 20 | 20000 | 3604.9 | 0 | 1 | 0 | 0 / 0 |
| n23_T13_m19.json | 23 | 13 | 19 | 20000 | 1200.1 | 123 | 4 | 0 | 0 / 0 |
| n23_T13_m20.json | 23 | 13 | 20 | 20000 | 1206.1 | 533 | 15 | 1 | 0 / 0 |
| n23_T13_m21.json | 23 | 13 | 21 | 20000 | 1200.1 | 940 | 24 | 0 | 0 / 0 |
| n25_T14_m21.json | 25 | 14 | 21 | 20000 | 1208.6 | 373 | 10 | 0 | 0 / 0 |
| n25_T14_m22.json | 25 | 14 | 22 | 20000 | 1199.2 | 617 | 16 | 0 | 0 / 0 |
| n25_T14_m23.json | 25 | 14 | 23 | 20000 | 1200.2 | 699 | 18 | 0 | 0 / 0 |

Model sizes (clause counts, from `stats.constraints`): n = 18: monotone 50,388, medial 82,824, cores 200,124 clauses
(755,616 literals); n = 20: 94,962 / 170,544 / 147,288 (372,096 lit.); n = 22: 168,245 / 324,786 / 276,507 (702,240 lit.);
n = 23: 219,604 / 437,437 / 370,139 (942,172 lit.); n = 25: 361,790 / 761,530 / 283,360 (566,720 lit.). Model build
time 5.8 s (n = 18) to 18.6 s (n = 25).
In all nine cases `rounds` and `learnt` are 0 and `fail_kinds` is empty: the solver never returned a candidate hypergraph
to be tested by `realize_exact`, so the realizability half of the CEGAR loop was never exercised.
No case returned SAT, so no `new_claim.py` call was made and no set exists in this folder.

## Conclusion
[heuristic] No record candidate was found at n = 18, 20, 22, 23, 25 within the stated time limits, and nothing was
refuted: all nine cases ended UNKNOWN (timeout). This is weak negative evidence only and is not a nonexistence
statement. It is recorded as dead end D18 (kb/dead_ends.md), feeds journal/LOG.md entries of 2026-10-14T09:25Z, 11:20Z and 13:25Z, and is cited in K42 of kb/known_results.md; it produced no K-row and no certificate of its own.

## Open issues
- The folder does not record the machine load during the sweep (other census jobs were running).
- It is not determinable from the files whether longer runs or more workers would change any status.
