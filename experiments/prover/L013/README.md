# L013 (prover): I11 on the class C for n <= 26 by the window-cell induction, steps n = 23, 24, 25, 26

Certificate: results/proofs/L013-i11-on-C-n-le-26.md. Date: 2026-10-17. Tags: computations [verified-here] (exact; unrefereed until the
certificate is accepted); the theorem is [verified-here] conditional on referee acceptance.

## Question
Does I11 (11 tau <= 3n + 2m) hold on C (linear, F7-free, e(S) <= |S|-2) for n = 23, ..., 26, extending L011 (n <= 22)?

## Method
1. `arith13.py` (exact integers): violator cells (connected, K8 window, slack < 0) for n = 23..27, degree bound floor((s+8)/2) from I11 at
   n-1, counting exclusion 3m > Delta n; record cells; lower bounds; degree bounds in the record cells.
2. `run_top.py` runs the L012 engine (`engine.py`, byte-identical copy; binaries built from experiments/prover/L012/indep, byte-identical
   to ../L012/bin) on the twelve open top-level cells, in induction order, from an EMPTY cell directory `out/cells` (NPROC=2, nice 19).
3. Audits and cross-checks: `check_cells.py` (pure-Python re-verification of all 30,855 representatives, branch sets, decompositions
   against the independent generator `decomp_bf.py`, input counts, ext_d counters), `compare_runs.py` (L012's lists; the worker's runs),
   `crosscheck_direct.py` (direct enumeration of recursion cells with MD raised), `ext_validate.py` (final extension steps without
   pruning + Python filter; brute force on sampled inputs), `abase_control.py` and `positive_control.py` (positive controls),
   `n27_remark.py` (where the method stops at n = 27).

## Exact commands
`bash reproduce.sh` (all of them, in order). `run_n26_after.sh` and `run_crosscheck_after2.sh` are only the scheduling helpers that
were used to start the n = 26 run and cross-check batch 3 after the previous job (reproduce.sh runs everything sequentially instead);
batch 2 was stopped after its first four cells and its remaining cells were run by `run_crosscheck2b.sh`.

## Results
- All twelve top-level cells (23,13,9,2), (23,14,9,3), (23,20,10,3), (24,12,9,2), (24,13,9,3), (24,18,10,3), (25,16,10,2),
  (25,17,10,3), (25,22,11,3), (26,14,10,2), (26,15,10,3), (26,21,11,3) are EMPTY (`top_results.jsonl`); six more cells are excluded by
  counting. Hence I11 holds on C for n <= 26.
- 167 cells computed (105 direct, 62 recursion; 91 non-empty; 30,855 classes): `cells_table.tsv`, `cells_summary_output.txt`,
  tracked lists `cells.tar.gz`. Audit: 0 problems (`check_cells_output.txt`).
- Identical (representatives and branch counters) to L012's lists on all 105 common cells and to the worker's 167 cells
  (`compare_runs_output.txt`); arithmetic identical to the worker's (`compare_arith_output.txt`).
- Direct-enumeration cross-checks: `crosscheck_direct.jsonl`. Extension-step validation: `ext_validate_output.txt`.
  Positive controls: `abase_control_output.txt`, `check_cells_D4_output.txt`, `positive_control.jsonl`.
- n = 27: the cell (27,25,12,3) needs cell(23,21,10,3) (Q14) in the engine's recursion (`n27_remark_output.txt`).

## Conclusion
I11 holds on C for every n <= 26 (Theorem 1 of the certificate). No value of f(n) is decided (the I11 bound equals the Henning-Yeo
bound at n = 23..26); Q14 is untouched; n = 27 needs Q14 with this engine.
