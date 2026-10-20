#!/bin/bash
# Reproduces every computation cited in results/proofs/L015-reader-family-c-le-5-9.md (C1-C7).
# Pure Python 3 (standard library only), exact integers and Fractions; about 4 CPU-minutes in total on one core.
# Run from anywhere:  bash /home/user/Erdos-757/experiments/prover/L015/reproduce.sh
# Read-only inputs: data/reader_5_9_family.json and results/claims/C003-reader-5-9-K6.json (C3 compares with them),
# experiments/20261020-1730-reader-5-9/check_results.json and census_deep_results.json (C6 compares with them).
# No code of experiments/20261020-1730-reader-5-9/, e757/ or judge/ is imported.
set -euo pipefail
cd /home/user/Erdos-757/experiments/referee/L015-round3/prover_rerun
nice -n 10 timeout 120  python3 -I v1_facts_O.py  > v1_facts_O_output.txt             # C1: facts F0-F6 about O, phi, y, residues mod 269
nice -n 10 timeout 120  python3 -I v2_transfer.py > v2_transfer_output.txt            # C2: best table, M, R0, R0 (x) M = R0 + 5 (two methods)
nice -n 10 timeout 1500 python3 -I v3_family.py 8 0 1 2 3 4 5 6 7 8 9 10 11 12 15 20 30 40 60 > v3_family_output.txt   # C3 (writes v3_family_results.json)
nice -n 10 timeout 1200 python3 -I v4_h.py 20     > v4_h_output.txt                   # C4: h by literal brute force (K<=1) and generic exact solver (K<=20)
nice -n 10 timeout 600  python3 -I v5_witness.py 0 1 2 3 4 5 6 7 8 9 10 12 15 20 30 50 > v5_witness_output.txt   # C5: explicit Sidon subsets T_K
nice -n 10 timeout 120  python3 -I v6_compare.py  > v6_compare_output.txt             # C6: comparison with the agent's numbers (needs C3, C4 outputs)
nice -n 10 timeout 120  python3 -I v7_controls.py > v7_controls_output.txt            # C7: non-vacuity controls
rm -rf __pycache__
grep -h -E "ALL (FACTS|TRANSFER CHECKS|FAMILY CHECKS|h CHECKS|WITNESS CHECKS|COMPARISONS AGREE|CONTROLS)" v*_output.txt
