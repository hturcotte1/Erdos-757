# Exact induction I11 at n = 28, 29 and the record cell (25,23,11) with Delta <= 4 (IN PROGRESS)

Started 2026-10-27 ~03:10 UTC. Unrefereed computation; tags [verified-here] as an unrefereed computation. Plan: ../20261027-0235-cost-n28-n29/README.md.
Milestone 1 (n = 28): see "n = 28" below. The rest is filled in at the end of the run.

Method: L012 engine (src/engine.py, decomp22.py: byte-identical to experiments/prover/L012), L014/L016 streamed driver (src/stream.py), ext_d = ext_d_fast (L016, Lemma B), canon/filt/enum_conn = L012 binaries (checksums_code.txt),
`src/run1.py` = one cell per process (refuses to run with missing component cells; appends to progress.tsv right after saving), `run_list.sh` (nice -n 5, timeout 3 h per cell, NPROC as set), `seed.py` (seeds out/cells with every existing cell file, checks overlaps, writes provenance.tsv/json).

## Progress note (07:40 UTC, 4.5 h into the run)
Done: n = 28 (all three violator cells (28,17,11,2), (28,18,11,3), (28,23,12,3) = 0; also (28,14,10,2) = 0, (28,19,11,3) = 0), n = 29 cells (29,15,11,2) = (29,16,11,3) = (29,22,12,3) = 0, record cell (25,23,11,4) = 6 classes (none realizable) and (25,23,11,3) = 0, cell(21,19,9,4) = 31,268 (exported), f(19) side cells (18,12,7,5) = 0 etc.
Remaining n = 29: (26,18,10,3) [running; ext_d at ~46% of its input after 1 h 45 min, so ~2 h more at the current load 13 on 4 cores, estimate done ~09:45 UTC] -> (27,21,11,3) [~521k inputs by the cost estimate, 2-3 h, so ~12:00 UTC] -> (28,24,12,3) -> (29,27,13,3) (both small once (27,21,11,3) exists). If the load stays, (27,21,11,3) may not finish inside the 9 h budget (ends ~12:10 UTC); the partial state is resumable (the engine reloads finished cells).
Remaining f(19): cell(19,17,8,5) (running at nice 15 so as not to slow the n = 29 chain; d = 4 branch ext_d 18 7 8 4 3 at 45 min CPU); cell(19,16,8,4) = 956 classes already exists (refereed L012).
Disk: only 3.6 GB free at 07:38 (other agents: /tmp/pytest-of-root 4.4 GB etc.); this folder uses ~0.7 GB.
