#!/bin/bash
# Final data checks of L022, run sequentially (one process at a time), low priority.
cd /home/user/Erdos-757/experiments/prover/L022
timeout 1500 nice -n 10 python3 order_checks.py > out/order_checks.txt 2>&1
timeout 1500 nice -n 10 python3 edge_delete_check.py 1 10 > out/edge_delete_check.txt 2>&1
timeout 1500 nice -n 10 python3 local_configs.py > out/local_configs.txt 2>&1
timeout 1800 nice -n 10 python3 test_subext.py 1 40000 7 12 > out/test_subext_1.txt 2>&1
timeout 1800 nice -n 10 python3 test_subext.py 3 20000 7 11 > out/test_subext_3.txt 2>&1
timeout 2400 nice -n 10 python3 test_subext.py 2 60000 9 13 > out/test_subext_2.txt 2>&1
echo done > out/final_checks.done
