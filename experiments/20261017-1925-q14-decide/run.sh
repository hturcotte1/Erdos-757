#!/bin/bash
# Exact commands for experiments/20261017-1925-q14-decide (run from this directory). NPROC=2, nice 5, MD=10.
cd "$(dirname "$0")"; mkdir -p out/cells
P=../20261017-1735-q14-cell-sizes
[ -e bin ] || ln -s ../prover/L012/bin bin
for f in engine.py decomp22.py decomps.py; do [ -e $f ] || cp $P/$f .; done
# reuse the already computed cell files of the previous probe by symlink (not recomputed)
for f in $P/out/cells/cell_*; do b=$(basename $f); [ -e out/cells/$b ] || ln -s $(realpath $f) out/cells/$b; done
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log NPROC=2 MD=10
# step 1: cell(22,18,9,3), cap 100 min
nice -n 5 timeout 6000 python3 run_one.py 22 18 9 3 > out/run_22_18_9.log 2>&1
# step 2: cell(23,21,10,3)
nice -n 5 timeout 3600 python3 run_one.py 23 21 10 3 > out/run_23_21_10.log 2>&1
# note: the first attempt of step 2 ran all 133,804 inputs (0 HIT lines) but the streamed pipeline aborted because `grep` returned rc 1 on empty
# input under pipefail; mystream.py was patched with `(grep ... || true)` and step 2 was rerun with the identical command:
# nice -n 5 timeout 3600 python3 run_one.py 23 21 10 3 > out/run_23_21_10.log 2>&1
