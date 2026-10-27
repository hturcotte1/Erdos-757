#!/bin/bash
# usage: run.sh n,m,t,D ...   (streamed L014 driver, NPROC=1, nice 15)
cd "$(dirname "$0")"
export CELLDIR=$PWD/ctl/cells ENGINELOG=$PWD/ctl/engine.log WORKDIR=$PWD/ctl/work PROGRESS=$PWD/ctl/progress.jsonl NPROC=1 MD=10
exec nice -n 15 timeout ${TMO:-3600} python3 src/run_cells.py "$@"
