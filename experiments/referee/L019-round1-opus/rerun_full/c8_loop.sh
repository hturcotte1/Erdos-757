#!/bin/bash
set -e
D=/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs
# C8: local cover number of the closed neighbourhood of v for the uncoverable linear triples (Remark 10.3)
for c in 17_13_7 15_11_6 22_17_9 26_22_11; do
  timeout 1800 nice -n 10 python3 nbhd_cover.py $D/cell_$c.txt 100000                 >> nbhd_cover_output.txt
done
