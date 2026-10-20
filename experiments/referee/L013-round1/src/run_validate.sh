#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L013-round1
for c in "A 8 4" "C 10 5" "D 7 3" "E 12 5" "B 14 6"; do set -- $c; for d in 2 3 4; do
  ./bin/myext $2 $3 $d 9 all < out/val_$1.txt | grep '^SET' | sort > out/v_my_$1_$d.txt
  timeout 900 nice -n 10 python3 src/bf_ext.py $2 $3 $d < out/val_$1.txt | sort > out/v_bf_$1_$d.txt; rc=${PIPESTATUS[0]}
  echo "case $1 (NG=$2,t=$3) d=$d: myext $(wc -l < out/v_my_$1_$d.txt) bf $(wc -l < out/v_bf_$1_$d.txt) bf_rc=$rc $(cmp -s out/v_my_$1_$d.txt out/v_bf_$1_$d.txt && echo IDENTICAL || echo DIFFERENT)"
done; done
