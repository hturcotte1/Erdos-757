#!/bin/bash
# (L014) scheduler of the main run (phases 2 and 3): starts each group of cells as soon as its prerequisites are complete cell files.
# Phase 1 (started by hand, see reproduce.sh): A = cell(14,10,5,3); B = the 97 cells of the tree that do not need (14,10,5,3).
cd /home/user/Erdos-757/experiments/prover/L014
export CELLDIR=$PWD/out/cells MD=10 PROGRESS=$PWD/out/progress.jsonl
done_cell() { grep -q '^INFO ' out/cells/cell_$1.txt 2>/dev/null; }
until done_cell 14_10_5_D3 && done_cell 21_18_9_D3 && done_cell 17_14_7_D3; do sleep 15; done
echo "phase 2 start $(date -u +%FT%TZ)"
(ENGINELOG=$PWD/out/engine_C.log WORKDIR=$PWD/out/workC NPROC=1 nice -n 5 timeout 9000 python3 run_cells.py 15,13,6,3 18,14,7,3 > out/logs/C.log 2>&1; echo "C rc=$?") &
(ENGINELOG=$PWD/out/engine_D.log WORKDIR=$PWD/out/workD NPROC=1 nice -n 5 timeout 9000 python3 run_cells.py 21,15,8,3 > out/logs/D.log 2>&1; echo "D rc=$?") &
wait
echo "phase 3 start $(date -u +%FT%TZ)"
(ENGINELOG=$PWD/out/engine_F.log WORKDIR=$PWD/out/workF NPROC=2 nice -n 5 timeout 9000 python3 run_cells.py 22,18,9,3 > out/logs/F.log 2>&1; echo "F rc=$?") &
(ENGINELOG=$PWD/out/engine_G.log WORKDIR=$PWD/out/workG NPROC=1 nice -n 5 timeout 9000 python3 run_cells.py 19,17,8,3 > out/logs/G.log 2>&1; echo "G rc=$?") &
wait
echo "phase 4 start $(date -u +%FT%TZ)"
ENGINELOG=$PWD/out/engine_T.log WORKDIR=$PWD/out/workT NPROC=2 nice -n 5 timeout 5400 python3 run_cells.py 23,21,10,3 > out/logs/T.log 2>&1; echo "T rc=$?"
echo "main run end $(date -u +%FT%TZ)"
