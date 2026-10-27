#!/bin/bash
# Referee L023 round 1: ONE engine step, cell(21,19,9,3), from: refereed seeds, my own recomputation of cell(17,15,7,3) (from refereed
# seeds only, ../engine_run), and (U1)'s UNREFEREED cell(20,16,8,3) (copied; not reproduced by this referee).
cd "$(dirname "$0")"
export CELLDIR=$PWD/cells ENGINELOG=$PWD/engine.log WORKDIR=$PWD/work PROGRESS=$PWD/progress.jsonl NPROC=1 MD=10
cp ../engine_run/cells/cell_17_15_7_D3.txt cells/
cp /home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/out/cells/cell_20_16_8_D3.txt cells/
sha256sum cells/cell_17_15_7_D3.txt cells/cell_20_16_8_D3.txt
date -u +START\ %FT%TZ
timeout 7000 nice -n 10 python3 run_cells.py 21,19,9,3
echo "EXIT $?"
date -u +END\ %FT%TZ
