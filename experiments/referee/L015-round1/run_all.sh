#!/bin/bash
# Referee L015 round 1: reruns every referee computation (own code, imports nothing from the repository).
# Total about 2 CPU-minutes. Outputs: r*.log in this folder. prover_rerun/ holds COPIES of the prover's
# v1..v7 scripts (v7's sys.path line pointed at the copy), rerun here so that experiments/prover/L015 is untouched.
set -euo pipefail
cd /home/user/Erdos-757/experiments/referee/L015-round1
nice -n 10 timeout 300  python3 -I r1_facts_O.py      > r1_facts_O.log      # F0-F6, table, 5.6 hitting sets, U*
nice -n 10 timeout 1500 python3 -I r2_family.py       > r2_family.log       # points, integer form, census K<=20, T_K K<=30, (4,5) K<=8, C003
nice -n 10 timeout 2400 python3 -I r3_h.py 20 3       > r3_h.log            # h: frontier DP K<=20, literal K<=1, CP-SAT K<=3, controls
nice -n 10 timeout 1200 python3 -I r4_sat.py $(seq 0 20) > r4_sat.log       # h: SAT (CaDiCaL), >=7+5K SAT, >=8+5K UNSAT, K<=20
nice -n 10 timeout 1200 python3 -I r6_lemma_tests.py  > r6_lemma_tests.log  # general lemmas (Step 4, 5.1) on data, random sets, gluings; Step 7 ratios
grep -h -E "SUMMARY" r*.log
