#!/bin/bash
# Referee round 2 (L008): Lemma A' without Henning-Yeo.  For every connected cell (n,m) with n<=15 and lo<=m, enumerate all
# connected linear 3-graphs with tau >= lo (no degree bound) with bfs_enum, then count those in O+ (F7-free and P3) with ext_r2.
cd /home/user/Erdos-757/experiments/referee/L008-round2
python3 -c "
import sys
for n in range(3,16):
    for m in range((n)//2, n-1):
        if n > 2*m+1: continue
        lo=(3*n+2*m)//11+1
        if lo<=m: print(n,m,lo)
" > out/hyfree_cells.txt
while read n m t; do
  s=$(date +%s)
  timeout 900 nice -n 5 ./bin/bfs_enum $n $m $t 100 1 1 > out/hyfree_${n}_${m}_${t}.txt 2>/dev/null; rc=$?
  e=$(date +%s)
  f=$(./bin/ext_r2 FILTER $n < out/hyfree_${n}_${m}_${t}.txt | tail -1)
  echo "cell ($n,$m,>=$t) rc=$rc [$((e-s)) s] $(tail -1 out/hyfree_${n}_${m}_${t}.txt | sed 's/.*classes=/classes=/') | $f"
done < out/hyfree_cells.txt
