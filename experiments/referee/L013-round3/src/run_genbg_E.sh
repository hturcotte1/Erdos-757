#!/bin/bash
# Delta <= 3 cells with n <= 24 in the normal layout (points first): unmodified default genbg + my filter
cd /home/user/Erdos-757/experiments/referee/L013-round3; P=/home/user/Erdos-757/experiments/prover/L013/out/cells
for c in "22 11 8 3" "23 11 8 3" "22 12 8 3" "23 12 8 3" "22 13 8 3" "24 13 9 3"; do set -- $c
  s=$(date +%s); nice -n 10 timeout 2400 ./bin/genbg -c -Z1 -d1:3 -D$4:3 -q $1 $2 $((3*$2)):$((3*$2)) 2>logs/genbgE_$1_$2_$3_D$4.err | nice -n 10 ./bin/gfilt $1 $2 $3 $4 > out/gE_$1_$2_$3_D$4.txt; e=$(date +%s)
  pc=$(grep -c '^FOUND' $P/cell_$1_$2_$3_D$4.txt); mc=$(grep -c '^FOUND' out/gE_$1_$2_$3_D$4.txt)
  echo "cell($1,$2,$3,$4): mine=$mc prover=$pc $( [ "$mc" = "$pc" ] && echo EQUAL || echo DIFFERENT) | $(tail -1 out/gE_$1_$2_$3_D$4.txt) wall=$((e-s))s genbg_exit=${PIPESTATUS[0]} err=$(cat logs/genbgE_$1_$2_$3_D$4.err | tr '\n' ' ')"; done
