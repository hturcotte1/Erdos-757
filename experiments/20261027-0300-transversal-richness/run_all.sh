#!/bin/bash
# runs rich on every collected cell (1 process); output outputs/cell_<n>_<m>_<tau>.jsonl (skips finished cells); order: small n first, then 26_22_11, 23_16_9, 23_21_10 last (largest, least informative)
cd "$(dirname "$0")"; mkdir -p outputs
for b in $(ls inputs/cell_*.txt | xargs -n1 basename | sed 's/.txt//' | sort -t_ -k2,2n -k3,3n | grep -v -E 'cell_23_|cell_26_') cell_26_22_11 cell_23_16_9 cell_23_21_10; do
  [ -f outputs/$b.jsonl ] && continue
  nice -n 10 timeout 3000 ./rich < inputs/$b.txt > outputs/$b.jsonl.tmp && mv outputs/$b.jsonl.tmp outputs/$b.jsonl
done
echo ALLDONE
