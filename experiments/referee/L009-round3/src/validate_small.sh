#!/bin/bash
# For small cells (n m T0 D): class set of my brute force (all labelled graphs) == class set of my genbg == class set of prover's enum_conn
D=/home/user/Erdos-757/experiments/referee/L009-round3; P=$D/prover_copy/indep
cd $D; mkdir -p out/val
for c in "6 3 2 3" "7 4 2 3" "7 5 3 3" "8 4 3 3" "8 5 3 3" "8 6 3 3" "8 6 4 3" "9 4 3 3" "9 5 3 3" "9 6 3 3" "9 6 4 4" "9 7 4 3" "9 7 3 4" "10 5 4 4" "10 6 4 3"; do set -- $c
  n=$1; m=$2; t=$3; d=$4; tag=${n}_${m}_${t}_${d}
  ./bin/bf $n $m $t $d > out/val/bf_$tag.txt 2> out/val/bf_$tag.err
  TAU0=$t ./bin/genbg_my -q -c -Z1 -d1:$d -D$d:3 $n $m $((3*m)):$((3*m)) > out/val/g_$tag.txt 2> out/val/g_$tag.err
  $P/enum_conn $n $m $t $d 1 > out/val/e_$tag.txt
  ./src/classes.sh $n BF < out/val/bf_$tag.txt > out/val/bf_$tag.cls
  grep "^G " out/val/g_$tag.txt | ./src/classes.sh $n G < /dev/stdin > out/val/g_$tag.cls
  ./src/classes.sh $n FOUND < out/val/e_$tag.txt > out/val/e_$tag.cls
  nb=$(wc -l < out/val/bf_$tag.cls); ng=$(wc -l < out/val/g_$tag.cls); ne=$(wc -l < out/val/e_$tag.cls)
  lab=$(grep -c '^BF' out/val/bf_$tag.txt); lin=$(grep -o 'linear_labelled=[0-9]*' out/val/bf_$tag.err)
  r1=$(cmp -s out/val/bf_$tag.cls out/val/g_$tag.cls && echo same || echo DIFF); r2=$(cmp -s out/val/bf_$tag.cls out/val/e_$tag.cls && echo same || echo DIFF)
  echo "cell ($n,$m,tau>=$t,D<=$d): bf labelled=$lab ($lin) classes bf=$nb genbg=$ng enum_conn=$ne | bf~genbg:$r1 bf~enum_conn:$r2"
done
