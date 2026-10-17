#!/bin/bash
# swapped classes: first class = m edge-vertices (degree 3), second class = n points (degree 1..D); -Z1 = two points share <= 1 edge (linear)
cd /home/user/Erdos-757/experiments/referee/L013-round3
for c in "22 11 7 2" "23 13 8 2" "26 14 10 2" "25 12 9 2" "25 13 9 2" "22 11 8 3" "25 12 9 3" "23 11 8 3"; do set -- $c
  s=$(date +%s); nice -n 10 timeout 2400 ./bin/genbg -c -Z1 -d3:1 -D3:$4 -q $2 $1 $((3*$2)):$((3*$2)) 2>logs/genbgS_$1_$2_$3_D$4.err | nice -n 10 ./bin/gfilt $1 $2 $3 $4 swap > out/gS_$1_$2_$3_D$4.txt; e=$(date +%s)
  echo "cell($1,$2,$3,$4) swapped: $(tail -1 out/gS_$1_$2_$3_D$4.txt) wall=$((e-s))s genbg_exit=${PIPESTATUS[0]} err=$(cat logs/genbgS_$1_$2_$3_D$4.err | tr '\n' ' ')"; done
