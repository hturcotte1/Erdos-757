#!/bin/bash
# runs rich on every collected cell (1 process); output outputs/cell_<n>_<m>_<tau>.jsonl
cd "$(dirname "$0")"; mkdir -p outputs
for f in $(ls inputs/cell_*.txt | sort -t_ -k2,2n -k3,3n); do
  b=$(basename $f .txt)
  nice -n 10 timeout 3000 ./rich < $f > outputs/$b.jsonl.tmp && mv outputs/$b.jsonl.tmp outputs/$b.jsonl
done
echo ALLDONE
