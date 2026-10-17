#!/bin/bash
# Referee L012 round 3 -- every computation of the report results/reviews/L012-n23-record-no-degree-4__referee__20261017T171553Z.md
# (run from this directory; about 1 CPU-hour; large files in out/, logs in logs/, binaries in bin/; all three git-ignored).
set -e
cd /home/user/Erdos-757/experiments/referee/L012-round3
P=/home/user/Erdos-757/experiments/prover/L012; F=/home/user/Erdos-757/experiments/20261017-1030-n23-record-cell
ND=/home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; NB=/home/user/Erdos-757/experiments/referee/L010-round1/out/nauty_build
mkdir -p bin out logs
gcc -O2 -Wall -o bin/bareal src/bareal.c; gcc -O2 -Wall -o bin/xext src/xext.c; gcc -O2 -Wall -o bin/chk src/chk.c; gcc -O2 -Wall -o bin/gcells src/gcells.c
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -I$NB -I$ND -o bin/genbg $ND/genbg.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
tar xzf $P/cells.tar.gz -C out; zcat $P/route4_classes.txt.gz > out/r4_699.txt
# 1. arithmetic, decompositions, all 36 engine branches, Remark 5
python3 src/arith.py out/cells > logs/arith.txt
# 3. realization: controls and the 699 classes (two halves)
echo "FOUND: (0,1,2) (0,3,4) (0,5,6) (1,3,5) (2,4,6)" > out/f7.txt; ./bin/bareal 7 print < out/f7.txt
./bin/bareal 14 print < $P/abase_pattern.txt > out/abase_real.txt; tail -1 out/abase_real.txt     # 948 realizations; Fractions re-check in the report's inline script
head -350 out/r4_699.txt > out/r4_a.txt; tail -n +351 out/r4_699.txt > out/r4_b.txt
./bin/bareal 23 < out/r4_a.txt > out/bareal_699_a.txt & ./bin/bareal 23 < out/r4_b.txt > out/bareal_699_b.txt; wait
python3 src/census14_control.py /home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz ./bin/bareal > logs/census14_control.txt
# 2, 4, 5. inputs, route 4, route 20
python3 src/build_inputs.py 4 out/cells > out/my_r4_inputs.txt; python3 src/build_inputs.py 20 out/cells > out/my_r20_inputs.txt
./bin/xext 22 10 4 3 < out/my_r4_inputs.txt > out/xext_r4.txt; tail -1 out/xext_r4.txt
python3 src/analyze_ext.py out/xext_r4.txt 23 out/r4_699.txt out/my_r4_survivors.txt > logs/analyze_r4.txt
./bin/xext 22 10 3 2 < out/my_r20_inputs.txt > out/xext_r20.txt; tail -1 out/xext_r20.txt
# validation of xext against a Python brute force (small cases; see logs/validate_xext.txt for the case list)
# 6. direct cells (genbg + gcells); the small route cells and the lower direct cells
for c in "8 5 3" "10 7 4" "12 10 5"; do set -- $c; for D in 3 4; do ./bin/genbg -q -c -Z1 -d1:3 -D$D:3 $1 $2 $((3*$2)):$((3*$2)) | ./bin/gcells $1 $2 $3 $D > out/g_$1_$2_$3_D$D.txt; tail -1 out/g_$1_$2_$3_D$D.txt; done; done
touch logs/closure.done; ./src/direct_cells.sh; cat logs/direct_cells.txt
# 7. isomorphism: BLISS convention test, classes, nauty relabelling invariance
python3 src/iso_check.py classes out/r4_699.txt 23 > logs/iso_classes_699.txt; python3 src/iso_check.py relabel out/r4_699.txt 23 $P/bin/canon > logs/relabel_699.txt
# 8. top recursion level of (22,17,9,4) and (19,16,8,4)
for b in "22 17 9 4 3" "22 17 9 4 4" "19 16 8 4 3" "19 16 8 4 4"; do set -- $b; python3 src/build_branch_inputs.py $1 $2 $3 $4 $5 out/cells 2>logs/br_$1_$2_$3_D$4_d$5.txt | grep -E '^[0-9]+( [0-9]+)+$' > out/br_$1_$2_$3_D$4_d$5.txt; done
./bin/xext 21 9 4 3 < out/br_22_17_9_D4_d4.txt > out/xbr_22_17_9_D4_d4.txt; ./bin/xext 21 9 3 2 < out/br_22_17_9_D4_d3.txt > out/xbr_22_17_9_D4_d3_par.txt
./bin/xext 18 8 4 3 < out/br_19_16_8_D4_d4.txt > out/xbr_19_16_8_D4_d4.txt; ./bin/xext 18 8 3 2 < out/br_19_16_8_D4_d3.txt > out/xbr_19_16_8_D4_d3.txt
for b in xbr_22_17_9_D4_d4 xbr_22_17_9_D4_d3_par; do python3 src/analyze_ext.py out/$b.txt 22 out/cells/cell_22_17_9_D4.txt out/${b}_conn.txt; done
cat out/xbr_22_17_9_D4_d4_conn.txt out/xbr_22_17_9_D4_d3_par_conn.txt > out/cell_22_17_9_D4_mine.txt; python3 src/iso_check.py match out/cells/cell_22_17_9_D4.txt out/cell_22_17_9_D4_mine.txt 22
for b in xbr_19_16_8_D4_d4 xbr_19_16_8_D4_d3; do python3 src/analyze_ext.py out/$b.txt 19 out/cells/cell_19_16_8_D4.txt out/${b}_conn.txt; done
cat out/xbr_19_16_8_D4_d4_conn.txt out/xbr_19_16_8_D4_d3_conn.txt > out/cell_19_16_8_D4_mine.txt; python3 src/iso_check.py match out/cells/cell_19_16_8_D4.txt out/cell_19_16_8_D4_mine.txt 19
# 9, 10, 11. closure of the 699, falsifier raw hits, properties of the 699
python3 src/closure.py out/r4_699.txt out/cells > logs/closure_699.txt; ./bin/chk 23 9 < out/closure_Hv.txt | tail -1
zcat $F/out/hits_final_route4_a.txt.gz $F/out/hits_final_route4_b.txt.gz | grep '^HIT' > out/falsifier_hits.txt; python3 src/iso_check.py match out/r4_699.txt out/falsifier_hits.txt 23
./bin/chk 23 10 < out/r4_699.txt > out/chk_699.txt; tail -1 out/chk_699.txt
