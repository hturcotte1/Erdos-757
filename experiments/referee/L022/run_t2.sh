#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L022
until grep -q "DONE" out/run_all.log; do sleep 10; done
echo "T2 START $(date -u +%T)" >> out/run_all.log
nice -n 10 timeout 1200 python3 -u -I t2.py 11 12000 12000 > out/t2_seed11.txt 2>&1; echo "t2 exit $? $(date -u +%T)" >> out/run_all.log
nice -n 10 timeout 600 python3 -u -I t2.py 23 6000 6000 > out/t2_seed23.txt 2>&1; echo "t2b exit $? $(date -u +%T)" >> out/run_all.log
echo "T2 DONE $(date -u +%T)" >> out/run_all.log
