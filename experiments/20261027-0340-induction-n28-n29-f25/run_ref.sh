#!/bin/bash
# recompute (21,18,9,4) and (24,19,10,4) (otherwise taken from non-refereed sources) from refereed seeds + cells computed here only
cd "$(dirname "$0")"
export CELLDIR=$PWD/out/cells_ref ENGINELOG=$PWD/out/engine_ref.log WORKDIR=$PWD/out/work_ref PROGRESS_TSV=$PWD/progress_ref.tsv NPROC=1 MD=10 SORTMEM=400M
mkdir -p out/work_ref
for k in 21,18,9,4 24,19,10,4; do nice -n 5 timeout 10800 python3 src/run1.py $k >> out/run_ref.log 2>&1; done
