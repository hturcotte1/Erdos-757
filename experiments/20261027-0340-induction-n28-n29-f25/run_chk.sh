#!/bin/bash
# recompute the two cells that came from the concurrent d4 worker, in an isolated cell directory (symlinks to all other cells)
cd "$(dirname "$0")"
export CELLDIR=$PWD/out/cells_chk ENGINELOG=$PWD/out/engine_chk.log WORKDIR=$PWD/out/work_chk PROGRESS_TSV=$PWD/progress_chk.tsv NPROC=1 MD=10 SORTMEM=400M
for k in 26,17,10,3 27,20,11,3; do nice -n 5 timeout 10800 python3 src/run1.py $k >> out/run_chk.log 2>&1; done
