#!/bin/bash
# BONUS (not requested): try the three open n=25 cells with the engine, 40 min cap each; uses a copy of out/cells.
cd "$(dirname "$0")"
export CELLDIR=$PWD/out/cells25 ENGINELOG=$PWD/out/engine_n25.log RESJSONL=results_cells_n25.jsonl NPROC=3
for c in "25 16 10 2" "25 17 10 3" "25 22 11 3"; do
  timeout 2400 python3 run_cells.py $c > "out/run_n25_$(echo $c | tr ' ' '_').log" 2>&1 || echo "TIMEOUT/FAIL $c" >> out/n25_status.txt
done
echo done >> out/n25_status.txt
