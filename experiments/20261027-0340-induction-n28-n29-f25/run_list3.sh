#!/bin/bash
# usage: run_list.sh LOGTAG key1 key2 ...   (each key = n,m,t,D; sequential; per-cell timeout 3 h; a failing/missing-deps cell is logged and skipped)
cd "$(dirname "$0")"
TAG=$1; shift
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log WORKDIR=$PWD/out/work PROGRESS_TSV=$PWD/progress.tsv NPROC=${NPROC:-2} MD=10 SORTMEM=${SORTMEM:-400M}
for k in "$@"; do
  # reuse files that appeared meanwhile (concurrent d4 worker)
  flock out/seed.lock python3 seed.py >> out/seed.log 2>&1
  df -h . | tail -1 | awk '{print $4}' | sed 's/G//' | awk '{ if ($1+0 < 1.2) exit 1 }' || { echo "DISK LOW, stopping before $k" | tee -a out/run_$TAG.log; exit 9; }
  echo "$(date -u +%FT%TZ) START $k" >> out/run_$TAG.log
  nice -n 5 timeout ${CELL_TIMEOUT:-10800} python3 src/run1.py $k >> out/run_$TAG.log 2>&1
  rc=$?
  echo "$(date -u +%FT%TZ) END $k rc=$rc" >> out/run_$TAG.log
  if [ $rc -ne 0 ] && [ $rc -ne 3 ]; then printf '(%s)\tFAILED rc=%s (3=missing deps, 124=timeout 3h)\t\t\t\t\n' "$k" "$rc" >> progress.tsv; fi
done
