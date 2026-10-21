#!/bin/bash
# (L016) cell(26,22,11,3) in full (streamed driver of L014, unchanged engine of L012, ext_d MAXP=640) in out/cellsB, seeded with the
# 198 refereed lists of L013/L014 and the worker's cell(25,19,10,3) (NOT recomputed in full; see the certificate).
cd /home/user/Erdos-757/experiments/prover/L016
CELLDIR=$PWD/out/cellsB WORKDIR=$PWD/out/workB ENGINELOG=$PWD/out/logs/engine_B.log PROGRESS=$PWD/out/progress_B.jsonl NPROC=3 MD=10 \
  nice -n 5 timeout 9000 python3 run_cells.py 26,22,11,3 > out/logs/run_B.log 2>&1
echo "rc=$?" >> out/logs/run_B.log
