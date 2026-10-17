#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L013-round1
for b in "20 15 8 3 7" "23 16 9 3 8"; do
  set -- $b; n=$1; m=$2; t=$3; d=$4; tp=$5
  timeout 900 nice -n 10 python3 src/build_inputs.py out/prover_cells/cells $n $m $t $d $tp > out/inputs/in_${n}_${m}_${t}_d${d}.txt 2> out/inputs/in_${n}_${m}_${t}_d${d}.log
  s=$(date +%s)
  timeout 3600 nice -n 10 ./bin/myext2 $((n-1)) $t $d 3 < out/inputs/in_${n}_${m}_${t}_d${d}.txt > out/ext/rec_${n}_${m}_${t}_d${d}.txt
  echo "($n,$m,$t,3) d=$d: $(tail -1 out/inputs/in_${n}_${m}_${t}_d${d}.log) | $(tail -1 out/ext/rec_${n}_${m}_${t}_d${d}.txt) secs=$(( $(date +%s) - s ))"
  timeout 3000 nice -n 10 python3 src/iso_compare.py $n out/ext/rec_${n}_${m}_${t}_d${d}.txt out/prover_cells/cells/cell_${n}_${m}_${t}_D3.txt
done
