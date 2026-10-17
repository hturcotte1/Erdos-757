#!/bin/bash
# (L013) cross-check (b), batch 5: direct enumeration of the top-level Delta <= 3 cells (23,14,9,3) and (26,15,10,3), 60 min cap each; nice 19.
cd "$(dirname "$0")"
M=$PWD/out/cells
for c in "23 14 9 3" "26 15 10 3"; do
  nice -n 19 timeout 3600 python3 crosscheck_direct.py $M $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT (60 min cap) or error\"}" >> crosscheck_direct.jsonl
done
