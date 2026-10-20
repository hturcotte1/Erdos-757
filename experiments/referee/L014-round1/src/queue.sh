#!/bin/bash
# sequential queue of own one-level recomputations (2 parallel parts each); waits for the running (19,17,8,3) job first
cd /home/user/Erdos-757/experiments/referee/L014-round1
while pgrep -f "myrec2.sh 19 17 8 3" > /dev/null; do sleep 10; done
for c in "22 18 9 3" "21 15 8 3" "18 14 7 3" "15 13 6 3" "15 12 6 3" "16 11 6 3" "17 11 6 3" "17 13 7 3" "18 12 7 3" "19 12 7 3" "20 12 7 3" "15 11 6 3" "14 12 6 3" "17 14 7 3" "21 18 9 3" "23 21 10 4"; do
  set -- $c
  ./src/myrec2.sh $1 $2 $3 $4 2 > logs/myrec2_$1_$2_$3_$4.txt 2>&1
  grep RESULT logs/myrec2_$1_$2_$3_$4.txt >> logs/queue_results.txt || echo "NO RESULT $c" >> logs/queue_results.txt
done
echo ALLDONE >> logs/queue_results.txt
