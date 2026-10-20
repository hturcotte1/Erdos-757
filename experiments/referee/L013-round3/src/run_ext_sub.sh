#!/bin/bash
# the five C9 sub-cells (empty connected cells resting on the recursion alone): their final extension steps with MY program
cd /home/user/Erdos-757/experiments/referee/L013-round3; P=/home/user/Erdos-757/experiments/prover/L013/out/cells
for b in "23 15 9 3 2 8" "23 15 9 3 3 8" "24 14 9 3 2 8" "24 14 9 3 3 8" "21 18 9 3 3 8" "24 19 10 3 3 9" "25 18 10 3 3 9"; do set -- $b
  tag=$1_$2_$3_D$4_d$5_tp$6; python3 src/build_inputs.py $1 $2 $3 $4 $5 $6 $P > out/in_$tag.txt 2> logs/build_$tag.txt
  ni=$(grep -c . out/in_$tag.txt); s=$(date +%s)
  if [ "$ni" -gt 0 ]; then nice -n 10 timeout 5400 ./bin/xext_ref $(($1-1)) $6 $3 $5 $(($5-1)) < out/in_$tag.txt > out/x_$tag.txt; r=$(tail -1 out/x_$tag.txt); else r="no inputs"; fi
  e=$(date +%s); echo "SUBCELL ($1,$2,$3,$4) d=$5 tp=$6: inputs=$ni [$(grep TOTAL logs/build_$tag.txt)] $r wall=$((e-s))s"; done
