#!/bin/bash
# Referee L013 round 3: every computation of results/reviews/L013-i11-on-C-n-le-26__referee__<UTC>.md (run from this directory; ~1.5 CPU-hours)
set -e; cd "$(dirname "$0")"; P=/home/user/Erdos-757/experiments/prover/L013/out/cells
ND=/home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; NB=/home/user/Erdos-757/experiments/referee/L010-round1/out/nauty_build
mkdir -p bin out logs
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -I$NB -I$ND -o bin/genbg $ND/genbg.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -DMAXN1=30 -I$NB -I$ND -o bin/genbg30 $ND/genbg.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O2 -w -o bin/unit_tests src/unit_tests.c; gcc -O2 -w -o bin/verify_cells src/verify_cells.c; gcc -O2 -w -o bin/gfilt src/gfilt.c; gcc -O2 -w -o bin/xext_ref src/xext_ref.c; gcc -O2 -w -o bin/xext_ref2 src/xext_ref2.c
python3 src/arith_ref.py > logs/arith_ref.txt                      # R1
python3 src/decomp_ref.py $P > logs/decomp_ref.txt                   # R2
./bin/unit_tests > logs/unit_tests.txt || true                       # R3 (1 expected self-test misexpectation, see review)
for f in $P/cell_*.txt; do b=$(basename $f .txt); set -- $(echo $b | sed 's/cell_//; s/_D/ /; s/_/ /g'); ./bin/verify_cells $1 $2 $3 $4 < $f; done > logs/verify_cells.txt
./src/run_genbg_A.sh > logs/genbg_A.txt; ./src/run_genbg_B.sh > logs/genbg_B.txt; ./src/run_genbg_C.sh > logs/genbg_C.txt; ./src/run_genbg_D.sh > logs/genbg_D.txt; ./src/run_genbg_E.sh > logs/genbg_E.txt   # R4
for c in "26 14 10 2" "25 12 9 2" "25 13 9 2"; do set -- $c; ./bin/genbg30 -c -Z1 -d1:3 -D$4:3 -q $1 $2 $((3*$2)):$((3*$2)) | ./bin/gfilt $1 $2 $3 $4 > out/g30_$1_$2_$3_D$4.txt; done
python3 src/isocompare.py 22 out/g_22_11_7_D2.txt $P/cell_22_11_7_D2.txt; python3 src/isocompare.py 23 out/g_23_13_8_D2.txt $P/cell_23_13_8_D2.txt
./src/run_ext_top.sh > logs/ext_top.txt; ./src/run_ext_sub.sh > logs/ext_sub.txt                          # R5
python3 src/run_all_new_rec.py > logs/all_new_rec.txt; ./src/run_conn_all.sh > logs/conn_all.txt            # R6
