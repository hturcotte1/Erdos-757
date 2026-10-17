#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L013-round3
for b in "23 14 9 3 3 8" "24 13 9 3 3 8" "26 15 10 3 3 9" "24 18 10 3 3 9" "25 17 10 3 3 9" "23 20 10 3 3 9" "26 21 11 3 3 10" "23 15 9 3 3 8" "24 14 9 3 3 8" "21 18 9 3 3 8" "24 19 10 3 3 9" "25 18 10 3 3 9"; do set -- $b
  tag=$1_$2_$3_D$4_d$5_tp$6; r=$(nice -n 10 timeout 3000 ./bin/xext_ref2 $(($1-1)) $6 $3 $5 $(($5-1)) < out/in_$tag.txt | tail -1 | sed 's/.*graphs=/graphs=/; s/nodes=[0-9]* last_level_candidates=[0-9]* //; s/validate=0\/0//')
  echo "($1,$2,$3,$4) d=$5 tp=$6: $r"; done
