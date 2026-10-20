#!/bin/bash
# (L013) positive controls by random members of C in recursion cells (seeded; see positive_control.py), nice 19, 15 min cap each.
cd "$(dirname "$0")"
for c in "16 11 6 3 300 150000 11" "15 12 6 3 300 150000 12" "18 13 7 3 200 200000 13"; do   # (three further cells were planned and dropped: time budget)
  nice -n 19 timeout 900 python3 positive_control.py out/cells $c || echo "{\"cell\": \"$c\", \"status\": \"TIMEOUT_OR_ERROR\"}" >> positive_control.jsonl
done
