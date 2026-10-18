#!/bin/bash
# (L014) replacement of sched_main2.sh from 23:02 UTC (scheduling only): G = (19,17,8,3) needs (15,13,6,3) and (18,14,7,3) but not
# (21,15,8,3), so it starts as soon as C is complete; F = (22,18,9,3) starts when D2 = (21,15,8,3) (still running, started by
# sched_main2.sh in its own session) is complete; T = (23,21,10,3) when F and G are complete.  Each job in its own session.
cd /home/user/Erdos-757/experiments/prover/L014
export CELLDIR=$PWD/out/cells MD=10 PROGRESS=$PWD/out/progress.jsonl
done_cell() { grep -q '^INFO ' out/cells/cell_$1.txt 2>/dev/null; }
( until done_cell 15_13_6_D3 && done_cell 18_14_7_D3; do sleep 10; done
  echo "G start $(date -u +%FT%TZ)"
  ENGINELOG=$PWD/out/engine_G.log WORKDIR=$PWD/out/workG NPROC=1 setsid -w nice -n 5 timeout 9000 python3 run_cells.py 19,17,8,3 > out/logs/G.log 2>&1; echo "G rc=$? $(date -u +%FT%TZ)" ) &
( until done_cell 15_13_6_D3 && done_cell 18_14_7_D3 && done_cell 21_15_8_D3; do sleep 10; done
  echo "F start $(date -u +%FT%TZ)"
  ENGINELOG=$PWD/out/engine_F.log WORKDIR=$PWD/out/workF NPROC=2 setsid -w nice -n 5 timeout 9000 python3 run_cells.py 22,18,9,3 > out/logs/F.log 2>&1; echo "F rc=$? $(date -u +%FT%TZ)" ) &
until done_cell 22_18_9_D3 && done_cell 19_17_8_D3; do sleep 10; done
echo "phase 4 start $(date -u +%FT%TZ)"
ENGINELOG=$PWD/out/engine_T.log WORKDIR=$PWD/out/workT NPROC=2 setsid -w nice -n 5 timeout 5400 python3 run_cells.py 23,21,10,3 > out/logs/T.log 2>&1; echo "T rc=$? $(date -u +%FT%TZ)"
echo "main run end $(date -u +%FT%TZ)"
