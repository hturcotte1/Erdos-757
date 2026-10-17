#!/bin/bash
# Reproduction of every computation cited in results/proofs/L010-f20-equals-12.md (run from this directory).  Large files go to out/
# (git-ignored).  Uses the prover's enumerations of L008 (mine_12_10_5_deg3, mine_15_11_6_deg3) and L009 (cell_6_3_2, cell_8_5_3,
# cell_10_7_4, cell_13_8_5) as inputs; see those folders' reproduce.sh to regenerate them.
set -e
F=/home/user/Erdos-757/experiments/20261017-0705-n19-n20-via-i11
L8=/home/user/Erdos-757/experiments/prover/L008/indep; L9=/home/user/Erdos-757/experiments/prover/L009/indep
mkdir -p out bin
cd indep; gcc -O2 -Wall -o enum_conn enum_conn.c; gcc -O2 -Wall -o ext_indep4 ext_indep4.c; gcc -O2 -o filter_hits filter_hits.c; gcc -O2 -o filter_hits2 filter_hits2.c; cd ..
gcc -O2 -o bin/ext_vertex2 $F/ext_vertex2.c
# --- C1: arithmetic
python3 decomp20.py > decomp20_output.txt
# --- C2: enumerations
(cd indep && ./run_cells.sh > run_cells.log)
for c in 8_6_3 9_4_3 11_7_4 14_8_5; do python3 compare_found.py out/cell_$c.txt -- $F/K_$c.txt | tail -n 1; done
for c in 6_3_2 8_5_3 10_7_4; do python3 compare_found.py $L9/cell_$c.txt -- $F/K_$c.txt | tail -n 1; done
zcat $L8/mine_12_10_5_deg3.txt.gz > out/cell_12_10_5.txt; zcat $L8/mine_15_11_6_deg3.txt.gz > out/cell_15_11_6.txt
python3 compare_found.py out/cell_12_10_5.txt -- $F/K_12_10_5.txt | tail -n 1
# --- C3: components in C
for c in 6_3_2 8_5_3 10_7_4 13_8_5; do ./indep/filter_hits FOUND < $L9/cell_$c.txt > out/filt_$c.txt; tail -n 1 out/filt_$c.txt; done
for c in 8_6_3 9_4_3 11_7_4 14_8_5 12_10_5 15_11_6; do ./indep/filter_hits FOUND < out/cell_$c.txt > out/filt_$c.txt; tail -n 1 out/filt_$c.txt; done
# --- C4: rebuild of connected (18,12,7) with a degree-3 vertex: the 10 decompositions of (17,9) with slack 3 (4 of them empty)
python3 combine.py out/inX_3.txt out/filt_8_5_3.txt:SURVIVOR out/filt_9_4_3.txt:SURVIVOR
python3 combine.py out/inX_5.txt AP out/filt_14_8_5.txt:SURVIVOR
python3 combine.py out/inX_7.txt AP out/filt_6_3_2.txt:SURVIVOR out/filt_8_5_3.txt:SURVIVOR
python3 combine.py out/inX_8.txt AP AP out/filt_11_7_4.txt:SURVIVOR
python3 combine.py out/inX_9.txt AP AP out/filt_10_7_4.txt:SURVIVOR ISO
python3 combine.py out/inX_10.txt AP AP AP out/filt_8_6_3.txt:SURVIVOR
cat out/inX_3.txt out/inX_5.txt out/inX_7.txt out/inX_8.txt out/inX_10.txt > out/inX_falsifier_types.txt; cat out/inX_falsifier_types.txt out/inX_9.txt > out/inX_all.txt
./indep/ext_indep4 17 6 3 < out/inX_all.txt > out/hitsX.txt; tail -n 1 out/hitsX.txt
./indep/filter_hits HIT < out/hitsX.txt > out/filtX.txt; tail -n 1 out/filtX.txt; python3 connected_filter.py out/filtX.txt out/X_conn.txt
./bin/ext_vertex2 17 7 3 < out/inX_9.txt > out/hitsX9_ev2.txt; ./indep/ext_indep4 17 6 3 < out/inX_9.txt > out/hitsX9_mine.txt; python3 compare_hits.py out/hitsX9_ev2.txt out/hitsX9_mine.txt
python3 -c "import json,collections; X=json.load(open('$F/X18_deg3_classes.json')); print(len(X))"
# --- C5: final step for (19,15,8)
python3 combine.py out/inH19_a.txt AP AP out/filt_12_10_5.txt:SURVIVOR; python3 combine.py out/inH19_b.txt AP out/filt_15_11_6.txt:SURVIVOR
python3 combine.py out/inH19_c.txt out/filt_10_7_4.txt:SURVIVOR out/filt_8_5_3.txt:SURVIVOR; cat out/inH19_a.txt out/inH19_b.txt out/inH19_c.txt > out/inH19.txt
./indep/ext_indep4 18 7 3 < out/inH19.txt > out/hitsH19.txt; tail -n 1 out/hitsH19.txt
./indep/filter_hits2 HIT notau < out/hitsH19.txt > out/filtH19.txt; tail -n 1 out/filtH19.txt
python3 -c "
import random
random.seed(20)
for src,k,dst in [('out/inX_falsifier_types.txt',1500,'out/inX_sample.txt'),('out/inH19.txt',2000,'out/inH19_sample.txt')]:
    L=open(src).read().splitlines(); open(dst,'w').write(chr(10).join(random.sample(L,k))+chr(10))"
./bin/ext_vertex2 17 7 3 < out/inX_sample.txt > out/hitsXs_ev2.txt; ./indep/ext_indep4 17 6 3 < out/inX_sample.txt > out/hitsXs_mine.txt; python3 compare_hits.py out/hitsXs_ev2.txt out/hitsXs_mine.txt
./bin/ext_vertex2 18 8 3 < out/inH19_sample.txt > out/hitsH19s_ev2.txt; ./indep/ext_indep4 18 7 3 < out/inH19_sample.txt > out/hitsH19s_mine.txt; python3 compare_hits.py out/hitsH19s_ev2.txt out/hitsH19s_mine.txt
python3 control19.py; ./indep/filter_hits HIT < out/control19_hits.txt | tail -n 1
# --- C6: (20,13,8) with a degree-3 vertex: case [AP,AP,AP,(10,7,4)]
python3 combine.py out/inH20.txt AP AP AP out/filt_10_7_4.txt:SURVIVOR; ./indep/ext_indep4 19 7 3 < out/inH20.txt > out/hitsH20.txt; tail -n 1 out/hitsH20.txt
./indep/filter_hits HIT < out/hitsH20.txt | tail -n 1
./bin/ext_vertex2 19 8 3 < out/inH20.txt > out/hitsH20_ev2.txt; python3 compare_hits.py out/hitsH20_ev2.txt out/hitsH20.txt
python3 combine.py out/inH20_C10all.txt ../L007/indep/mine_10_7_4.txt AP AP AP; ./indep/ext_indep4 19 7 3 < out/inH20_C10all.txt > out/hitsH20_C10all.txt
./indep/filter_hits HIT < out/hitsH20_C10all.txt | tail -n 1
# --- C7: witness for f(20) <= 12; record cells at n = 21..23
python3 witness_20.py; python3 cells_21_23.py > window_21_23.txt
