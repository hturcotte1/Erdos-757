#!/bin/bash
# Exact commands for experiments/20261017-1645-i11-n23-n24 (run from this directory; about 25 CPU-minutes of engine time at NPROC=3).
# bin -> ../prover/L012/bin (compiled binaries; rebuild per ../prover/L012/reproduce.sh if missing).
set -e
cd "$(dirname "$0")"; mkdir -p out
[ -e bin ] || ln -s ../prover/L012/bin bin
python3 arith.py > arith_output.txt                     # step 1 (n = 23, 24, 25) -> arith_output.txt, arith_results.json
python3 compare_arith23.py                              # acceptance: n=23 lines agree with ../prover/L012/arith23_output.txt for m=19,20,21
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log NPROC=3
timeout 2400 python3 run_cells.py 23 13 9 2 23 14 9 3 > out/run_n23_a.log 2>&1      # step 2 (3.6 s)
timeout 2400 python3 run_cells.py 23 20 10 3 > out/run_n23_b.log 2>&1               # step 2, recomputation of L012 Step 4 (330 s)
timeout 2400 python3 run_cells.py 24 12 9 2 24 13 9 3 24 18 10 3 > out/run_n24.log 2>&1   # step 3 (4 s; reuses the cell files of step 2)
python3 step4_n25_cells.py > step4_n25_output.txt       # step 4: arithmetic + cell lists for n = 25
python3 collect.py                                      # cells_table.tsv from out/cells
# bonus (not requested): the three open n = 25 cells computed with the engine, copy of out/cells, 40 min cap each (about 21 min total)
cp -r out/cells out/cells25; bash run_n25_bonus.sh
# step 5: cross-checks (direct enumeration, MD=15, versus the cells built by recursion with MD=10)
nice timeout 3000 python3 crosscheck.py 20 11 7 2 17 11 6 2 21 11 7 2 19 12 7 2 20 12 7 2 > out/crosscheck_b.log 2>&1
nice timeout 1500 python3 crosscheck.py 20 11 7 3 > out/crosscheck_c.log 2>&1
python3 make_results.py                                 # results.json
