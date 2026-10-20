# I11 on C at n = 27: probe (cell(26,22,11,3) chain)

Date 2026-10-17 21:48 UTC to 2026-10-18 03:49 UTC (6 h cap). Computation only, NOT refereed. Tag: [verified-here] as computations (exact integers, nauty canonical forms), unrefereed.

## Question
Can the I11 induction (11 tau <= 3n + 2m on the class C) be pushed to n = 27, i.e. are all five open violator cells of n = 27 empty: (27,13,10) D<=2, (27,14,10) D<=3, (27,18,11) D<=2, (27,19,11) D<=3, (27,25,12) D<=3 (arith_output.txt, same as 1720 folder)?

## Method
- Unchanged L012 engine.py / decomp22.py / decomps.py; streamed pipelines (mystream.py, copied from 1925) ext_d | grep HIT | filt | canon | sort -u. NPROC=1, nice -n 19, MD=10, never more than one worker.
- CELLDIR seeded (symlinks, nothing recomputed) with every existing cell file: 1925, 1735, 1720, 1645 (out/cells, cells25), L013, L012 (`seed_cells.txt`, 197 files, no content mismatch between overlapping files; D4 files from L012/L013 included).
- `plan.py` / `plan_output.txt` / `plan.json`: full recursion plan (every cell the engine needs, recursively, exists or missing, with input counts where known): 208 cells visited, 49 missing, of which 46 had to be computed (the other 3 are the heavy chain, below).
- `run_all.py` computed missing cells bottom-up, each under its own timeout (2400 s; the n=27 tops and heavy cells the remaining cap). `progress.tsv` has a line per finished cell; `cells_table.tsv` lists all 46 new cells.
- **Deviation from the unchanged binaries (necessary):** the first attempt at (26,16,10,3) aborted with `MAXP` (ext_d has a static bound of 256 on the number of candidate vertex pairs; with 25-vertex inputs of low degree there are up to 300 pairs). I recompiled `ext_d` from the L012 source with ONLY `#define MAXP 640` (`src/ext_d_maxp640.c`, `diff` is the one line); the output is byte-identical to the L012 ext_d on a 3,000-input regression (13,456-input (19,16,8,3) d=3 set: 4,157 hits, `cmp` identical). `bin/` = symlinks to the L012 canon, enum_conn, filt, realize, realize_extra + the recompiled ext_d. Cells computed before the restart used only inputs that did not hit MAXP (they completed with rc 0).
- The heavy cell (25,19,10,3) (2,082,993 ext_d inputs on 24-vertex graphs) was run with `mystream2.py` / `run_one2.py` (chunked variant of mystream.recurse: same branch, decompositions, inputs, ext_d call, filt mode and canon, but inputs are processed in contiguous chunks of 25,000 and each finished chunk persists its canonical keys (`out/chunks/.../cNNNNN.keys.gz`) and counters, so the run is resumable). Validated: (19,16,8,3) with CHUNK=3000 gives the identical 227 classes as the L012 file, and a resumed run (one chunk deleted) too.
- Cost estimate that decided this: `sample_cost.py` (1,500 random inputs of each big decomposition, seed 20261017) predicted about 8 h wall for the branch under the machine load at that time (cap left about 4.3 h).

## Exact commands
`bash run.sh` (arith, plan, run_all.py: bottom-up all cells except the heavy chain); `python3 sample_cost.py 1500`; `bash run_heavy.sh` (heavy chain with the resumable runner; stopped by `timeout` at the cap 2026-10-18 03:48:58 UTC, rc 124). `python3 collect.py`, `python3 chunk_stats.py` for the tables. (The first driver launch used the unpatched `bin`; see Deviation; progress.tsv has a NOTE line.)

## Results
Open n = 27 cells:

| cell | classes | seconds | inputs | bad_tau | status |
|---|---|---|---|---|---|
| (27,13,10,2) | 0 | 1.1 | 1 | 0 | EMPTY |
| (27,18,11,2) | 0 | 0.0 | 0 | 0 | EMPTY (all component cells empty) |
| (27,14,10,3) | 0 | 2.4 | 9 | 0 | EMPTY |
| (27,19,11,3) | 0 | 2.2 | 18 | 0 | EMPTY |
| (27,25,12,3) | - | - | - | - | NOT COMPUTED |

Chain for (27,25,12,3) (its only branch is d=3, tau'=11, remainder (26,22) slack 1: [(26,22,11)], [(12,10,5),(14,12,6)] (both seeded), [(23,21,10),(3,1,1)] (void since cell(23,21,10,3) is empty)):

| cell | classes | seconds (wall, nice 19, shared machine) | inputs | bad_tau | status |
|---|---|---|---|---|---|
| (24,16,9,3) | 39,568 | 5,224.6 | 127,766 | 0 | done (6.10e9 ext_d nodes); `cell_24_16_9_D3.txt.gz` |
| (25,19,10,3) | - | 15,281 s of ext_d chunks | 950,000 of 2,082,993 done | 0 | INTERRUPTED at the cap |
| (26,22,11,3) | - | - | - | - | not started (needs (25,19,10,3)) |
| (27,25,12,3) | - | - | - | - | not started |

(25,19,10,3), branch d=3, tau'=9 (the only branch), `partial_25_19_10.json`: 38 of 84 chunks done (inputs 1 to 950,000; these cover all decompositions up to the first about 618,000 inputs of [(3,1,1),(3,1,1),(18,14,7)]), 6,026,620 hits in C, 1,242,774 connected hits, 35,645 distinct classes so far (partial, NOT the cell), bad_tau 0, 1.4e10 ext_d nodes. Remaining: 1,132,993 inputs (46 chunks, about 370 s each, about 4.7 h at the same share; late chunks yield few connected hits (0 to 5,000 per chunk)). Then (26,22,11,3) (15 decompositions; [(25,19,10)] contributes one input per class of the cell, the others about 193,725 inputs plus the 94,513 + 9,387 + 6 + 29,898 ones of [(3,1,1),(22,18,9)] etc.) and (27,25,12,3) (299 inputs plus the classes of the other two components) would still be needed.
Besides these, 46 new cells were computed in total (all bad_tau = 0 in every ext_d call; non-violator cells are non-empty, e.g. (23,13,8,3) 2,693 classes, (22,12,7,2) 1,238, (24,12,8,2) 14, (24,16,9,3) 39,568); see `cells_table.tsv`.

## Conclusion
**'I11 holds on C for n = 27': NOT DECIDED.** Four of the five open n = 27 cells, (27,13,10,2), (27,18,11,2), (27,14,10,3), (27,19,11,3), are EMPTY (computation, unrefereed). The fifth, (27,25,12,3), depends on cell(26,22,11,3), which depends on cell(25,19,10,3) (45.6% of its inputs processed at the 6 h cap; estimated further about 4.7 h at one niced process, plus (26,22,11,3), whose size is not yet estimated). To resume: untar `chunks_25_19_10_d3_tp9.tar.gz` into `out/` (so that `out/chunks/` exists), gunzip `cell_24_16_9_D3.txt.gz` into `out/cells/`, untar `cells_n27_new.tar.gz` into `out/cells/`, symlink the seed files as in run.sh/`seed_cells.txt`, then `bash run_heavy.sh` (set CAP_EPOCH). A node with more cores could split the remaining chunks (disjoint chunk indices are independent; the chunk code is deterministic).

Files: arith.py, arith_output.txt, plan.py, plan_output.txt, plan.json, run.sh, run_all.py, run_heavy.sh, run_one.py, run_one2.py, mystream.py, mystream2.py, engine.py (+decomp*.py copies), src/ext_d_maxp640.c, sample_cost.py, collect.py, chunk_stats.py, progress.tsv, cells_table.tsv, results.json, partial_25_19_10.json, new_cells.txt, seed_cells.txt, cell_24_16_9_D3.txt.gz, cells_n27_new.tar.gz, chunks_25_19_10_d3_tp9.tar.gz; logs in out/ (git-ignored).


## Resumed 2026-10-20 (16:10-22:10 UTC, 6 h cap, NPROC=1, nice 19, timeout) [verified-here as a computation, unrefereed]
What was done: container restart checked first. All seeded cell files (243 files in out/cells, 0 broken symlinks), out/chunks (38 chunks of cell(25,19,10,3)) and bin/ were intact; bin/ext_d is the MAXP=640 build, md5 8f76c7f8ff13d53c6f7b48dda5a37751 (source src/ext_d_maxp640.c, md5 bb0bb8c8caec067eae2cea83c77eb901); the unfinished 39th chunk was simply rerun.
Resume-logic check at the chunk boundary: chunk 38/84 (c00037) was deleted and recomputed in the resumed run; keys.gz md5 (b85fb8e3...) and hits/connected counts were identical.
Command: `CAP_EPOCH=1792534240 bash run_heavy.sh` (CAP_EPOCH = 2026-10-20 22:10:40 UTC; log out/heavy2.log, chunk table out/chunk_progress.tsv).

Results:
- **cell(25,19,10,3) = 35,645 classes** (branch d=3, tau'=9, the only branch; 48 decompositions, 2,082,993 inputs in 84 chunks, 2.3128e10 ext_d nodes, bad_tau 0, 20,133 s wall in this run including a load from other jobs). Total so far 35,645 = the same count as after 38 chunks (the last 46 chunks found no new classes). File `cell_25_19_10_D3.txt.gz`; row in progress.tsv, results.json, cells_table.tsv.
- **cell(26,22,11,3)**: only branch d=3, tau'=10 (Delta <= 3 is the correct bound for the whole recursion: the violator (27,25,12) has all AP-degrees <= 3, so d ranges over max(1,ceil(3m/n)) .. 3 and ceil(66/26) = 3 leaves d = 3; a d=4 branch does not exist; the tp = 11 branch has S' < 0). 15 decompositions, about 229,369 inputs = 10 chunks of 25,000. Only chunk 1/10 finished before the cap (910 s, 283 hits in C, all connected, bad_tau 0, 1.38e8 nodes). INTERRUPTED at the cap (progress.tsv line), resumable (chunks_26_22_11_d3_tp10.tar.gz; about 9 more chunks at about 900 s each is the estimate, about 2.3 h at this load).
- cell(27,25,12,3): not started (needs cell(26,22,11,3); 299 known inputs plus the classes of the components).

Conclusion: **'I11 holds on C for n = 27': NOT DECIDED.** Four of five open n = 27 cells are empty; (27,25,12,3) remains. Remaining work: about 9 chunks of cell(26,22,11,3), then cell(27,25,12,3).
To resume: untar chunks_25_19_10_d3_tp9.tar.gz and chunks_26_22_11_d3_tp10.tar.gz into out/ (gives out/chunks/), gunzip cell_24_16_9_D3.txt.gz and cell_25_19_10_D3.txt.gz and untar cells_n27_new.tar.gz into out/cells/, symlink the seeds as in run.sh, then `CAP_EPOCH=<epoch> bash run_heavy.sh`.


## Finished 2026-10-20 (22:12-23:35 UTC, NPROC=2, nice -n 5, timeout) [verified-here as a computation, unrefereed]
Binary: bin/ext_d is still the MAXP=640 build, md5 8f76c7f8ff13d53c6f7b48dda5a37751 (unchanged; other bin/ md5 as in out/ext_d_md5.txt). Disk free stayed at 18 GB.
Parallelism: `mystream2.py` got a `WORKER` mode (env `WORKER=1`): a worker claims a chunk with an O_EXCL `cNNNNN.claim` file, skips chunks claimed or done, and at the end raises WORKER_DONE_SKIPPED_CHUNKS (expected). Chunk contents are unchanged (same code path per chunk). Two workers were started with
`CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine_w.log NPROC=1 MD=10 CHUNK=25000 WORKER=1 nice -n 5 timeout 13000 python3 run_one2.py 26 22 11 3` (x2; chunk 1/10 existed from the earlier run, which was loaded as is; the resume of the chunk boundary was checked by the previous worker, see above). Then the assembling run without WORKER: `... python3 run_one2.py 26 22 11 3` (7 s), and `... timeout 3000 nice -n 5 python3 run_one2.py 27 25 12 3` (31 s). Logs out/worker26_{1,2}.log, out/chunk_progress.tsv (copy chunk_progress.tsv).

Results:
- **cell(26,22,11,3) = 36 classes** (d=3, tp=10 only; 15 decompositions, 229,369 inputs, 10 chunks, 9.415e8 ext_d nodes, bad_tau 0, hits in C 7,181, connected hits 1,080; sum of chunk times 8,906 s). Chunks 5 to 10 gave no hits. File cell_26_22_11_D3.txt.gz.
- **cell(27,25,12,3) = 0 classes (EMPTY)** (d=3, tp=11, S'=1; 3 decompositions: [(26,22,11)] 36 inputs, [(12,10,5),(14,12,6)] 298 inputs (149 x 2 products), [(3,1,1),(23,21,10)] 0 (cell(23,21,10,3) empty); 334 inputs, 53,959 ext_d nodes, bad_tau 0, 36 ext_d hits F7-free but 0 survive the filter (linear, F7-free, P3, connected on 27 vertices, tau == 12); 31.4 s). File cell_27_25_12_D3.txt.gz.

Conclusion: **'I11 holds on C for n = 27: YES (computation, unrefereed)'**: the five open n = 27 cells (27,13,10,2), (27,18,11,2), (27,14,10,3), (27,19,11,3), (27,25,12,3) are all EMPTY. Caveats: same unrefereed status and engine as L013 (unchanged L012 engine; ext_d with MAXP 640; chunked/streamed driver); no certificate document (L015-type) written; no referee run.
Files added: cell_26_22_11_D3.txt.gz, cell_27_25_12_D3.txt.gz, chunks_26_22_11_d3_tp10.tar.gz, chunks_27_25_12_d3_tp11.tar.gz, chunk_progress.tsv, start_epoch_20261020.txt; results.json (key resume_2026-10-20_second_run), progress.tsv, cells_table.tsv updated.
