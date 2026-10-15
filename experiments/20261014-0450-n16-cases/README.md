# n=16, T=9: resumable case split (monotone K30 + medial K31 + forbidden cores, F7-free)

Question: is there an ordered midpoint hypergraph on 16 vertices with alpha <= 9 (hence m in {13,14} by
Henning-Yeo) satisfying the exact realizability consequences?  UNSAT everywhere => no such abstract
hypergraph => f(16) = 10 modulo Henning-Yeo (to be certified later by the independent DFS).

## Method
30 sub-instances: m_exact in {13,14} x vertex 1 either not a midpoint (k=0) or the midpoint of (0,1,k),
k=2..15.  Each is one `enumerate_solutions` call (e757/cpsat_model.py: eager alpha<=9 clauses, lazy F7,
K30, K31, cores added by size up to a 2.5M-literal budget, blocking clauses sound because m is fixed),
workers=1, 3000 s limit, 4 sub-instances in parallel.  The reflection lex constraint is dropped inside
cases (the case split on vertex 1 is not reflection-invariant; dropping a symmetry-breaking constraint is
trivially sound, it only costs a factor <= 2).  A TIMEOUT case is automatically split by the edge of vertex 2
((0,2,k), (1,2,k), or none).  If SAT all solutions are enumerated, each goes through
e757.realizability.realize_exact, and realizable sets through scripts/new_claim.py immediately.
Each finished sub-instance writes results/case_m{M}_k{K}[_v2_..].json atomically; the driver skips
existing JSONs, so a restart resumes (an interrupted sub-instance restarts from scratch).

## Command (one line, resumable; also runs the feasible-size sweep afterwards)
    bash scripts/start_job.sh experiments/20261014-0450-n16-cases 14 bash experiments/20261014-0450-n16-cases/run_all.sh
Progress: `python3 experiments/20261014-0450-n16-cases/aggregate.py` (rewrites the block below), log run.log.
Sweep results: experiments/20261014-0030-feasible-sizes/results/n{N}_T{T}_m{M}.json.

<!-- RESULTS START -->
Top-level cases finished: 4 / 30.  UNSAT: 0, SAT: 0, TIMEOUT (split further): 4.  Realizable sets found: 0.

| m | k (edge (0,1,k); 0 = none) | vertex-2 split | status | #solutions | #realizable | wall s |
|---|---|---|---|---|---|---|
| 13 | 0 | - | TIMEOUT | 0 | 0 | 3000 |
| 13 | 2 | - | TIMEOUT | 0 | 0 | 2997 |
| 13 | 3 | - | TIMEOUT | 0 | 0 | 3000 |
| 13 | 4 | - | TIMEOUT | 0 | 0 | 3000 |
<!-- RESULTS END -->

## Outcome (added 2026-10-15 from the files in `results/`) [verified-here for the counts; heuristic for the interpretation]
- `run.log` header: `# started 2026-10-14T04:47:38Z max 14h`, `# command: bash experiments/20261014-0450-n16-cases/run_all.sh`.
- Only 4 of the 30 top-level cases finished: m = 13 with k = 0, 2, 3, 4 (vertex 1 not a midpoint, or the midpoint of (0,1,k)); each ended TIMEOUT at
  about 3000 s with 0 solutions (`case_m13_k0.json`: wall 3000.1 s, 1 worker, constraints monotone 24,752 / medial 36,400 / cores 590,460 clauses
  (2,495,376 literals)). The cases k = 5, 6, 7, 8 of m = 13 left empty `case_m13_k*_solutions.jsonl` files (0 bytes; presumably started but never finished).
  No case file for m = 14 exists. All result files are time-stamped 05:37 on 2026-10-14.
- The aggregate block above (rewritten by `aggregate.py` on 2026-10-15) is the final state: 0 UNSAT, 0 SAT, 4 TIMEOUT, 0 realizable sets.
- The case split was abandoned (journal/LOG.md, entry 2026-10-14T05:50Z "n=16 case split abandoned"); the sweep that `run_all.sh` would have run
  afterwards was started separately (experiments/20261014-0030-feasible-sizes).

## Conclusion
[heuristic] No sub-case of the n = 16, alpha <= 9 decision could be settled by CP-SAT with K30/K31/cores in 3000 s; the TIMEOUTs are neither SAT nor UNSAT, so
nothing is proved about f(16). Recorded in dead end D15 (kb/dead_ends.md); the follow-ups are experiments/20261014-0550-n16-layered and
experiments/20261014-1200-census-invariants.
