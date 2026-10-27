#!/bin/bash
# random growth: 200000 samples per n (K=1), then 60000 with K=4 and 20000 with K=10 greedy-by-tau
cd "$(dirname "$0")"
export I11_OUT=out/low_grow.txt I11_CONN=0 I11_DMAX=3
for n in $(seq 28 40); do
  mlo=$(( (n-1+1)/2 )); mhi=$((n-2))
  timeout 3000 nice -n 5 ./i11 grow $n $mlo $mhi 200000 $((n*1000+1)) 1 >> out/grow_K1.txt
  timeout 3000 nice -n 5 ./i11 grow $n $mlo $mhi 60000 $((n*1000+2)) 4 >> out/grow_K4.txt
  timeout 3000 nice -n 5 ./i11 grow $n $mlo $mhi 20000 $((n*1000+3)) 10 >> out/grow_K10.txt
done
echo done > out/grow_done.txt
