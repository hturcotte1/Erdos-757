# L016 prover folder: I11 on C at n = 27 and f(27) = 16

Certificate: results/proofs/L016-i11-n27-f27-equals-16.md (tags and full statements there). Prover run 2026-10-20 23:35 to 2026-10-21 01:09 UTC.

## Question
Does I11 (11 tau <= 3n + 2m) hold for every member of the class C (linear, F7-free, e(S) <= |S|-2) with n = 27 vertices? Then f(27) = 16.

## Method
- The window-cell induction of L007-L013 at n = 27: arithmetic (arith16.py) leaves five violator cells (27,13,10,2), (27,14,10,3), (27,18,11,2), (27,19,11,3), (27,25,12,3).
- Each is computed by L012's engine.py (byte-identical) through L014's streamed driver stream.py (byte-identical), from cell directories seeded ONLY with the 198 refereed lists of L013 and L014; plan16.py shows that exactly 49 further lists are needed.
- Run A (run_A.sh): the 45 small lists (incl. the four sparse top cells) with bin/ext_d = L012's ext_d.c with MAXP 640 (one line; certificate Step 0.6).
- Run F (run_F1.sh with NP=3): the four heavy lists (24,16,9,3), (25,19,10,3), (26,22,11,3), (27,25,12,3) in out/cellsF with fast/bin/ext_d = bin/ext_d_fast (src/ext_d_fast.c: the same program with a branching enumeration of the minimum covers instead of Gosper's loop; certificate Step 0.7, Lemma B; about 17x faster on 25-vertex inputs).
- Run B2 (run_B2.sh): (26,22,11,3) and (27,25,12,3) with ext_d_fast from the worker's cell(25,19,10,3) (cross-check / item (b) of the task).
- Checks: decomposition brute force (decomp_check.py on the dry-run trees), regressions of ext_d_fast against ext_d (regress.py, run_regress_full.sh), MAXP 256 vs 640, audits of the stored lists (filters16.py), closure checks (closure.py), unpruned final steps (ext_validate.py), comparison of all 49 lists and their branch data with the worker's run (compare_cells16.py, compare_branches16.py), 8 random chunks of the worker's (25,19,10,3) run recomputed and compared (chunk_check.py, run_chunks.sh), the explicit 27-point set (c27_construction.py).
- Process notes: a first run B of (26,22,11,3) with the Gosper build and a first single-process start of run F were stopped at 23:49:50 UTC before writing any list.

## Exact commands
See reproduce.sh (every command, in order).

## Results
- Arithmetic (arith16_output.txt): the five open violator cells at n = 27 as in L013 C1; (27,23,12), (27,24,12) excluded by counting.
- Plan (out/plan_all_from_refereed.txt): 49 lists to compute beyond the 198 refereed seeds.
- Run A (45 lists, MAXP 640 Gosper ext_d): the four sparse top cells (27,13,10,2), (27,14,10,3), (27,18,11,2), (27,19,11,3) are EMPTY; unpruned final steps: every extension with the required tau is disconnected (extval_sparse_output.txt).
- Run F (ext_d_fast): cell(24,16,9,3) = 39,568 classes (identical to the worker's, identical counters: nodes 6,104,447,853 etc.). cell(25,19,10,3) = 35,645 classes (2,082,993 inputs, nodes 23,128,213,292, identical to the worker's), cell(26,22,11,3) = 36 classes, cell(27,25,12,3) = EMPTY (334 inputs, no extension in C; unpruned: 36 extensions with tau >= 12, all disconnected). Run F 23:50-01:05 UTC, rc=0.
- Run B2 (ext_d_fast, from the worker's cell(25,19,10,3); cross-check): cell(26,22,11,3) = 36 classes, cell(27,25,12,3) = EMPTY (334 inputs; 36 F7-free extensions with tau >= 12, none in C; unpruned: 36 extensions, all disconnected); identical to the worker's lists and counters.
- All 49 new lists (runs A and F) identical to the worker's run, with identical branch data (compare_cells_output.txt, compare_branches_output.txt); run B2 identical too.
- 8 random chunks of the worker's cell(25,19,10,3) run recomputed with ext_d_fast: identical (chunk_check_output.txt); chunks 1, 40, 74 also with the Gosper build: identical (chunk_check_gosper_output.txt).
- Run G: the top cell (27,25,12,3) with the Gosper build bin/ext_d from run F's lists: 0 classes, same counters (out/logs/run_G.log, progress_G.jsonl).
- Run F's own heavy lists: audit OK (audit_F_output.txt), closure OK (closure_F_output.txt).
- Audits (audit_output.txt): 49 lists, 83,545 classes, all OK; closure checks (closure_output.txt): 0 problems.
- Regressions (out/regress/): ext_d_fast byte-identical to ext_d on 4,600 sampled inputs; on all 133,804 inputs of L014's top cell the counters equal L014's; MAXP 256 vs 640 identical on 3,000 inputs.
- C27 (c27_construction_output.txt): 27-point (4,5)-set with h = 16.

## Conclusion
I11 holds on C for n = 27 (all five open violator cells empty), hence for all n <= 27 with L013; f(27) = 16 (lower bound from I11, explicit witness C27 with h = 16); no 27-point (4,5)-set beats 4/7; for n <= 30 a record is not excluded only at n = 25, 29, 30. All 49 new lists were computed here from the refereed seeds (runs A and F) and agree with the worker's run in every list and every counter. Status: certificate SUBMITTED, unrefereed. Deviations: ext_d with MAXP 640 (one line) and, for the four heavy cells, ext_d_fast (Lemma B; regressions C6).
