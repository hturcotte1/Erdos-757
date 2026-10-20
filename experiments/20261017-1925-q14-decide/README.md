# Q14 decision: the degree-3 case of the record cell (23,21,10)

Date 2026-10-17 (20:17 to 21:45 UTC). Computation only, NOT refereed. All numbers below are [verified-here] as computations (exact integer enumeration, nauty canonical forms), tag: unrefereed.

## Question
Is cell(23,21,10,3) empty? That cell is the set of isomorphism classes of CONNECTED members of the class C (linear, F7-free, (P3) e(S)<=|S|-2) with 23 vertices, 21 edges, tau = 10 exactly and maximum degree <= 3 (a 23-point (4,5)-set with h = 13 would have such a hypergraph; L012 gives degree <= 3, Q14).

## Method
- Engine: `engine.py` = byte-identical copy of `experiments/prover/L012/engine.py` (md5 a1924839...; `decomp22.py`, `decomps.py` copied from `../20261017-1735-q14-cell-sizes`). Binaries `bin -> ../prover/L012/bin` (enum_conn, ext_d, filt, canon, realize, realize_extra). Seeded cell files: the 183 cell files computed by the earlier probe, symlinked (not recomputed) from `../20261017-1735-q14-cell-sizes/out/cells` (themselves seeded from the 1720 run).
- The plain engine runs out of memory on the big cells (probe finding), so `mystream.py` (derived from the probe's `streamdirect.py`) replaces `engine.recurse` (n >= 17) and `engine.direct` (n >= 13) by shell pipelines ext_d | grep HIT | filt | canon | sort -u, same programs, same decompositions, same inputs, same ext_d call (`ext_d n-1 tp t d d-1`) and filt modes; differences from the probe's code: inputs are split into NPROC=2 interleaved chunks run as two parallel pipelines (counters summed), and `grep` is wrapped in `(grep ... || true)` (see below). `run_one.py` = probe's, plus a PROGRESS env var.
- Step 1: `ext_d 21 8 9 3 2` (branch d=3, tau'=8, S'=5) on the 2,014,413 inputs from the 20 decompositions of (21,15), then filt (linear, F7-free, (P3), connected on 22 vertices, tau 'notau' since tau' = t-1 gives tau = t) and canon.
- Step 2: `ext_d 22 9 10 3 2` on the 133,804 inputs from the five decompositions of (22,18) with slack 3 (94,513 + 0 + 9,387 + 6 + 29,898), filt, canon.
- Commands (`run.sh`, from this folder; nice -n 5, NPROC=2, MD=10): `python3 run_one.py 22 18 9 3`, `python3 run_one.py 23 21 10 3`; sanity: `sanity_all.sh` / `sanity.sh`.
- Process note: the first attempt of step 2 ran all 133,804 inputs (0 HIT lines) but my streamed pipeline then aborted because `grep` exits with rc 1 on empty input under `set -o pipefail` (log kept: `out/run_23_21_10_firstattempt_grep_rc1.log`; progress.tsv line marked FIRST_ATTEMPT). I wrapped the greps in `(grep ... || true)` in `mystream.py` and reran step 2 with the identical command; all numbers below are from the rerun (same ext counters: 48,029,683 nodes). The step 1 run was done before the patch (its greps matched, so the patch cannot affect it); the patched `mystream.py` was used for all sanity runs after the patch (10,8,4 / 19,16,8 / 17,11,6 stream).

## Results
| cell | classes | seconds (wall, 2 procs) | inputs | ext_d nodes | raw HIT lines (in C) | F7-free hits | connected hits | bad_tau |
|---|---|---|---|---|---|---|---|---|
| (22,18,9,3) | **94,513** | 2,762.8 | 2,014,413 | 5,238,536,047 | 3,042,157 | 3,470,939 | 2,239,624 (filt, before canonical dedup) | 0 |
| (23,21,10,3) | **0** | 481.2 | 133,804 | 48,029,683 | **0** | 4,249 (all fail (P3)) | 0 | 0 |
- (22,18,9,3) matches the probe's estimates (5.2e9 nodes, 3.1e6 hits in C). Class file: `out/cell_22_18_9_D3.txt` (17.5 MB, git-ignored), tracked gzip `cell_22_18_9_D3.txt.gz` (sha256 prefix of the uncompressed file 9a6e1794e8b55fd4). `out/cell_23_21_10_D3.txt` is empty (so no gzip).
- (23,21,10,3): inputs by decomposition: [(22,18,9)] 94,513; [(21,18,9),iso] 0 (cell(21,18,9,3) is empty); [(10,8,4),(12,10,5)] 9,387; [(8,6,3),(14,12,6)] 6; [(3,1,1),(19,17,8)] 29,898. Every input was searched; no HIT passes ext_d's internal tests, i.e. no re-insertion of a degree-3 vertex yields a member of C with tau = 10.
- Step 3 (realization): not needed, the class list is empty (`./bin/realize 23 < out/cell_23_21_10_D3.txt` gives graphs=0). Positive control, run anyway: `abase_control_output.txt`, A_base pattern with bin/realize 14: assignments=1596, distinct=1413, realizations=948 (as in L012 C5), A_base itself among them.

## Sanity (step 4): which program produced which number
| cell | reference | recomputed here | by |
|---|---|---|---|
| (10,8,4,3) | 63 (probe/L012 file) | 63, identical sets | plain unmodified L012 `engine.py` (direct) and `mystream`/run_one |
| (19,16,8,3) | 227 (L012 file) | 227, identical sets (both) | plain unmodified L012 `engine.py` (8 s) and the streamed pipeline (8.4 s) |
| (17,11,6,3) | 45,669 (probe) | 45,669, identical sets | streamed pipeline (39 s) |
| (23,21,10,3) | - | 0 classes | additionally the plain unmodified L012 `engine.py 23 21 10 3` (NPROC=2, 1,047 s, own Python filtering): RESULT 0 |
Cells loaded from the probe/L012 cell files (not recomputed here): all cells other than (22,18,9,3) and (23,21,10,3). Programs: L012 binaries (ext_d, filt, canon, enum_conn, realize) for everything; engine.py (L012) as the driver; probe scripts / mystream.py only for the streamed route (22,18,9,3), (23,21,10,3), and the streamed sanity runs. Sanity logs: `out/sanity_*.log` (git-ignored), first sanity run had a harness bug (missing /usr/bin/time, D2 cells not linked) and was rerun; only the reruns are reported.

## Conclusion
**cell(23,21,10,3) is EMPTY** (computation, [verified-here], not refereed; it depends on the L012 engine reduction and on the correctness of all seeded cell files and of ext_d/filt/canon, which are L012-certified; the new cell (22,18,9,3) has 94,513 classes and no independent recomputation beyond the node/hit agreement with the probe's sampled estimate). Together with L012 (Theorem 2 reduces a 23-point record to m = 21, Theorem 3 excludes a degree-4 vertex) this would show that no 23-point (4,5)-set has h = 13; that deduction and the computation above need a referee before any such claim is made.
