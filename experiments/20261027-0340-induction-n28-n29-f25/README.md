# Exact induction I11 at n = 28, 29 and the record cell (25,23,11) with Delta <= 4 (IN PROGRESS)

Started 2026-10-27 ~03:10 UTC. Unrefereed computation; tags [verified-here] as an unrefereed computation. Plan: ../20261027-0235-cost-n28-n29/README.md.
Milestone 1 (n = 28): see "n = 28" below. The rest is filled in at the end of the run.

Method: L012 engine (src/engine.py, decomp22.py: byte-identical to experiments/prover/L012), L014/L016 streamed driver (src/stream.py), ext_d = ext_d_fast (L016, Lemma B), canon/filt/enum_conn = L012 binaries (checksums_code.txt),
`src/run1.py` = one cell per process (refuses to run with missing component cells; appends to progress.tsv right after saving), `run_list.sh` (nice -n 5, timeout 3 h per cell, NPROC as set), `seed.py` (seeds out/cells with every existing cell file, checks overlaps, writes provenance.tsv/json).
