#!/bin/bash
# Exact commands for experiments/20261017-2150-i11-n27 (run from this folder).  NPROC=1, nice 19, MD=10, 6 h cap.
cd "$(dirname "$0")"; mkdir -p out/cells
[ -e bin ] || ln -s ../prover/L012/bin bin
# seeding: symlink every existing cell file (1925, 1735, 1720, 1645, L013, L012 out/cells) into out/cells (see seed_cells.txt)
python3 arith.py > arith_output.txt     # copy of the 1720 arith.py (n=26,27)
python3 plan.py > plan_output.txt       # full recursion plan: cells needed, exists or missing
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log NPROC=1 MD=10
nice -n 19 python3 run_all.py > out/driver.log 2>&1
