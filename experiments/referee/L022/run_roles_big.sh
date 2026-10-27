#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L022
until grep -q "T2 DONE" out/run_all.log; do sleep 10; done
echo "ROLES_BIG START $(date -u +%T)" >> out/run_all.log
nice -n 10 timeout 1200 python3 -u -I roles.py 22_17_9 26_22_11 > out/roles_big.txt 2>&1; echo "roles_big exit $? $(date -u +%T)" >> out/run_all.log
echo "ALL DONE $(date -u +%T)" >> out/run_all.log
