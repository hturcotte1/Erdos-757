#!/bin/bash
# (L016) the top cell (27,25,12,3) once more with the Gosper build bin/ext_d (MAXP 640), from run F's lists (out/cellsG = copy of
# out/cellsF without the top list)
cd /home/user/Erdos-757/experiments/prover/L016
CELLDIR=$PWD/out/cellsG WORKDIR=$PWD/out/workG ENGINELOG=$PWD/out/logs/engine_G.log PROGRESS=$PWD/out/progress_G.jsonl NPROC=1 MD=10 \
  nice -n 5 timeout 1200 python3 run_cells.py 27,25,12,3 > out/logs/run_G.log 2>&1
echo "rc=$?" >> out/logs/run_G.log
