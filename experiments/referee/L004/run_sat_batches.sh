#!/usr/bin/env bash
# Referee L004: sequential, resumable SAT batches (one process at a time, niced). Usage: run_sat_batches.sh LIST CHUNK OUTDIR
set -u
D=/home/user/Erdos-757/experiments/referee/L004
LIST=$1; CH=$2; OUT=$3
mkdir -p $OUT
split -l $CH -d -a 4 $D/$LIST $OUT/chunk_
for c in $OUT/chunk_????; do
  o=$c.sat.gz
  if [ -f $o ] && zcat $o 2>/dev/null | grep -q '^# DONE'; then echo "skip $c"; continue; fi
  echo "start $c $(date -u +%H:%M:%S)"
  LAZYF7=1 nice -n 10 python3 $D/sat14.py 14 8 $o list:$c
done
echo "ALL DONE $(date -u +%H:%M:%S)"
