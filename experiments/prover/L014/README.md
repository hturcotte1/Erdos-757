# L014 (prover): the maximum-degree-3 case of the record cell (23,21,10) is empty, so f(23) = 14

Certificate: results/proofs/L014-f23-equals-14.md. Started 2026-10-17 21:46 UTC. Everything here was re-run from scratch; no file of
the worker's or probe's runs is read by the computations (they are only compared with, C6).

## Question
Is the list `cell(23,21,10,3)` of the L012 engine (connected members of C = linear, F7-free, e(S) <= |S|-2, with 23 vertices, 21 edges,
tau = 10 and maximum degree <= 3) empty?  By L012 Theorem 1 this decides whether a 23-point (4,5)-set with h = 13 exists (Q14).

## Method
- Binaries rebuilt from ../L012/indep/*.c with L012's commands, byte-identical to ../L012/bin (`build_check_output.txt`);
  `engine.py`, `decomp22.py` byte-identical copies of L012's.
- `stream.py`: streamed twins of `engine.direct` / `engine.recurse` (same binaries, same branches, decompositions, inputs and calls;
  the lines flow through `ext_d | awk | filt | awk | cut | canon | awk | sort -u` pipelines with files on disk instead of Python
  lists). The unchanged engine was OOM-killed on these cells in the probe's run (13.8 GB). Equivalence: by construction (docstring,
  certificate Step 2) and by `equiv_check.py` (unchanged engine vs streamed driver on 9 cells, `equiv_check_output.txt`).
- `run_cells.py`: computes a list of cells with `engine.cell` (streamed unless `--orig`), one JSON line per cell in out/progress.jsonl.
- `tree.py`: dry run of `engine.cell` (which cells it visits); `listB.txt`, `listE.txt`: the scheduling groups.
- Main run: empty `out/cells`, MD = 10, nice 5; phase 1 in parallel: A = (14,10,5,3) (direct, NPROC=1), B = the 97 other cells that do
  not need it (NPROC=1); then `sched_main.sh`: C = (15,13,6,3), (18,14,7,3) and D = (21,15,8,3) in parallel (NPROC=1 each); then
  F = (22,18,9,3) (NPROC=2) with G = (19,17,8,3) (NPROC=1); then T = (23,21,10,3) (NPROC=2).
- Checks: `decomp_check.py` (decompositions vs brute force, every branch), `compare_cells.py` (every list vs the worker's, probe's,
  L012's, L013's), `crosscheck_direct.py` and MD = 9 recursions (recursion vs direct), `post_checks.sh` (final step without pruning,
  brute force `bf_final.py` on a sample, the Delta <= 4 control cell(23,21,10,4) vs L012's 699 classes, A_base), `audit_sample.py`
  (pure-Python re-verification of sampled representatives), `c23_construction.py` (explicit 23-point set with h = 14).
- Resources: 4 cores shared with referees (load 7 to 10), 15 GB RAM, 21 GB free disk at the start; nothing large is kept in memory;
  raw hit streams never touch the disk (only per-chunk input files and the distinct canonical forms); out/ is git-ignored.

## Exact commands
`reproduce.sh` (all of them, in order).

## Results
«to be filled»

## Conclusion
«to be filled»
