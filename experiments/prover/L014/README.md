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

## Process notes (scheduling only; no effect on any list)
- 22:31 UTC: the kernel groups CPU time by session (`/proc/sys/kernel/sched_autogroup_enabled` = 1), so the two phase-2 jobs started by
  `sched_main.sh` (C and D) shared one CPU share and per-process nice values had no effect between sessions. The job D =
  `run_cells.py 21,15,8,3` was stopped after 5 min (its ext_d was killed; `stream.recurse` raised `RuntimeError: pipeline failed` as
  designed; no cell file had been written) and `sched_main.sh` was stopped (its running child C continued unchanged). `sched_main2.sh`
  re-runs D from scratch and the later phases, each job in its own session (`setsid -w`). The auxiliary session (`sched_aux.sh`, my own
  cross-checks) was given autogroup nice 19 so that it yields to everything else.
- 22:33 UTC: `stream.py` was changed by one line: each chunk pipeline of `stream.recurse` is started as `setsid -w bash -c ...` (own
  session, hence own CPU share; `setsid -w` returns the pipeline's exit code). The pre-change file is kept as `stream_v1.py`
  (`diff stream_v1.py stream.py` shows only this line and the docstring). Cells computed before the change (phase 1, C, D2, the D=4 cells of E,
  the C7/C8 runs) used the old version, F, G, T, R4 the new one; the lists cannot differ (same commands), and the new version was
  checked on (14,12,6,3) (one chunk) and (17,14,7,3) (two chunks, 10,162 inputs): identical lists and branch data.
- 23:02 UTC: `sched_main2.sh` (main loop only) was replaced by `sched_main3.sh`, which starts G = (19,17,8,3) as soon as C is complete
  (G does not need (21,15,8,3)), F = (22,18,9,3) when D2 is complete, then T; the running D2 continued unchanged.
- 23:21 UTC: `post_checks.sh` (still waiting for the top cell, nothing run) was replaced by `post_checks2.sh`: the same checks, with the
  pruned and unpruned re-runs of the final step and the classifier in parallel sessions.

## Exact commands
`reproduce.sh` (all of them, in order).

## Results
- C1: 104 keys visited by `engine.cell(23,21,10,3)` (86 direct, 18 recursion, 24 branches); every decomposition list (455; 1,039 for
  the Delta<=4 control tree; 25 for the MD=9 trees) equals an independent brute force; the top branch is d=3, t'=9, S'=3 with exactly
  five decompositions of (22,18).
- C3 (main run, from an empty directory): (14,10,5,3) 45,229 (direct), (15,13,6,3) 949,522, (18,14,7,3) 799,342, (21,15,8,3) 232,759,
  (19,17,8,3) 29,898, (22,18,9,3) 94,513, (21,18,9,3) 0, ... (`cells_summary_output.txt`, `big_table_output.txt`); top cell (23,21,10,3): 133,804 inputs, `ext_d 22 9 10 3 2` nodes=48,029,683 hits_F7free=4,249 hits_in_C=0 bad_tau=0: EMPTY.
- C4: unpruned final step 10,986 extensions with tau >= 10; `filt`: 0 members of C; `pyverify` independently: hits=10986 nonlinear=0 F7=6737 F7free_P3_violated=4249 members_of_C=0 disconnected=4824 F7free_connected=280; brute force on 246 sampled
  inputs: identical hit sets, inputs=246 equal=246 different=0 hits=310 hits_inC=0 hits_F7=153 hits_P3fail=157 hits_disconnected=66 tau_checked=228 cover_full_checked=5 dsets=1134655.
- C5: control cell(23,21,10,4) with the same machinery: 699 classes, identical to L012's 699 (FOUND lines and recomputed canonical
  forms; its d=3 branch again 0 in C, its d=4 branch 2,178 inputs, 1,822,642,633 nodes, 14,290 in C as in L012); A_base in cell(14,12,6,4); 2,910 / 54,243 census patterns in the Delta<=4 lists, 700 / 39,309
  of them (Delta<=3) in cell(14,12,6,3) / cell(12,10,5,3).
- C6: every list equal to the worker's / probe's / L012's / L013's where they exist: vs W1735: common cells 128, equal 128, different 0; vs W1925: common cells 130, equal 130, different 0; vs W1720: common cells 114, equal 114, different 0; vs L012: common cells 117, equal 117, different 0; vs L013: common cells 114, equal 114, different 0.
- C7: unchanged engine = streamed driver on 9 cells (identical lists and branch counters).
- C8: recursion = direct on (14,10,5,3), (13,10,5,3), (12,10,5,3) (MD=9), (15,11,6,3), (12,10,5,3) (L008's direct runs), (17,11,6,2),
  (20,11,7,3), (20,12,7,2) (L013's direct runs) and nine more recursion cells of phase E by own direct runs ((17,11,6,2) 114, (20,12,7,2) 38, (20,11,7,3) 45, (19,12,7,2) 1, (20,11,7,2) 1, four empty); the own direct run of (14,12,6,3) was stopped after 24 min without result.
- C9: audit 145 cell files, 28,547 representatives, 0 problems; the empty sub-list (21,18,9,3) re-validated unpruned (5,078 extensions, none a connected member of C).
- C10: C23 = B12 U (10^9 + 7919 B11) is a 23-point (4,5)-set with h = 14.

## Conclusion
Theorem 1 (certificate L014): no member of C has (n, m, tau) = (23, 21, 10) and maximum degree <= 3. With L012 Theorem 1 this gives
h(A) >= 14 for every 23-point (4,5)-set, hence f(23) = 14 (C23 attains it), and no (4,5)-set with at most 24 points beats 4/7.
Tag: [verified-here] conditional on referee acceptance (computer-assisted); f(23) = 14 [derived-here].
