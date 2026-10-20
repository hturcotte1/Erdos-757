#!/bin/bash
# Referee round 2: top-level recomputation of every recursive cell of the prover's engine (sequential, one process at a time).
cd /home/user/Erdos-757/experiments/referee/L012-round2
while read n m t D; do
  echo "=== $n $m $t $D"
  timeout 900 nice -n 5 python3 src/recompute_cell.py $n $m $t $D 2>&1 | grep -E "^  \{|CELL|NOTE|Error|Traceback|missing"
done < out/rec_cells.txt
echo ALLDONE
