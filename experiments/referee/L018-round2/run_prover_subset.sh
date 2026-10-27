#!/bin/bash
# Referee re-run of the prover's own scripts (C1, C8, C9, C3, C4, C6) in a scratch copy; outputs prefixed my_
cd /home/user/Erdos-757/experiments/referee/L018-round2/prover_copy
N="nice -n 10 timeout 2400"
date -u; echo "== C1 R=1"; $N python3 localconf.py 1 1 > my_out_root1_R1.txt; echo rc=$?
date -u; echo "== C1 R=2"; $N python3 localconf.py 1 2 > my_out_root1_R2.txt; echo rc=$?
date -u; echo "== C1 R=3"; $N python3 localconf.py 1 3 > my_out_root1_R3.txt; echo rc=$?
date -u; echo "== show R=2"; $N python3 show.py 1 2 > my_out_root1_R2_leaves.txt; echo rc=$?
date -u; echo "== show R=3"; $N python3 show.py 1 3 > my_out_root1_R3_leaves.txt; echo rc=$?
date -u; echo "== C8"; $N python3 tight_glue.py > my_tight_glue_output.txt; echo rc=$?
date -u; echo "== C9"; $N python3 prune28.py 28 29 > my_prune28_output.txt; echo rc=$?
date -u; echo "== C6"; $N python3 tightdeg.py > my_tightdeg_output.txt; echo rc=$?
date -u; echo "== C3"; $N python3 lemma_m_check.py > my_lemma_m_check_output.txt; echo rc=$?
date -u; echo "== C4"; $N python3 lemma_tests.py 11 > my_lemma_tests_output.txt; echo rc=$?
date -u; echo ALLDONE
