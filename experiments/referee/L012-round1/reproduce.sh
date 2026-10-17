#!/bin/bash
# Referee L012 round 1 -- every computation of the review (run from this directory; ~1 CPU-hour; large files in out/, logs in logs/).
set -e
cd /home/user/Erdos-757/experiments/referee/L012-round1
ND=/home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; NB=/home/user/Erdos-757/experiments/referee/L010-round1/out/nauty_build
P=/home/user/Erdos-757/experiments/prover/L012
mkdir -p out/bin logs
gcc -O2 -Wall -o out/bin/rreal src/rreal.c -lm; gcc -O2 -Wall -o out/bin/rreal_extra src/rreal_extra.c -lm
gcc -O2 -w -o out/bin/rext src/rext.c; gcc -O2 -w -o out/bin/rfilt src/rfilt.c; gcc -O2 -w -o out/bin/gfilt src/gfilt.c
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -I$NB -I$ND -o out/bin/genbg $ND/genbg.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -DPRUNE1=mprune1 -DPRUNE2=mprune2 -DOUTPROC=mout -DSUMMARY=msum -I$NB -I$ND -o out/bin/mgenbg $ND/genbg.c src/myhooks.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
# arithmetic, decompositions (Steps 0.3, 1, 2, 4.2, all 36 engine branches), Remark 5, degree statistics, Step 8 counts
python3 src/arith_decomp.py; python3 src/misc_checks.py
# exact realization (independent): A_base control, n=12 and n=14 census controls, the 699 classes, per-class comparison
zcat $P/route4_classes.txt.gz > out/r4_699.txt
python3 src/abase_control.py
python3 src/census12_control.py /home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz $P/out/cells/cell_12_10_5_D4.txt
python3 src/census14_control.py
./out/bin/rreal 23 < out/r4_699.txt > out/rreal_699.txt; tail -1 out/rreal_699.txt
./out/bin/rreal_extra 23 < out/r4_699.txt > out/rreal_extra_699.txt
# route 4 and route 20 with the referee's own extension enumerator, filter and VF2 classes
python3 src/build_inputs.py 4 > out/r4_inputs.txt; python3 src/build_inputs.py 20 > out/r20_inputs.txt
python3 src/bf_rext.py
head -1089 out/r4_inputs.txt > out/r4_in_a.txt; tail -n +1090 out/r4_inputs.txt > out/r4_in_b.txt
./out/bin/rext 22 4 3 < out/r4_in_a.txt > out/rext_r4_a.txt; ./out/bin/rext 22 4 3 < out/r4_in_b.txt > out/rext_r4_b.txt
./out/bin/rfilt 22 out/r4_in_a.txt < out/rext_r4_a.txt > out/rfilt_r4_a.txt; ./out/bin/rfilt 22 out/r4_in_b.txt < out/rext_r4_b.txt > out/rfilt_r4_b.txt
cat out/rfilt_r4_a.txt out/rfilt_r4_b.txt | grep '^S:' > out/r4_survivors.txt; python3 src/iso_match.py out/r4_699.txt out/r4_survivors.txt 23
./out/bin/rext 22 3 2 < out/r20_inputs.txt > out/rext_r20.txt; ./out/bin/rfilt 22 out/r20_inputs.txt < out/rext_r20.txt > out/rfilt_r20.txt; tail -1 out/rfilt_r20.txt
# cell lists: direct genbg enumerations, top-level recomputations, closure test, D3 = (D4 restricted to Delta<=3)
for c in "8 5 3 4" "10 7 4 4" "12 10 5 4" "12 10 5 3" "8 5 3 3" "10 7 4 3" "13 9 5 3" "10 8 4 3"; do set -- $c; ./out/bin/genbg -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) | ./out/bin/gfilt $1 $2 $3 $4 > out/g_$1_$2_$3_D$4.txt; done
./src/mgenbg_cells.sh 500 "14 12 6 3" "14 12 6 4" "15 11 6 3" "15 11 6 4" "17 13 7 3" "17 11 6 2" "19 12 7 2" "20 12 7 2" "20 11 7 2" "20 11 7 3" "15 12 6 3"
for c in 22,17,9,4 19,16,8,4 22,17,9,3 19,16,8,3 17,13,7,3 21,14,8,3 18,13,7,3 15,12,6,3 21,13,8,4 18,12,7,4 20,14,8,3 19,11,7,3 20,12,7,2 17,11,6,2 20,11,7,3 14,12,6,4 15,11,6,4; do python3 src/recompute_cell.py $c; done
for c in route4 22,17,9,4 19,16,8,4 22,17,9,3 19,16,8,3 14,12,6,4 15,11,6,4 21,14,8,3 18,13,7,3 19,12,7,2 20,11,7,2 14,12,6,3 17,13,7,3 15,11,6,3 20,12,7,2 20,11,7,3 17,11,6,2 15,12,6,3; do python3 src/closure_check.py $c out/r4_699.txt; done
python3 src/d3_subset.py
