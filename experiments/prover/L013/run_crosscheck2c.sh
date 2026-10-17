#!/bin/bash
# (L013) cross-check (b), batch 2c (moved from batch 2b to run in parallel): the top-level cells (26,14,10,2) and, capped, (24,13,9,3); nice 19.
cd "$(dirname "$0")"
M=$PWD/out/cells
for c in "26 14 10 2" "24 13 9 3"; do
  nice -n 19 timeout 2700 python3 crosscheck_direct.py $M $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT_OR_ERROR\"}" >> crosscheck_direct.jsonl
done
