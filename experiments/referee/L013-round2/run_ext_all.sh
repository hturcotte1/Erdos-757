#!/bin/bash
# Referee: final extension step of every top-level branch and of the five C9 sub-cells, from the prover's cell lists,
# with the referee's decompositions (decomp_ref.py), random relabelling of every input, and the referee's extension program (refx ext).
cd /home/user/Erdos-757/experiments/referee/L013-round2
CD=out/prover_cells/cells
run() { n=$1; m=$2; t=$3; d=$4; tp=$5; NG=$((n-1)); EP=$((d-1)); f=out/inp/in_${n}_${m}_${t}_d${d}.txt
  timeout 1200 nice -n 10 python3 build_inputs.py $CD $n $m $t $d $tp --perm $((n*1000+m*10+d)) > $f 2> $f.log
  echo "BRANCH ($n,$m,$t) d=$d tp=$tp $(head -1 $f.log)"
  timeout 3600 nice -n 10 ./bin/refx ext $NG $tp $t $d $EP < $f > out/inp/res_${n}_${m}_${t}_d${d}.txt
  grep SUMMARY out/inp/res_${n}_${m}_${t}_d${d}.txt; grep -c GOOD out/inp/res_${n}_${m}_${t}_d${d}.txt; }
for spec in "$@"; do run $spec; done
