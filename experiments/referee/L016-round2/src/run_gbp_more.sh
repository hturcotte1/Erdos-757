#!/bin/bash
R=/home/user/Erdos-757/experiments/referee/L016-round2; cd $R
for k in "27 18 11 2 540" "27 19 11 3 900"; do set -- $k; s=$(date +%s); RPRUNE_T=$3 nice -n 10 timeout $5 ./bin/genbg30_prune -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) > out/gbp_raw_$1_$2_$3_$4.g6; rc=$?; e=$(date +%s); ./bin/rext gb $1 $2 $3 $4 < out/gbp_raw_$1_$2_$3_$4.g6 2> out/gbp_filt_$1_$2_$3_$4.log | out/nauty/nauty2_8_8/labelg -q 2>/dev/null | sort -u > out/gbp_$1_$2_$3_$4.g6; echo "PRUNED-GENBG ($1,$2,$3,$4) genbg_rc=$rc secs=$((e-s)) raw=$(wc -l < out/gbp_raw_$1_$2_$3_$4.g6) $(cat out/gbp_filt_$1_$2_$3_$4.log) classes=$(wc -l < out/gbp_$1_$2_$3_$4.g6)" >> out/gbp_more_status.txt; done
echo "gbp more done $(date -u)" >> out/gbp_more_status.txt
