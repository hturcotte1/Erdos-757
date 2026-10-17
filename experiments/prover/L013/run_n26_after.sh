#!/bin/bash
# (L013) Wait until the n <= 25 driver has finished (its last top cell (25,22,11,3) is in top_results.jsonl), then run the n = 26 top cells
# in the same cell directory (sub-cells computed by the n <= 25 run are loaded from disk; nothing from any other directory is used).
cd "$(dirname "$0")"
while ! grep -q '"cell": \[25, 22, 11, 3\]' top_results.jsonl 2>/dev/null; do sleep 20; done
CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log NPROC=2 MD=10 TOPJSONL=$PWD/top_results.jsonl \
  nice -n 19 timeout 7200 python3 run_top.py 26 14 10 2 26 15 10 3 26 21 11 3 > out/run_top_n26.log 2>&1
