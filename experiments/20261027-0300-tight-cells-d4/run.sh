#!/bin/bash
# usage: run.sh n,m,t,D ...   (streamed L014 driver, NPROC=1, nice 15)
cd "$(dirname "$0")"
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log WORKDIR=$PWD/out/work PROGRESS=$PWD/out/progress.jsonl NPROC=1 MD=10
exec nice -n 15 timeout ${TMO:-3600} python3 src/run_cells.py "$@"
