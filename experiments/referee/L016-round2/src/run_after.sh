#!/bin/bash
# runs after the chunk job: (26,22,11,3) recomputation, closure on (25,19,10,3), pruned genbg attempts (time-boxed)
R=/home/user/Erdos-757/experiments/referee/L016-round2; CF=/home/user/Erdos-757/experiments/prover/L016/out/cellsF
cd $R
while pgrep -f "src/chunks25.py" > /dev/null; do sleep 5; done
echo "start after-chain $(date -u)" > out/after_status.txt
nice -n 10 timeout 1500 python3 src/recompute.py 26 22 11 3 $CF --save out/mine_26_22_11_3.g6 > out/recompute_26_22_11_3.txt 2>&1
echo "recompute26 done $(date -u)" >> out/after_status.txt
nice -n 10 timeout 900 python3 src/closure.py $CF 25 19 10 > out/closure_25_19_10_3.txt 2>&1
echo "closure25 done $(date -u)" >> out/after_status.txt
for k in "27 14 10 3"; do set -- $k; s=$(date +%s); RPRUNE_T=$3 nice -n 10 timeout 600 ./bin/genbg30_prune -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) > out/gbp_raw_$1_$2_$3_$4.g6 2> out/gbp_raw_$1_$2_$3_$4.err; rc=$?; e=$(date +%s); ./bin/rext gb $1 $2 $3 $4 < out/gbp_raw_$1_$2_$3_$4.g6 2> out/gbp_filt_$1_$2_$3_$4.log | out/nauty/nauty2_8_8/labelg -q 2>/dev/null | sort -u > out/gbp_$1_$2_$3_$4.g6; echo "PRUNED-GENBG ($k) genbg_rc=$rc secs=$((e-s)) raw=$(wc -l < out/gbp_raw_$1_$2_$3_$4.g6) $(cat out/gbp_filt_$1_$2_$3_$4.log) classes=$(wc -l < out/gbp_$1_$2_$3_$4.g6) | $(tail -2 out/gbp_raw_$1_$2_$3_$4.err | tr '\n' ' ')" >> out/after_status.txt; done
echo "all done $(date -u)" >> out/after_status.txt
