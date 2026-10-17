#!/bin/bash
# every branch of the twelve top-level cells: build inputs with MY decompositions from the prover's cell files, run MY extension program
cd /home/user/Erdos-757/experiments/referee/L013-round3; P=/home/user/Erdos-757/experiments/prover/L013/out/cells
for b in "23 13 9 2 2 8" "25 16 10 2 2 9" "26 14 10 2 2 9" "23 14 9 3 2 8" "24 12 9 2 2 8" "24 13 9 3 2 8" "24 13 9 3 3 8" "26 15 10 3 2 9" "26 15 10 3 3 9" "24 18 10 3 3 9" "25 22 11 3 3 10" "25 17 10 3 3 9" "23 20 10 3 3 9" "26 21 11 3 3 10"; do set -- $b
  tag=$1_$2_$3_D$4_d$5_tp$6; python3 src/build_inputs.py $1 $2 $3 $4 $5 $6 $P > out/in_$tag.txt 2> logs/build_$tag.txt
  ni=$(grep -c . out/in_$tag.txt); s=$(date +%s)
  if [ "$ni" -gt 0 ]; then nice -n 10 timeout 3000 ./bin/xext_ref $(($1-1)) $6 $3 $5 $(($5-1)) < out/in_$tag.txt > out/x_$tag.txt; r=$(tail -1 out/x_$tag.txt); else r="no inputs"; fi
  e=$(date +%s); echo "BRANCH ($1,$2,$3,$4) d=$5 tp=$6: inputs=$ni [$(grep TOTAL logs/build_$tag.txt)] $r wall=$((e-s))s"; done
