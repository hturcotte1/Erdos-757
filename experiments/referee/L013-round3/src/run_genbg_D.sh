#!/bin/bash
# the 16 direct cells new in L013 (not in L012's lists): unmodified genbg (normal layout, n <= 21) + my filter; compare with the prover's counts
cd /home/user/Erdos-757/experiments/referee/L013-round3; P=/home/user/Erdos-757/experiments/prover/L013/out/cells
for c in "6 3 1 2" "6 4 1 2" "8 5 2 2" "9 4 2 2" "9 5 2 2" "9 6 3 3" "11 6 3 2" "12 6 3 2" "12 7 4 3" "14 7 4 2" "15 7 4 2" "15 8 5 3" "17 8 5 2" "17 8 6 2" "18 9 6 3" "20 10 7 2" "21 10 7 2" "21 10 7 3" "13 10 5 3"; do set -- $c
  s=$(date +%s); nice -n 10 timeout 1800 ./bin/genbg -c -Z1 -d1:3 -D$4:3 -q $1 $2 $((3*$2)):$((3*$2)) 2>logs/genbgD_$1_$2_$3_D$4.err | nice -n 10 ./bin/gfilt $1 $2 $3 $4 > out/gD_$1_$2_$3_D$4.txt; e=$(date +%s)
  pc=$(grep -c '^FOUND' $P/cell_$1_$2_$3_D$4.txt); mc=$(grep -c '^FOUND' out/gD_$1_$2_$3_D$4.txt)
  echo "cell($1,$2,$3,$4): mine=$mc prover=$pc $( [ "$mc" = "$pc" ] && echo EQUAL || echo DIFFERENT) | $(tail -1 out/gD_$1_$2_$3_D$4.txt) wall=$((e-s))s err=$(cat logs/genbgD_$1_$2_$3_D$4.err | tr '\n' ' ')"; done
