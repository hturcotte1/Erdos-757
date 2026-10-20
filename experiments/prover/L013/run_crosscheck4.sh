#!/bin/bash
# (L013) cross-check (b), batch 4: direct enumeration of the load-bearing recursion cells that were corroborated only by the recursion
# (load_bearing.py): the Delta <= 2 cells (22,11,8,2), (23,11,8,2), (25,12,9,2), (25,13,9,2), then (25,12,9,3) and, capped, (24,14,9,3); nice 19.
cd "$(dirname "$0")"
M=$PWD/out/cells
for c in "22 11 8 2" "23 11 8 2" "25 12 9 2" "25 13 9 2" "25 12 9 3" "24 14 9 3"; do
  nice -n 19 timeout 2400 python3 crosscheck_direct.py $M $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT_OR_ERROR\"}" >> crosscheck_direct.jsonl
done
