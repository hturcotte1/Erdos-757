#!/bin/bash
# usage: run_cells.sh TAG key1 key2 ...  (one cell per process; nice -n 15; timeout 3h per cell)
cd "$(dirname "$0")"
TAG=$1; shift
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine_$TAG.log WORKDIR=$PWD/out/work_$TAG PROGRESS_TSV=$PWD/progress_raw_$TAG.tsv NPROC=1 MD=10 SORTMEM=400M
mkdir -p $WORKDIR
for k in "$@"; do
  echo "$(date -u +%FT%TZ) START $k" >> out/run_$TAG.log
  nice -n 15 timeout 10800 python3 src/run1.py $k >> out/run_$TAG.log 2>&1
  echo "$(date -u +%FT%TZ) END $k rc=$?" >> out/run_$TAG.log
done
