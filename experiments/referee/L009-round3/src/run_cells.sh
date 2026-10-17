#!/bin/bash
D=/home/user/Erdos-757/experiments/referee/L009-round3; cd $D; mkdir -p out/cells
for c in "6 3 2 3" "8 5 3 3" "10 7 4 3" "10 8 4 3" "13 8 5 3" "13 9 5 3" "16 10 6 3" "16 9 6 9" "16 9 6 3" "18 10 7 10" "13 8 5 8" "18 11 7 3" "17 12 7 3" "14 12 6 3"; do set -- $c
  n=$1; m=$2; t=$3; d=$4; tag=${n}_${m}_${t}_D${d}
  s=$(date +%s); TAU0=$t ./bin/genbg_my -q -c -Z1 -d1:$d -D$d:3 $n $m $((3*m)):$((3*m)) > out/cells/g_$tag.txt 2> out/cells/g_$tag.err; e=$(date +%s)
  echo "cell ($n,$m,tau>=$t,D<=$d) [$((e-s)) s]: $(grep MYSUMMARY out/cells/g_$tag.err)"
done
