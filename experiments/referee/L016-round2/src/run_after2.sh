#!/bin/bash
R=/home/user/Erdos-757/experiments/referee/L016-round2; CF=/home/user/Erdos-757/experiments/prover/L016/out/cellsF
cd $R
until grep -q "all done" out/after_status.txt 2>/dev/null; do sleep 5; done
nice -n 10 timeout 600 python3 src/closure.py $CF 24 16 9 > out/closure_24_16_9_3.txt 2>&1
echo "closure24 done $(date -u)" >> out/after_status.txt
