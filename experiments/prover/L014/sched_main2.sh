#!/bin/bash
# (L014) replacement of sched_main.sh from phase 2 on (22:31 UTC): the kernel groups CPU time by session (sched_autogroup), so the two
# phase-2 jobs of sched_main.sh shared one CPU share; D = (21,15,8,3) was stopped (no cell file had been written) and is re-run here
# from scratch in its own session; C = (15,13,6,3), (18,14,7,3) (started by sched_main.sh) continues unchanged.  Each job runs in its
# own session (setsid -w).  The cell lists do not depend on this scheduling (each list depends only on its key and its component lists).
cd /home/user/Erdos-757/experiments/prover/L014
export CELLDIR=$PWD/out/cells MD=10 PROGRESS=$PWD/out/progress.jsonl
done_cell() { grep -q '^INFO ' out/cells/cell_$1.txt 2>/dev/null; }
echo "phase 2b start (D re-run) $(date -u +%FT%TZ)"
(ENGINELOG=$PWD/out/engine_D2.log WORKDIR=$PWD/out/workD2 NPROC=1 setsid -w nice -n 5 timeout 9000 python3 run_cells.py 21,15,8,3 > out/logs/D2.log 2>&1; echo "D2 rc=$? $(date -u +%FT%TZ)") &
until done_cell 15_13_6_D3 && done_cell 18_14_7_D3 && done_cell 21_15_8_D3; do sleep 15; done
echo "phase 3 start $(date -u +%FT%TZ)"
(ENGINELOG=$PWD/out/engine_F.log WORKDIR=$PWD/out/workF NPROC=2 setsid -w nice -n 5 timeout 9000 python3 run_cells.py 22,18,9,3 > out/logs/F.log 2>&1; echo "F rc=$? $(date -u +%FT%TZ)") &
(ENGINELOG=$PWD/out/engine_G.log WORKDIR=$PWD/out/workG NPROC=1 setsid -w nice -n 5 timeout 9000 python3 run_cells.py 19,17,8,3 > out/logs/G.log 2>&1; echo "G rc=$? $(date -u +%FT%TZ)") &
until done_cell 22_18_9_D3 && done_cell 19_17_8_D3; do sleep 15; done
echo "phase 4 start $(date -u +%FT%TZ)"
ENGINELOG=$PWD/out/engine_T.log WORKDIR=$PWD/out/workT NPROC=2 setsid -w nice -n 5 timeout 5400 python3 run_cells.py 23,21,10,3 > out/logs/T.log 2>&1; echo "T rc=$? $(date -u +%FT%TZ)"
echo "main run end $(date -u +%FT%TZ)"
