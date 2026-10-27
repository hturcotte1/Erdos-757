#!/bin/bash
# completes the growth runs after the first script was stopped (K=4/10 greedy is slow); skips (n,K) pairs already complete
cd "$(dirname "$0")"
export I11_OUT=out/low_grow.txt I11_CONN=0 I11_DMAX=3
for n in $(seq 32 40); do
  mlo=$(( n/2 )); mhi=$((n-2))
  grep -q "GROW n=$n m=$mhi K=1 " out/grow_K1.txt || timeout 3000 nice -n 5 ./i11 grow $n $mlo $mhi 200000 $((n*1000+1)) 1 >> out/grow_K1.txt
  grep -q "GROW n=$n m=$mhi K=4 " out/grow_K4.txt || timeout 3000 nice -n 5 ./i11 grow $n $mlo $mhi 10000 $((n*1000+2)) 4 >> out/grow_K4.txt
  grep -q "GROW n=$n m=$mhi K=10 " out/grow_K10.txt || timeout 3000 nice -n 5 ./i11 grow $n $mlo $mhi 3000 $((n*1000+3)) 10 >> out/grow_K10.txt
done
echo done > out/grow_done.txt
