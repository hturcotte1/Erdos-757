#!/bin/bash
# (L016) the 45 small new cells of the n = 27 tree (incl. the four sparse top cells (27,13,10,2), (27,18,11,2), (27,14,10,3),
# (27,19,11,3)) in out/cells, seeded only with the 198 refereed lists of L013/L014; post-order of plan16.py.
cd /home/user/Erdos-757/experiments/prover/L016
CELLDIR=$PWD/out/cells WORKDIR=$PWD/out/work ENGINELOG=$PWD/out/logs/engine_A.log PROGRESS=$PWD/out/progress_A.jsonl NPROC=1 MD=10 \
  nice -n 10 timeout 3000 python3 run_cells.py $(cat listA.txt) > out/logs/run_A.log 2>&1
echo "rc=$?" >> out/logs/run_A.log
