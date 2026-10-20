#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L013-round3
for c in "23 13 9 2" "24 12 9 2" "26 14 10 2" "22 11 7 2" "23 13 8 2" "22 11 8 2"; do set -- $c
  s=$(date +%s); nice -n 10 timeout 1500 ./bin/genbg -c -Z1 -d1:3 -D$4:3 -q $1 $2 $((3*$2)):$((3*$2)) 2>logs/genbg_$1_$2_$3_D$4.err | nice -n 10 ./bin/gfilt $1 $2 $3 $4 > out/g_$1_$2_$3_D$4.txt; e=$(date +%s)
  echo "cell($1,$2,$3,$4): $(tail -1 out/g_$1_$2_$3_D$4.txt) wall=$((e-s))s genbg_exit=${PIPESTATUS[0]}"; done
