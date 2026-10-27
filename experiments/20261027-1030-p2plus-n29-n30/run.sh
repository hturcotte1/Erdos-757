#!/bin/bash
# usage: run.sh n,m,t,D ...  (streamed L016 driver, NPROC=1, nice 19; MAXP640 ext_d_fast = src/bin/ext_d)
cd "$(dirname "$0")"
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log WORKDIR=$PWD/out/work PROGRESS=$PWD/out/progress.jsonl NPROC=1 MD=10
exec nice -n 19 timeout ${TMO:-10800} python3 src/run_cells.py "$@"
