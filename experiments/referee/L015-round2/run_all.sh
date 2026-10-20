#!/bin/bash
# L015 referee round 2: reruns every own check (exact ints/Fractions; pysat for SAT). About 30 s wall in total.
# Run:  bash /home/user/Erdos-757/experiments/referee/L015-round2/run_all.sh
set -euo pipefail
cd /home/user/Erdos-757/experiments/referee/L015-round2
nice -n 10 timeout 300  python3 -I -B r1_facts.py > r1_facts_output.txt                                  # F0-F6, table, 5.6 bounds
nice -n 10 timeout 900  python3 -I -B r2_family.py 0 1 2 3 4 5 6 7 8 9 10 > r2_family_output_a.txt       # census K<=10
cp r2_family_results.json r2_family_results_a.json
nice -n 10 timeout 1800 python3 -I -B r2_family.py 11 12 13 14 15 16 17 18 19 20 25 30 40 > r2_family_output_b.txt   # census K<=20, 25, 30, 40
mv r2_family_results.json r2_family_results_b.json
nice -n 10 timeout 600  python3 -I -B r2_controls.py > r2_controls_output.txt                            # non-vacuity controls
nice -n 10 timeout 1800 python3 -I -B r3_45.py 0 1 2 3 4 5 6 7 8 > r3_45_output.txt                      # literal |B-B| K<=8
nice -n 10 timeout 3000 python3 -I -B r4_h.py 8 20 > r4_h_output.txt                                     # h: SAT K<=8, DP K<=20
nice -n 10 timeout 1500 python3 -I -B r5_witness_c003.py > r5_witness_c003_output.txt                    # T_K K<=30, C003
nice -n 10 timeout 900  python3 -I -B r6_selftest.py > r6_selftest_output.txt                            # DP/SAT vs brute force
grep -h -E "^ALL|CONTROLS OK" r1_facts_output.txt r2_family_output_a.txt r2_family_output_b.txt r2_controls_output.txt r3_45_output.txt r4_h_output.txt r5_witness_c003_output.txt r6_selftest_output.txt
