#!/bin/bash
# Referee L023 round 1: (1) recompute the unrefereed degree-4 subtree lists cell(21,18,9,4), cell(24,19,10,4) from refereed seeds only;
# (2) then the top level cell(25,23,11,4) and cell(25,23,11,3) with: my D=4 lists, refereed lists, and (U1)'s lists
#     cell(24,20,10,3), cell(21,19,9,3) (copied, UNREFEREED; the second is compared separately with my own recomputation).
cd "$(dirname "$0")"
export CELLDIR=$PWD/cells ENGINELOG=$PWD/engine.log WORKDIR=$PWD/work PROGRESS=$PWD/progress.jsonl NPROC=1 MD=10
date -u +START\ %FT%TZ
timeout 3000 nice -n 10 python3 run_cells.py 21,18,9,4 24,19,10,4
echo "EXIT1 $?"
cp /home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells/cell_24_20_10_D3.txt /home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells/cell_21_19_9_D3.txt cells/
sha256sum cells/cell_24_20_10_D3.txt cells/cell_21_19_9_D3.txt
timeout 3000 nice -n 10 python3 run_cells.py 25,23,11,4 25,23,11,3
echo "EXIT2 $?"
date -u +END\ %FT%TZ
