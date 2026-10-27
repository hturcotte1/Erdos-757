#!/bin/bash
# Referee L023 round 1: recompute cell(17,15,7,3) and cell(21,19,9,3) (with their whole unrefereed subtrees) from refereed seeds only.
cd "$(dirname "$0")"
export CELLDIR=$PWD/cells ENGINELOG=$PWD/engine.log WORKDIR=$PWD/work PROGRESS=$PWD/progress.jsonl NPROC=1 MD=10
date -u +START\ %FT%TZ
timeout 9000 nice -n 10 python3 run_cells.py 17,15,7,3 21,19,9,3
echo "EXIT $?"
date -u +END\ %FT%TZ
