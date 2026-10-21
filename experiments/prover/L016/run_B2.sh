#!/bin/bash
# (L016) contingency / item (b): cell(26,22,11,3) and cell(27,25,12,3) with ext_d_fast in out/cellsB, i.e. from the worker's
# cell(25,19,10,3) (copied, NOT recomputed there) and the 198 refereed lists.
cd /home/user/Erdos-757/experiments/prover/L016
CELLDIR=$PWD/out/cellsB WORKDIR=$PWD/out/workB ENGINELOG=$PWD/out/logs/engine_B2.log PROGRESS=$PWD/out/progress_B2.jsonl NPROC=1 MD=10 \
  nice -n 10 timeout 5400 python3 fast/run_cells.py 26,22,11,3 27,25,12,3 > out/logs/run_B2.log 2>&1
echo "rc=$?" >> out/logs/run_B2.log
