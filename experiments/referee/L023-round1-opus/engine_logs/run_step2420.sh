#!/bin/bash
# Referee L023 round 1: ONE engine step, cell(24,20,10,3), from: refereed seeds, my own recomputation of cell(17,15,7,3) (from refereed
# seeds only), and (U1)'s UNREFEREED cell(20,16,8,3) and cell(23,17,9,3) (copied; not reproduced by this referee).
cd "$(dirname "$0")"
export CELLDIR=$PWD/cells ENGINELOG=$PWD/engine.log WORKDIR=$PWD/work PROGRESS=$PWD/progress.jsonl NPROC=1 MD=10
cp ../engine_run/cells/cell_17_15_7_D3.txt cells/
U1=/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells
cp $U1/cell_20_16_8_D3.txt $U1/cell_23_17_9_D3.txt cells/
sha256sum cells/cell_17_15_7_D3.txt cells/cell_20_16_8_D3.txt cells/cell_23_17_9_D3.txt
date -u +START\ %FT%TZ
timeout 6000 nice -n 10 python3 run_cells.py 24,20,10,3
echo "EXIT $?"
date -u +END\ %FT%TZ
