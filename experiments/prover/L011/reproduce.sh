#!/bin/bash
# Reproduction of every computation cited in results/proofs/L011-f22-equals-13.md (run from this directory; about 1.5 CPU-hours for
# the main steps plus about 1.5 CPU-hours for the cross-checks).  Large files go to out/ (git-ignored).  Uses as inputs the prover's
# enumerations of L008 (mine_12_10_5_deg3, mine_15_11_6_deg3) and L009 (T14_conn, T17_conn); see those folders' reproduce.sh.
set -e
F=/home/user/Erdos-757/experiments/20261017-0825-n21-n22-via-i11
L8=/home/user/Erdos-757/experiments/prover/L008/indep; L9=/home/user/Erdos-757/experiments/prover/L009/indep
mkdir -p out bin
cd indep; gcc -O2 -Wall -o enum_conn enum_conn.c; gcc -O2 -Wall -o ext_indep5 ext_indep5.c; gcc -O2 -o filter_hits filter_hits.c; gcc -O2 -o filter_hits2 filter_hits2.c; cd ..
gcc -O2 -o bin/ext_vertex2 $F/ext_vertex2.c
# --- C1: arithmetic (window cells, slack cells, decompositions by two generators, record cells)
python3 decomp22.py > decomp22_output.txt
# --- C2: enumerations
bash indep/run_cells.sh small > indep/run_cells_small.log; bash indep/run_cells.sh long1 > indep/run_cells_long1.log; bash indep/run_cells.sh long2 > indep/run_cells_long2.log
for c in 6_3_2 8_5_3 8_6_3 9_4_3 10_7_4 10_8_4 11_7_4 13_8_5 13_9_5 14_8_5 16_10_6 19_11_7; do python3 compare_found.py out/cell_$c.txt -- $F/K_$c.txt | tail -n 1; done
zcat $L8/mine_12_10_5_deg3.txt.gz > out/cell_12_10_5.txt; zcat $L8/mine_15_11_6_deg3.txt.gz > out/cell_15_11_6.txt
python3 compare_found.py out/cell_12_10_5.txt -- $F/K_12_10_5.txt | tail -n 1
cp $L9/T14_conn.txt out/T14_conn.txt; zcat $L9/T17_conn.txt.gz > out/T17_conn.txt
# --- C3: components in C
for c in 6_3_2 8_5_3 8_6_3 9_4_3 10_7_4 10_8_4 11_7_4 13_8_5 13_9_5 14_8_5 16_10_6 19_11_7 12_10_5 15_11_6; do ./indep/filter_hits FOUND < out/cell_$c.txt > out/filt_$c.txt; tail -n 1 out/filt_$c.txt; done
for t in T14 T17; do ./indep/filter_hits FOUND < out/${t}_conn.txt > out/filt_$t.txt; tail -n 1 out/filt_$t.txt; done
# --- C4: (21,12,8) with a degree-3 vertex: type [AP^4,(8,5,3)]
python3 combine.py out/in21_12.txt AP AP AP AP out/filt_8_5_3.txt:SURVIVOR
./indep/ext_indep5 20 7 3 < out/in21_12.txt > out/hits21_12.txt; tail -n 1 out/hits21_12.txt; ./indep/filter_hits HIT < out/hits21_12.txt | tail -n 1
./bin/ext_vertex2 20 8 3 < out/in21_12.txt > out/hits21_12_ev2.txt; python3 compare_hits.py out/hits21_12_ev2.txt out/hits21_12.txt
# --- C5: no connected (20,14,8) in C with max degree 3 (rebuild from the 9 decompositions of (19,11) with slack 2; 3 of them empty)
python3 combine.py out/inX20_1.txt AP AP AP out/filt_10_8_4.txt:SURVIVOR; python3 combine.py out/inX20_2.txt AP AP out/filt_13_9_5.txt:SURVIVOR
python3 combine.py out/inX20_3.txt AP out/filt_6_3_2.txt:SURVIVOR out/filt_10_7_4.txt:SURVIVOR; python3 combine.py out/inX20_4.txt AP out/filt_8_5_3.txt:SURVIVOR out/filt_8_5_3.txt:SURVIVOR
python3 combine.py out/inX20_5.txt AP out/filt_16_10_6.txt:SURVIVOR; python3 combine.py out/inX20_8.txt out/filt_9_4_3.txt:SURVIVOR out/filt_10_7_4.txt:SURVIVOR
cat out/inX20_1.txt out/inX20_2.txt out/inX20_3.txt out/inX20_4.txt out/inX20_5.txt out/inX20_8.txt > out/inX20_all.txt
./indep/ext_indep5 19 7 3 < out/inX20_all.txt > out/hitsX20.txt; tail -n 1 out/hitsX20.txt
./indep/filter_hits2 HIT notau < out/hitsX20.txt > out/filtX20.txt; tail -n 1 out/filtX20.txt
python3 connected_filter2.py out/filtX20.txt out/X20_conn.txt 20; python3 connected_filter.py out/filtX20.txt out/X20_conn_old.txt
python3 connected_hits.py out/hitsX20.txt out/hitsX20_conn.txt 20; ./indep/filter_hits2 HIT notau < out/hitsX20_conn.txt | tail -n 1
# --- C6: final step for (21,17,9): types [AP,AP,T14], [AP,T17], [C10,C10]
python3 combine.py out/in21_17_a.txt AP AP out/filt_T14.txt:SURVIVOR; python3 combine.py out/in21_17_b.txt AP out/filt_T17.txt:SURVIVOR
python3 combine.py out/in21_17_c.txt out/filt_10_7_4.txt:SURVIVOR out/filt_10_7_4.txt:SURVIVOR
cat out/in21_17_a.txt out/in21_17_b.txt out/in21_17_c.txt > out/in21_17_all.txt
./indep/ext_indep5 20 8 3 < out/in21_17_all.txt > out/hits21_17.txt; tail -n 1 out/hits21_17.txt
./indep/filter_hits HIT < out/hits21_17.txt > out/filt21_17.txt; tail -n 1 out/filt21_17.txt; python3 hit_types.py out/hits21_17.txt 14 20
# --- C7: no connected (21,13,8) in C with max degree 3 (rebuild from the 14 decompositions of (20,10) with slack 3; 8 of them empty)
python3 combine.py out/inX21_1.txt ISO AP AP AP out/filt_10_7_4.txt:SURVIVOR; python3 combine.py out/inX21_5.txt AP AP AP AP out/filt_8_6_3.txt:SURVIVOR
python3 combine.py out/inX21_6.txt AP AP AP out/filt_11_7_4.txt:SURVIVOR; python3 combine.py out/inX21_7.txt AP AP out/filt_6_3_2.txt:SURVIVOR out/filt_8_5_3.txt:SURVIVOR
python3 combine.py out/inX21_8.txt AP AP out/filt_14_8_5.txt:SURVIVOR; python3 combine.py out/inX21_10.txt AP out/filt_8_5_3.txt:SURVIVOR out/filt_9_4_3.txt:SURVIVOR
cat out/inX21_1.txt out/inX21_5.txt out/inX21_6.txt out/inX21_7.txt out/inX21_8.txt out/inX21_10.txt > out/inX21_all.txt
./indep/ext_indep5 20 7 3 < out/inX21_all.txt > out/hitsX21.txt; tail -n 1 out/hitsX21.txt
./indep/filter_hits2 HIT notau < out/hitsX21.txt > out/filtX21.txt; tail -n 1 out/filtX21.txt
python3 connected_filter2.py out/filtX21.txt out/X21_conn.txt 21; python3 connected_hits.py out/hitsX21.txt out/hitsX21_conn.txt 21
# --- C8: final step for (22,16,9): types [AP^3,(12,10,5)], [AP^2,(15,11,6)], [AP,(8,5,3),(10,7,4)]
python3 combine.py out/in22_16_a.txt AP AP AP out/filt_12_10_5.txt:SURVIVOR; python3 combine.py out/in22_16_b.txt AP AP out/filt_15_11_6.txt:SURVIVOR
python3 combine.py out/in22_16_c.txt AP out/filt_8_5_3.txt:SURVIVOR out/filt_10_7_4.txt:SURVIVOR
cat out/in22_16_a.txt out/in22_16_b.txt out/in22_16_c.txt > out/in22_16_all.txt
./indep/ext_indep5 21 8 3 < out/in22_16_all.txt > out/hits22_16.txt; tail -n 1 out/hits22_16.txt
./indep/filter_hits2 HIT notau < out/hits22_16.txt > out/filt22_16.txt; tail -n 1 out/filt22_16.txt; python3 hit_types.py out/hits22_16.txt 13 21
# --- C9: cross-checks with the falsifier's ext_vertex2 on random samples, and tau-free controls
python3 sample.py out/sX20.txt 1 out/inX20_all.txt:1500; python3 sample.py out/sX21.txt 2 out/inX21_1.txt:368 out/inX21_all.txt:632
python3 sample.py out/s21_17.txt 3 out/in21_17_a.txt:500 out/in21_17_b.txt:500 out/in21_17_c.txt:500
python3 sample.py out/s22_16.txt 4 out/in22_16_a.txt:500 out/in22_16_b.txt:500 out/in22_16_c.txt:500
./crosscheck.sh X20 19 7; ./crosscheck.sh X21 20 7; ./crosscheck.sh 21_17 20 8; ./crosscheck.sh 22_16 21 8; cat out/cross_*.done
for spec in "inX20_all 19 11 cX20" "inX21_all 20 12 cX21" "in21_17_all 20 13 c21_17" "in22_16_all 21 14 c22_16" "in21_12 20 15 c21_12"; do
  set -- $spec; python3 control22.py out/$1.txt $2 3000 $3 out/control_$4.txt; ./indep/filter_hits HIT < out/control_$4.txt | tail -n 1; done
# --- C10: witness for f(22) <= 13 (plain Python and e757.core; then the frozen verifier on the claim-format copy)
python3 witness_22.py; python3 claimfmt.py; python3 /home/user/Erdos-757/judge/judge.py witness_check/W22-f22-witness.json
