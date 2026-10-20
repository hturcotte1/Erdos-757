#!/bin/bash
# (L016) full chain with ext_d_fast (fast/bin/ext_d = bin/ext_d_fast), step 1: cell(24,16,9,3) in out/cellsF (seeded with the 198
# refereed lists of L013/L014 and the 45 small cells of run A, all recomputed here).
cd /home/user/Erdos-757/experiments/prover/L016
CELLDIR=$PWD/out/cellsF WORKDIR=$PWD/out/workF ENGINELOG=$PWD/out/logs/engine_F.log PROGRESS=$PWD/out/progress_F.jsonl NPROC=${NP:-1} MD=10 \
  nice -n ${NI:-19} timeout ${TO:-7000} python3 fast/run_cells.py "$@" >> out/logs/run_F.log 2>&1
echo "rc=$? keys=$*" >> out/logs/run_F.log
