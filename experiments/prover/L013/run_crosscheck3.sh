#!/bin/bash
# (L013) cross-check (b), batch 3: direct enumeration of the non-empty recursion cells with n >= 22 that are cheap enough
# ((22,11,7,2): 52 classes, (23,13,8,2): 12 classes) and, with a cap, (22,13,8,3): 85 classes; nice 19.
cd "$(dirname "$0")"
M=$PWD/out/cells
for c in "22 11 7 2" "23 13 8 2"; do   # (22,13,8,3) was started and stopped after about 1 minute (time budget)
  nice -n 19 timeout 2700 python3 crosscheck_direct.py $M $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT_OR_ERROR\"}" >> crosscheck_direct.jsonl
done
