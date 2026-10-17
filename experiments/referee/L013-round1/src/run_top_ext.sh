#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L013-round1
for b in "23 14 9 2 3" "23 14 9 3 3" "23 20 10 3 3" "24 12 9 2 2" "24 13 9 2 3" "24 13 9 3 3" "24 18 10 3 3" "25 17 10 3 3" "25 22 11 3 3" "26 15 10 2 3" "26 15 10 3 3" "26 21 11 3 3"; do
  set -- $b; n=$1; m=$2; t=$3; d=$4; D=$5
  s=$(date +%s)
  timeout 3000 nice -n 10 ./bin/myext $((n-1)) $t $d $D < out/inputs/in_${n}_${m}_${t}_d${d}.txt > out/ext/top_${n}_${m}_${t}_d${d}.txt
  echo "($n,$m,$t,D$D) branch d=$d: $(tail -1 out/ext/top_${n}_${m}_${t}_d${d}.txt) secs=$(( $(date +%s) - s ))"
done
