# Q14 probe: sizes of the cells needed by the degree-3 case of the record cell (23,21,10)

Date 2026-10-17 (17:32 to 20:20 UTC). Measurement probe, NOT a decision about Q14. All counts below were computed here with the L012 engine logic
(exact integers, nauty canonical forms), tag [verified-here] as computations, unrefereed. Cost extrapolations are [heuristic].

## Question
Which connected class-C cells (Delta <= 3) does cell(23,21,10,3) need, how big are they, how long do they take, and what would the rest cost?

## Method
- Engine: `engine.py`, `decomp22.py` byte-identical to the 1720 folder (`run.sh` copies them). Seeded with the 167 cell files of `../20261017-1720-i11-n26/out/cells`. MD = 10.
- Harness deviations (engine logic unchanged, same binaries enum_conn/ext_d/filt/canon, same decompositions and inputs):
  1. The unchanged engine could not run: `engine.direct` for the sub-cell (14,10,5,3) (57.9M labelled graphs) held all lines in Python and was
     OOM-killed at 13.8 GB (first attempt of cell (15,13,6,3), progress.tsv line 1); `engine.recurse` for (18,14,7,3) writes ~23M HIT lines (a 1.3 GB .out
     file after 4 min, disk had 1.3 GB free) and then keeps them all in Python lists. Hence `streamdirect.py`: `direct` and `recurse` re-implemented as shell pipelines
     (ext_d | grep HIT | filt | canon | sort -u), used for direct n >= 13 and recurse n >= 17 (`run_one.py`). `direct_stream.py` is the same for (14,10,5,3) (run by hand first).
  2. Validation of the streamed code: (10,8,4,3) direct = engine file (63 classes, identical sets); (17,11,6,3) recomputed by the streamed recurse = the engine's own
     file from the interrupted first run (45,669 classes, identical sets).
  3. Several cells were run concurrently by hand (each with NPROC=1, nice 19, one ext_d process): (18,14,7) with (20,12,7) and (21,15,8); (19,17,8) with (21,15,8); (22,18,9) alone.
     So seconds are wall time under load 3-8 on 4 shared cores. A `watchdog.sh` (kills the jobs if free disk < 700 MB; never fired) protected the shared disk.
- `sample_branch.py` (measurement only): builds the exact ext_d input list of every branch from the existing cell files, runs ext_d on an evenly spaced sample
  (>= 30 inputs per decomposition, about 1-2 %), discards HIT lines and extrapolates nodes / hits / CPU per decomposition. Calibration against full runs:
  (15,13,6) top branch estimated 2.81e7 nodes / 1.04e7 hits vs actual 2.798e7 / 1.037e7; (18,14,7) 4.27e8 / 2.35e7 vs actual 4.235e8 / 2.330e7.
- Commands: `run.sh` (decomps.py, then cells in order), by-hand launches: `python3 direct_stream.py 14 10 5 3`; `python3 run_one.py 20 12 7 3`; `python3 run_one.py 21 15 8 3`;
  `python3 run_one.py 19 17 8 3`; `python3 run_one.py 22 18 9 3` (all with `CELLDIR=$PWD/out/cells NPROC=1 MD=10`, `nice -n 19 timeout ...`); `python3 sample_branch.py n m t 3 30 50`.

## Decompositions (decompositions.txt = state at the start; decompositions_final.txt = state at the end)
All five cells and the target have exactly one branch (d = 3, tau' = t-1):
- (23,21,10): remainder (22,18) slack 3, 5 decompositions: [(22,18,9)]; [iso,(21,18,9)] (void, cell = 0); [(10,8,4),(12,10,5)] (63*149 = 9,387 inputs); [(8,6,3),(14,12,6)] (3*2 = 6); [(3,1,1),(19,17,8)] (29,898).
- (22,18,9): remainder (21,15) slack 5, 20 decompositions, 2,014,413 inputs (largest: [(3,1,1),(18,14,7)] 799,342; [2x(3,1,1),(15,13,6)] 949,522; [(21,15,8)] 232,759).
- (19,17,8): remainder (18,14) slack 5, 6 decompositions, 1,750,910 inputs. (21,15,8): remainder (20,12) slack 7, 44 decompositions. (18,14,7): (17,11) slack 7, 19 decompositions. (15,13,6): (14,10) slack 7, 6 decompositions.
- Not yet computed at the start: (22,18,9), (19,17,8), (21,15,8), (18,14,7), (15,13,6), and their sub-cells (14,10,5), (11,9,4), (17,11,6), (20,12,7). At the end only (22,18,9) and (23,21,10) are not computed.

## Finished cells (Delta <= 3; seconds = wall, nested sub-cells already computed excluded unless stated; progress.tsv, results.json)
| cell | classes | seconds | route | inputs | ext_d nodes |
|---|---|---|---|---|---|
| (14,10,5,3) | 45,229 | 2,116 | direct (streamed), 57,909,266 labelled, 57,037,881 in C | - | enum calls 1.08e9 |
| (11,9,4,3) | 1,216 | 19 | direct | - | - |
| (15,13,6,3) | 949,522 | 725 | recurse | 53,280 | 2.80e7 |
| (17,11,6,3) | 45,669 | 80 | recurse | 795 | 6.6e6 |
| (20,12,7,3) | 15,465 | 180 | recurse | 1,164 | 2.4e7 |
| (18,14,7,3) | 799,342 | 1,240 | recurse (streamed) | 102,916 | 4.23e8 |
| (21,15,8,3) | 232,759 | 1,902 | recurse (streamed) | 121,532 | 1.97e9 |
| (19,17,8,3) | 29,898 | 877 | recurse (streamed) | 1,750,910 | 6.15e8 |
| (22,18,9,3) | NOT FINISHED | killed at 2,400 s | recurse (streamed) | 2,014,413 | est. 5.2e9 |
| (23,21,10,3) | not started | - | - | 39,291 + (#(22,18,9) classes) | - |
bad_tau = 0 in every ext_d call. The (22,18,9,3) run: ext_d had read 34.5 % of the input bytes (2,118 s CPU, inside the decomposition [(3,1,1),(18,14,7)]; ext22_progress.log);
no hit count or class count is available for it (the pipeline only reports at the end). Cells the task listed as known and reused: (21,18,9)=0, (14,12,6)=2, (8,6,3)=3, (10,8,4)=63, (12,10,5)=149, (15,12,6)=10,617, (13,10,5)=6,683, (17,14,7)=1,708, (20,15,8)=953.
The cell files (281 MB in out/, git-ignored) are too large to tar under 20 MB; their sha256 prefixes and sizes are in results.json.

## Cost estimate for the rest [heuristic, extrapolated from `samples.jsonl` and the full runs above]
- (22,18,9,3): sample over all 20,405 sampled of 2,014,413 inputs: 5.2e9 ext_d nodes, 3.1e6 hits in C. Observed ext_d speed 1.25e6 nodes/s (2,118 s CPU for about 2.6e9 nodes by the sampled node
  shares) so about 4,200 s = 70 min CPU on one core for ext_d plus a few minutes of filt/canon (3e6 hits). That is about 1.2 CPU-hours; it was started 19:30 and would have ended near 20:40.
  Memory/disk under the streamed code are fine (inputs file 248 MB; peak Python a few GB for the seeded classes).
- Expected size of cell(22,18,9,3) [very rough]: classes / hits_in_C was 0.092, 0.034, 0.0069, 0.058 for (15,13,6), (18,14,7), (21,15,8), (19,17,8); with 3.1e6 hits that gives 2e4 to 3e5 classes.
- (23,21,10,3) after that: the three non-(22,18,9) decompositions are 39,291 inputs, sample (792 inputs) gives 5.7e6 nodes and 0 hits in C (sample only, 2 %). The (22,18,9)-class inputs
  cost 75 to 2,600 nodes per input (the per-input costs seen in (19,17,8) and (22,18,9)), i.e. 1e6 to 8e8 nodes for 2e4-3e5 inputs: at most about 10 minutes.
  Hence the unfinished steps are about 1.3 to 1.5 CPU-hours at the observed rates, dominated by (22,18,9,3). Measured: everything in the table above and the node counts of the first 34.5 % of (22,18,9); extrapolated: the rest.

## Conclusion
Degree-3 case of (23,21,10): the cells (15,13,6), (18,14,7), (21,15,8), (19,17,8) and their sub-cells are now computed (counts above, sizes 3e4 to 9.5e5 classes), so three of the four non-void
decompositions of cell(23,21,10,3) have all their inputs available (sizes 9,387, 6 and 29,898). What remains unknown is cell(22,18,9,3) (the decomposition [(22,18,9)]) and then cell(23,21,10,3);
the probe measured but did not finish the former (about 1.2 CPU-hours more by extrapolation, one more run with NPROC=1 and a 90 min cap, no further engineering). No statement about Q14 follows from this run.
