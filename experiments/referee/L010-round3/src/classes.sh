#!/bin/bash
# canonical class sets: prover's labelled lists vs my genbg lists, then the direct (18,12,>=7) Delta<=3 enumeration
cd /home/user/Erdos-757/experiments/referee/L010-round3
P10=/home/user/Erdos-757/experiments/prover/L010/out; P9=/home/user/Erdos-757/experiments/prover/L009/indep; P8=/home/user/Erdos-757/experiments/prover/L008/indep
cls() { ./bin/canon $1 | sort -u; }
for x in "6 $P9/cell_6_3_2.txt 6_3_2" "8 $P9/cell_8_5_3.txt 8_5_3" "10 $P9/cell_10_7_4.txt 10_7_4" "13 $P9/cell_13_8_5.txt 13_8_5" "8 $P10/cell_8_6_3.txt 8_6_3" "9 $P10/cell_9_4_3.txt 9_4_3" "11 $P10/cell_11_7_4.txt 11_7_4" "14 $P10/cell_14_8_5.txt 14_8_5"; do set -- $x
  grep ^FOUND $2 | cls $1 > out/cls_prover_$3.txt; grep ^FOUND out/g_${3}_d3.txt | cls $1 > out/cls_mine_$3.txt
  echo "$3: prover labelled $(grep -c ^FOUND $2) -> $(wc -l < out/cls_prover_$3.txt) classes; mine $(wc -l < out/cls_mine_$3.txt) classes; $(cmp -s out/cls_prover_$3.txt out/cls_mine_$3.txt && echo IDENTICAL || echo DIFFERENT)"; done
for x in "12 $P8/mine_12_10_5_deg3.txt.gz 12_10_5" "15 $P8/mine_15_11_6_deg3.txt.gz 15_11_6"; do set -- $x
  zcat $2 | grep ^FOUND | cls $1 > out/cls_prover_$3.txt; grep ^FOUND out/g_${3}_d3.txt | cls $1 > out/cls_mine_$3.txt
  echo "$3: prover labelled $(zcat $2 | grep -c ^FOUND) -> $(wc -l < out/cls_prover_$3.txt) classes; mine $(wc -l < out/cls_mine_$3.txt) classes; $(cmp -s out/cls_prover_$3.txt out/cls_mine_$3.txt && echo IDENTICAL || echo DIFFERENT)"; done
echo "--- direct genbg enumeration of connected linear (18,12,>=7) with Delta<=3 (no F7/P3 pruning):"
s=$(date +%s); TAU0=7 ./bin/genbg32 -q -c -Z1 -d1:3 -D3:3 18 12 36:36 > out/g_18_12_7_d3.txt 2> logs/g_18_12_7_d3.err; e=$(date +%s)
echo "found $(grep -c FOUND out/g_18_12_7_d3.txt); $(cat logs/g_18_12_7_d3.err) [$((e-s)) s]"
./bin/myfilter FOUND 18 all < out/g_18_12_7_d3.txt > out/g_18_12_7_d3_filtered.txt; tail -1 out/g_18_12_7_d3_filtered.txt
echo CLASSESDONE
