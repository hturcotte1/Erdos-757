#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L013-round1
for b in "23 15 9 2 3" "23 15 9 3 3" "24 14 9 2 3" "24 14 9 3 3" "21 18 9 3 3" "24 19 10 3 3" "25 18 10 3 3"; do
  set -- $b; n=$1; m=$2; t=$3; d=$4; D=$5
  s=$(date +%s)
  timeout 5400 nice -n 10 ./bin/myext $((n-1)) $t $d $D < out/inputs/in_${n}_${m}_${t}_d${d}.txt > out/ext/sub_${n}_${m}_${t}_d${d}.txt
  echo "($n,$m,$t,D$D) branch d=$d: $(tail -1 out/ext/sub_${n}_${m}_${t}_d${d}.txt) secs=$(( $(date +%s) - s ))"
done
