#!/bin/bash
# (L013) cross-check (b), batch 2b (the rest of batch 2, run in parallel with batch 3): the top-level Delta <= 2 cells (25,16,10,2),
# (26,14,10,2) and, capped, the top-level Delta <= 3 cell (24,13,9,3); nice 19.
cd "$(dirname "$0")"
M=$PWD/out/cells
for c in "25 16 10 2"; do   # (26,14,10,2) and (24,13,9,3) were moved to run_crosscheck2c.sh
  nice -n 19 timeout 2700 python3 crosscheck_direct.py $M $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT_OR_ERROR\"}" >> crosscheck_direct.jsonl
done
