# n=16, T=9: abstract decision with realizability-derived constraints

Question: does an ordered midpoint hypergraph on 16 vertices exist with alpha <= 9, F7-free, linear,
midpoint-injective, satisfying the exact realizability consequences K30 (monotone midpoints), K31 (no
medial triangle) and the forbidden cores of data/forbidden_ordered_n7.json + _n8.json?  (HY forces m in {13,14};
the two cases are run separately with m exactly 13 and 14.)

## Method [verified-here for the constraint code; no result was produced, see Results]
e757/cpsat_model.py: `enumerate_solutions(16, 9, m, monotone=True, medial=True, cores=..., core_lit_budget=2.5e6)`
(eager alpha<=9 encoding, lazy F7, reflection lex-leader, blocking clauses; sound because m is fixed).
Cores are added by increasing number of edges until a 2.5M-literal budget is hit (so only the smallest
cores are used at n=16; the 44 n<=7 cores alone are 2.6M literals).  For an `extra_ap` core the clause is
NOT(all S) OR e[T]; for all 38 extra_ap cores S+{T} violates (a)/(b), so this equals the plain no-good.
Every solution found is passed to `e757.realizability.realize_exact`; realizable ones to scripts/new_claim.py.
Exact command (job started 00:31 UTC, 2 workers each, 6500 s solver limit):
    python3 run_decide.py 16 9 13 6500 2   and   python3 run_decide.py 16 9 14 6500 2
Output: results/n16_T9_m13.json, results/n16_T9_m14.json (+ _solutions.jsonl.gz), logs m13.log, m14.log.
The machine was heavily loaded by other jobs (load ~10 on 4 cores).

## Soundness [verified-here]  (tests/test_cpsat_model.py)
* all realizable patterns (realize_exact True) of the full n<=7 census satisfy K30/K31/cores;
  the constraints cut a positive number of non-realizable patterns; 3000 random n=8 patterns likewise;
* CP-SAT clause set agrees with an independent python checker on 150 random n=7 patterns;
* the seven record patterns of data/small_records.json satisfy all constraints;
* min alpha with all constraints on (cores<=4 edges, HY) is still 5,6,6,7,7 for n=8..12.
Clause counts: n=16 monotone 24752, medial 36400; n=12: 4290 / 4488; cores see results json.

## Results (filled in 2026-10-15 from the files)
NONE. `results/` holds only `n16_T9_m13_solutions.jsonl.gz` and `n16_T9_m14_solutions.jsonl.gz`, both 0 bytes (truncated gzip streams: `zcat`
reports "unexpected end of file"); `m13.log` and `m14.log` are empty; no `n16_T9_m*.json` result file exists. `run.log` header:
`# started 2026-10-14T00:31:37Z max 2h`, `# command: bash -c python3 experiments/20261014-0030-n16-decision/run_decide.py 16 9 13 6500 2 > .../m13.log 2>&1 & python3 .../run_decide.py 16 9 14 6500 2 > .../m14.log 2>&1 & wait`.
Both solver runs died in the container restart around 04:40 UTC on 2026-10-14 without saving anything (journal/LOG.md, entry 2026-10-14T04:50Z).
The third job mentioned above (`run_realizable.py 13 14 6500 2`) has its own folder, experiments/20261014-0030-n16-decision-realizable, also with no result.

## Conclusion
No scientific result about n = 16 came out of this folder [verified-here: the absence of results]. The soundness tests of the constraint code (previous
section) remain valid and are what later folders reuse (experiments/20261014-0450-n16-cases, 20261014-0550-n16-layered, 20261014-0030-feasible-sizes).
The question "does a class-O' hypergraph with alpha <= 9 exist on 16 vertices?" stays open; see dead end D15 in kb/dead_ends.md (which cites other folders). Lesson recorded in the
LOG: every long job must write per-case resumable JSONs (done in the folders above).
Alternative engine added: `solve_realizable` (CEGAR on realizability: each realize_exact failure becomes a
minimal core learnt for all embeddings); UNSAT there is a statement about REALIZABLE hypergraphs directly.

Third job (started 00:44 UTC): `run_realizable.py 13 14 6500 2` = solve_realizable(16, 9, m in 13..14) with the
same constraints; log experiments/20261014-0030-n16-decision-realizable/run.log, result
results/realizable_n16_T9_m13_14.json.  Sweep job: experiments/20261014-0030-feasible-sizes/ (run.log,
results/n{18,20,22,23,25}_T*.json; n=18 eager, others hybrid eager sample 20000 + lazy cuts).
Status at hand-back (00:50 UTC): all three n=16 / sweep jobs still running; no result yet. (Final state: see Results below; the jobs died at the 04:40 UTC restart.)
