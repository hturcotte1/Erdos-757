#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L022
echo "START $(date -u +%FT%TZ)" > out/run_all.log
nice -n 10 timeout 1500 python3 -I rz.py > out/rz.txt 2>&1; echo "rz exit $? $(date -u +%T)" >> out/run_all.log
nice -n 10 timeout 900 python3 -I t2.py 11 30000 30000 > out/t2_seed11.txt 2>&1; echo "t2 exit $? $(date -u +%T)" >> out/run_all.log
nice -n 10 timeout 900 python3 -I t1t4.py > out/t1t4.txt 2>&1; echo "t1t4 exit $? $(date -u +%T)" >> out/run_all.log
nice -n 10 timeout 1200 python3 -I roles.py 3_1_1 8_5_3 10_7_4 12_10_5 14_12_6 15_11_6 17_13_7 > out/roles_small.txt 2>&1; echo "roles_small exit $? $(date -u +%T)" >> out/run_all.log
nice -n 10 timeout 1500 python3 -I roles.py 22_17_9 26_22_11 > out/roles_big.txt 2>&1; echo "roles_big exit $? $(date -u +%T)" >> out/run_all.log
echo "DONE $(date -u +%FT%TZ)" >> out/run_all.log
