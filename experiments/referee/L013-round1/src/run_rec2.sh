#!/bin/bash
# one recursion level of further cells: inputs from the prover's component lists (own decompositions), own extension (myext3),
# all HIT lines (connected, in C, tau = t, Delta <= 3) collected per cell, then VF2 class comparison with the prover's list.
cd /home/user/Erdos-757/experiments/referee/L013-round1
for c in "18 12 7" "21 13 8" "23 12 8" "16 11 6" "19 12 7" "22 13 8" "24 15 9"; do
  set -- $c; n=$1; m=$2; t=$3; tp=$((t-1)); all=out/ext/rec2_${n}_${m}_${t}_all.txt; : > $all
  for d in 2 3; do
    Sp=$((3*(n-1)+2*(m-d)-11*tp)); lo=$(( (3*m + n - 1) / n )); if [ $d -lt $lo ] || [ $Sp -lt 0 ]; then continue; fi
    timeout 900 nice -n 10 python3 src/build_inputs.py out/prover_cells/cells $n $m $t $d $tp > out/inputs/in_${n}_${m}_${t}_d${d}.txt 2> out/inputs/in_${n}_${m}_${t}_d${d}.log
    s=$(date +%s)
    timeout 3600 nice -n 10 ./bin/myext3 $((n-1)) $t $d 3 < out/inputs/in_${n}_${m}_${t}_d${d}.txt > out/ext/rec2_${n}_${m}_${t}_d${d}.txt; rc=$?
    grep '^HIT' out/ext/rec2_${n}_${m}_${t}_d${d}.txt >> $all
    echo "($n,$m,$t,3) d=$d rc=$rc: $(tail -1 out/inputs/in_${n}_${m}_${t}_d${d}.log) | $(tail -1 out/ext/rec2_${n}_${m}_${t}_d${d}.txt | sed 's/SUMMARY //') secs=$(( $(date +%s) - s ))"
  done
  echo "($n,$m,$t,3) total connected hits $(wc -l < $all); prover classes $(grep -c '^FOUND' out/prover_cells/cells/cell_${n}_${m}_${t}_D3.txt)"
  if [ -s $all ]; then timeout 3000 nice -n 10 python3 src/iso_compare.py $n $all out/prover_cells/cells/cell_${n}_${m}_${t}_D3.txt; fi
done
