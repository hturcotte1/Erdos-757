# Independent pysat encoding of class O' (cross-check for certificates)

Question: provide a second, independent implementation of "does an ordered midpoint hypergraph of class O'
on n vertices with exactly m edges have alpha <= T?" (python-sat, written from the definitions in the docstring
of `e757/sat_indep.py`; it imports nothing from e757 and in particular not `e757.cpsat_model` / `ordered_dfs`).
Tags: everything below is [verified-here] unless marked [heuristic].

## Method
Variables x[i,j,k]; eager clauses for (a) midpoint injectivity, (b) linearity, (d) K30, (e) K31, alpha<=T
(one clause per (T+1)-subset), exactly-m (pysat CardEnc.equals, sequential counter), forbidden cores of
<=7 vertices (all images under increasing maps, plus reflections); F7 and the 8-vertex cores lazily
(after each model, find copies by backtracking, add the no-good, re-solve; incremental solver).
API: `decide(n,T,m,cores,forbid_f7,extra_unit,time_limit,vertex1,solver)` and `enumerate_all(...)`
(vertex1=0: vertex 1 is not a midpoint; vertex1=k>=2: edge (0,1,k)). Default solver glucose4 (interruptible).

## Tests (`python3 -m pytest -q tests/test_sat_indep.py`)
Checker and brute-force enumerator are written separately in the test file.
1. min alpha for n=5..11 equals the c_hyp (F7-free) column of experiments/20261013-2257-chyp-table/table.md
   (4,4,5,5,6,6,7), found by descending T until UNSAT, m free.
2. Full solution lists at T = min alpha for every m agree as sets with a plain-recursion brute force:
   n=8 (T=5: m=5 1396, m=6 132) and n=9 (T=6: m=3 208, m=4 5122, m=5 63444, m=6 44642, m=7 3186; 116602 total).
   Default pytest compares n=9 for m in {0..4,7}; `E757_SLOW=1` compares every m (done once: passed, 339 s under load).
   Also: eager/lazy/hybrid core modes agree at n=8; the vertex-1 case split partitions the solutions (n=9, m=3).
3. All seven record patterns (data/small_records.json) satisfy every family (checker), are SAT when every edge
   variable is fixed, and UNSAT for alpha <= h-1.
4. n<=7 census (patterns from experiments/20261013-2257-forbidden-library/enumerate.py,
   realizability by e757.realizability.realize_exact): every realizable pattern is accepted by the checker and
   by the solver; moreover the checker accepts exactly the realizable patterns for n=3..7 (cores complete there).
5. Negative controls (K30, alpha, linearity, shared midpoint, medial triangle, F7-only) are UNSAT.

## Timings (glucose4, m free; machine load average ~8 on 4 cores, so times are inflated ~2x)
`python3 run_timings.py glucose4 300` -> results/timings_glucose4.{log,json}

| n | T=min alpha: SAT | T-1: UNSAT |
|---|---|---|
| 8 | 0.07 s | 0.02 s |
| 9 | 0.06 s | 0.06 s |
| 10 | 0.3 s | 0.05 s |
| 11 | 0.15 s | 6.2 s |
| 12 | 0.34 s | 2.4 s |
| 13 | 0.77 s | 256 s |

## n=16 single case (T=9, m=14, vertex 1 edge (0,1,2)), 530609 clauses, build 0.3 s
- glucose4, 600 s limit: TIMEOUT (first solve not finished; 603 s wall) -> results/single_m14_k2_glucose4.json.
- cadical195, `timeout 700`: no answer within 700 s (killed; the pysat CaDiCaL cannot be interrupted).
Conclusion: [heuristic] a single n=16 case is not a minutes-scale job for this plain encoding with a generic SAT
solver; expect hours per case (or needs symmetry breaking / the case split by vertex 2 as in the CP-SAT driver).
This measurement was made on a loaded machine.

## Command for all 30 cases (not run; resumable, per-case JSON in results/case_m{M}_k{K}.json)
    (from repo root) bash scripts/start_job.sh experiments/20261014-0515-sat-indep 14 python3 experiments/20261014-0515-sat-indep/run_cases.py 3000
(`run_cases.py` skips existing JSONs, so rerunning resumes; status COMPLETE with n_solutions=0 means UNSAT, TIMEOUT cases
need splitting. Use `python3 run_cases.py TL m k` to run one case. The time limit is enforced for glucose4 only.)

## Gyarfas-Lehel colouring constraints (`gl_constraints=True|'L'|'R'|'LR'`, saturated m = n-2 only)
Proof (also in the module docstring): for a saturated pattern the left graph G_L ({i,j} for each AP (i,j,k)) is a tree on
{0..n-2} (each j>=1 has exactly one parent i<j), its proper 2-colouring c (c_0=0) makes both classes transversals of H, hence
n-T <= sum c_v <= T-1 whenever alpha <= T (|class| >= tau >= n-T, classes sum to n-1). Same for G_R on {1..n-1} with d_{n-1}=0.
Encoding: colour variables, x[i,j,k] -> (c_j xor c_i), totalizer atleast/atmost. [verified-here] soundness tests
(`test_gl_constraints_*`): the saturated record patterns (direct check of both class sizes and transversality, and SAT with all
edges fixed for L, R, LR), all 10 realizable saturated census patterns with n=4..7 at T = their alpha, and the saturated min alpha
for n=8..11 is identical for none/L/R/LR.

Timings (UNSAT at T = min alpha - 1, m = n-2, single process, machine loaded; `run_gl_timings.sh`, results/gl_timings.jsonl):

| n,T,m | solver | none | L | R | LR |
|---|---|---|---|---|---|
| 11,6,9 | glucose4 | 4.7 s | 4.0 | 3.6 | 4.1 |
| 11,6,9 | cadical195 | 3.7 | 3.2 | 2.9 | 3.2 |
| 12,6,10 | glucose4 | 6.7 | 1.9 | 4.9 | 0.47 |
| 12,6,10 | cadical195 | 3.9 | 0.34 | 2.6 | 0.39 |
| 13,7,11 | glucose4 (150 s limit) | TIMEOUT | TIMEOUT | TIMEOUT | TIMEOUT |
| 13,7,11 | cadical195 (180 s kill) | KILLED | - | - | KILLED |

Speedups: n=11 about 1.1-1.2x; n=12 3.5x (L) to 14x (LR) with glucose4, 11x (L) with cadical; n=13 no solver finished within
150-180 s with or without the constraints, so no factor can be given (the m-free decision of the first section took 256 s).
Evidence so far is one instance per size and noisy (loaded machine) [heuristic].

n=16, T=9, m=14, vertex 1 edge (0,1,2), variant LR, glucose4, 900 s: **TIMEOUT** (results/gl_n16_LR_glucose4.json). Not solved, so
the 30-case run is NOT recommended as is (command, if wanted anyway, is in the section above; add gl_constraints="LR" to the
enumerate_all call in run_cases.py first, only valid for m=14).
Third variant ("class minus v is not a transversal"): skipped, no compact encoding found (it needs per-(v, edge) auxiliary
variables, O(n^4)); it is only informative for the class of size exactly n-T.
