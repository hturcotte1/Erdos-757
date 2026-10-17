#!/bin/bash
# check 6: class sets of the prover's component lists vs referee genbg (connected, linear, Delta<=3, tau>=T0); classes in C
P8=/home/user/Erdos-757/experiments/prover/L008/indep; P9=/home/user/Erdos-757/experiments/prover/L009/indep; P10=/home/user/Erdos-757/experiments/prover/L010/out
for x in "6 3 2 $P9/cell_6_3_2.txt" "8 5 3 $P9/cell_8_5_3.txt" "10 7 4 $P9/cell_10_7_4.txt" "13 8 5 $P9/cell_13_8_5.txt" "8 6 3 $P10/cell_8_6_3.txt" "9 4 3 $P10/cell_9_4_3.txt" "11 6 4 $P10/cell_11_6_4.txt" "11 7 4 $P10/cell_11_7_4.txt" "14 8 5 $P10/cell_14_8_5.txt" "16 9 6 $P10/cell_16_9_6.txt" "17 9 6 $P10/cell_17_9_6.txt" "12 10 5 $P8/mine_12_10_5_deg3.txt.gz" "15 11 6 $P8/mine_15_11_6_deg3.txt.gz"; do
  set -- $x
  TAU0=$3 F7PRUNE=0 ./bin/genbg_r2_32 -q -c -Z1 -d1:3 -D3:3 $1 $2 $((3*$2)):$((3*$2)) > out/comp_$1_$2_$3.txt 2>/dev/null
  ./bin/canon $1 < out/comp_$1_$2_$3.txt | awk '{print $1}' | sort -u > out/cls_comp_$1_$2_$3_mine.txt
  if [[ $4 == *.gz ]]; then zcat $4 | grep "^FOUND" > out/tmp_list.txt; else grep "^FOUND" $4 > out/tmp_list.txt; fi
  nl=$(wc -l < out/tmp_list.txt); ./bin/canon $1 < out/tmp_list.txt | awk '{print $1}' | sort -u > out/cls_comp_$1_$2_$3_prover.txt
  same=$(cmp -s out/cls_comp_$1_$2_$3_mine.txt out/cls_comp_$1_$2_$3_prover.txt && echo SAME || echo DIFFERENT)
  echo "($1,$2,>=$3) D<=3: mine $(wc -l < out/cls_comp_$1_$2_$3_mine.txt) classes ($(grep -c 'f7=0 p3=1' out/comp_$1_$2_$3.txt) in C), prover $nl labelled -> $(wc -l < out/cls_comp_$1_$2_$3_prover.txt) classes: $same"
done; rm -f out/tmp_list.txt
