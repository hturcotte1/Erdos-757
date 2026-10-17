#!/bin/bash
# (L013) cross-check (b), batch 1: direct enumeration of recursion cells, one at a time, nice 19, 30 min cap each.
cd "$(dirname "$0")"
M=$PWD/out/cells
for c in "22 11 8 3" "22 12 8 2" "23 13 9 2" "17 11 6 2" "20 11 7 3" "20 12 7 2" "21 11 7 2"; do
  nice -n 19 timeout 1800 python3 crosscheck_direct.py $M $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT_OR_ERROR\"}" >> crosscheck_direct.jsonl
done
