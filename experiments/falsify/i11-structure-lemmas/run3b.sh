#!/bin/bash
cd /home/user/Erdos-757/experiments/falsify/i11-structure-lemmas
for n in 18 19 20 21 22 23 24 25 26 27 28 29 30; do
  ms=""
  for m in $(seq $((n-9)) $((n-2))); do
    r=$(( (3*n+2*m) % 11 ))
    if [ $m -ge $((n-4)) ] && [ $m -le $((n-2)) ]; then ms="$ms $m"; elif [ $r -eq 0 ] || [ $r -eq 1 ]; then ms="$ms $m"; fi
  done
  for m in $ms; do
    nice -n 15 timeout 900 src/lsearch $n $m 20000 300 $((n*100+m)) 0.5 0.6 seeds.txt > out3b/n${n}_m${m}.txt 2>&1
    tail -1 out3b/n${n}_m${m}.txt | cut -c1-200
  done
done
echo ALLDONE
