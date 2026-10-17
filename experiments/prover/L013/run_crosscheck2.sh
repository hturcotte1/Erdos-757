#!/bin/bash
# (L013) cross-check (b), batch 2: direct enumeration of further recursion cells with n >= 22 (one of them the top-level cell (24,12,9,2)),
# one at a time, nice 19; each waits for the main run's file before comparing.
cd "$(dirname "$0")"
M=$PWD/out/cells
for c in "24 12 9 2" "22 13 8 2" "23 12 8 2" "24 14 9 2"; do   # (the other cells of the original batch moved to run_crosscheck2b.sh)
  nice -n 19 timeout 2700 python3 crosscheck_direct.py $M $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT_OR_ERROR\"}" >> crosscheck_direct.jsonl
done
