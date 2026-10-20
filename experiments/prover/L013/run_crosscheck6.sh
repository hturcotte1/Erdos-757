#!/bin/bash
# (L013) cross-check (b), batch 6: direct enumeration of the top-level Delta <= 3 cell (26,15,10,3), 22 min cap (time budget); nice 19.
cd "$(dirname "$0")"
M=$PWD/out/cells
for c in "26 15 10 3"; do
  nice -n 19 timeout 1320 python3 crosscheck_direct.py $M $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT (22 min cap) or error, no result\"}" >> crosscheck_direct.jsonl
done
