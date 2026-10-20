#!/bin/bash
# (L013) positive controls, batch 2 (larger recursion cells), nice 19, 8 min cap each.
cd "$(dirname "$0")"
for c in "17 14 7 3 200 400000 21" "20 15 8 3 100 400000 22" "21 14 8 3 100 400000 23"; do
  nice -n 19 timeout 480 python3 positive_control.py out/cells $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT (8 min cap) or error\"}" >> positive_control.jsonl
done
