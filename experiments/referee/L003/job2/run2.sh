#!/bin/bash
# Referee L003 follow-up job: strictly sequential, one niced process at a time.
D=/home/user/Erdos-757/experiments/referee/L003
cd $D
while [ -e /proc/23319 ]; do sleep 20; done; sleep 5
echo "== start $(date -u)"
# 1. n=11, K30+linearity, pure exact path (no float prefilter at all)
( time nice -n 10 ./satenum 11 7 1 0 0 | gzip > job2/sat_n11_k30lin_exact.txt.gz ) 2>&1 | grep real
zcat job2/sat_n11_k30lin_exact.txt.gz | tail -1
# 2. n=11 pattern counts (K30+lin search, exact alpha, own F7 test)
for m in 9 5 6 7 8; do ( time nice -n 10 ./patcount 11 7 $m ) 2>&1 | grep -E "PATCOUNT|real"; done
# 3. non-saturated realizability decisions, n=9 m=5,6 and n=10 m=7 (and n=10 m=8 saturated as a cross-check of the decider)
for nm in "9 6 5" "9 6 6" "10 6 7"; do set -- $nm; nice -n 10 ./patenum $nm | nice -n 10 python3 realdec.py $1 $2 h; done
echo "== end $(date -u)"
echo FINISHED
