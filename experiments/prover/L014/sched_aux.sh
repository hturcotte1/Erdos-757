#!/bin/bash
# (L014) auxiliary runs: (f) the Delta<=4 cells for the control cell(23,21,10,4) (all except the top cell), then the equivalence check of
# the streamed driver against the unmodified engine (equiv_check.py), then recursion-vs-direct cross-checks (crosscheck_direct.py and
# MD=9 recursions of m=10 cells).  Starts when phase B of the main run is complete.
cd /home/user/Erdos-757/experiments/prover/L014
M=$PWD/out/cells
done_cell() { grep -q '^INFO ' out/cells/cell_$1.txt 2>/dev/null; }
until done_cell 21_18_9_D3; do sleep 15; done
echo "E start $(date -u +%FT%TZ)"
CELLDIR=$M ENGINELOG=$PWD/out/engine_E.log WORKDIR=$PWD/out/workE PROGRESS=$PWD/out/progress.jsonl NPROC=1 MD=10 nice -n 5 timeout 5400 python3 run_cells.py $(cat out/listE.txt) > out/logs/E.log 2>&1; echo "E rc=$? $(date -u +%FT%TZ)"
nice -n 10 python3 equiv_check.py $M $PWD/out/equiv 3600 13,9,5,3 11,8,4,3 14,9,5,3 14,12,6,3 17,11,6,3 20,12,7,3 15,12,6,3 21,18,9,3 17,14,7,3 > equiv_check_output.txt 2>&1; echo "equiv rc=$? $(date -u +%FT%TZ)"
for c in 14,10,5,3 13,10,5,3 12,10,5,3; do
  k=$(echo $c | tr , _); rm -rf out/md9/$k; mkdir -p out/md9/$k/cells
  CELLDIR=$PWD/out/md9/$k/cells ENGINELOG=$PWD/out/md9/$k/engine.log WORKDIR=$PWD/out/md9/$k/work PROGRESS=$PWD/out/md9/$k/progress.jsonl NPROC=1 MD=9 nice -n 10 timeout 3600 python3 run_cells.py $c > out/md9/$k/run.log 2>&1
  echo "md9 $c rc=$? $(date -u +%FT%TZ)"
done
python3 compare_cells.py $M MD9_14_10_5=$PWD/out/md9/14_10_5_3/cells MD9_13_10_5=$PWD/out/md9/13_10_5_3/cells MD9_12_10_5=$PWD/out/md9/12_10_5_3/cells > md9_compare_output.txt
nice -n 10 python3 crosscheck_direct.py $M $PWD/out/direct 1800 14,12,6,3 15,11,6,3 17,13,7,3 16,11,6,3 18,12,7,3 19,12,7,3 17,11,6,3 20,12,7,3 > crosscheck_direct_output.txt 2>&1; echo "direct rc=$? $(date -u +%FT%TZ)"
echo "aux end $(date -u +%FT%TZ)"
