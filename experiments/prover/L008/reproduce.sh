#!/bin/bash
# Reproduction of every computation cited in results/proofs/L008-f16-equals-10.md (run from this directory).
# F = falsifier folder; its C sources are recompiled here.  The L007 computations it depends on: experiments/prover/L007/reproduce.sh.
# The stored copies of the main outputs are gzipped (indep/*.txt.gz); this script regenerates them uncompressed.  SHA-256 sums of the
# large outputs of the original run: checksums_large_outputs.txt.
set -e
F=/home/user/Erdos-757/experiments/20261017-0300-n16-via-i11
mkdir -p bin rerun
# --- C1: cells and decompositions
python3 decomp.py 16 > decomp_output.txt
# --- falsifier programs recompiled
gcc -O2 -o bin/ext_vertex2 $F/ext_vertex2.c; gcc -O2 -o bin/conn_dfs3 $F/conn_dfs3.c
sed 's/SD=4/SD=6/' $F/conn_dfs3.c > rerun/conn_dfs3s.c; cmp rerun/conn_dfs3s.c $F/conn_dfs3s.c; gcc -O2 -o bin/conn_dfs3s rerun/conn_dfs3s.c
# --- prover programs
cd indep; gcc -O2 -Wall -o enum_conn enum_conn.c; gcc -O2 -Wall -o ext_indep2 ext_indep2.c; gcc -O2 -o filter_hits filter_hits.c; cd ..
# --- C2: case (A) enumeration, four ways
./indep/enum_conn 12 10 5 3 1 > indep/mine_12_10_5_deg3.txt
./bin/conn_dfs3 12 10 5 3 0 0 > rerun/conn_dfs3_12_10_5.txt
for I in 0 1; do ./bin/conn_dfs3s 12 10 5 3 0 0 2 $I > rerun/conn_dfs3s_12_10_5_part$I.txt; done
python3 compare_found.py indep/mine_12_10_5_deg3.txt -- rerun/conn_dfs3_12_10_5.txt -- rerun/conn_dfs3s_12_10_5_part0.txt rerun/conn_dfs3s_12_10_5_part1.txt -- $F/R12_labelled.txt.gz
# --- C3: case (B) enumeration (prover, single process; about 25-40 min) and comparison with the falsifier's split run
./indep/enum_conn 15 11 6 3 1 > indep/mine_15_11_6_deg3.txt
python3 compare_found.py indep/mine_15_11_6_deg3.txt -- $F/g15_11_6_part0.txt.gz $F/g15_11_6_part1.txt.gz
# --- C4: extensions, both programs, all labelled inputs
python3 build_inputs.py A indep/mine_12_10_5_deg3.txt rerun/inputA_all.txt
python3 build_inputs.py B indep/mine_15_11_6_deg3.txt rerun/inputB_mine.txt
zcat $F/G_B_conn15.txt.gz > rerun/inputB_falsifier.txt
./bin/ext_vertex2 15 7 3 < rerun/inputA_all.txt > rerun/hitsA_all_ext_vertex2.txt
./indep/ext_indep2 15 6 3 < rerun/inputA_all.txt > indep/hitsA_all_mine.txt
python3 compare_hits.py rerun/hitsA_all_ext_vertex2.txt indep/hitsA_all_mine.txt
./bin/ext_vertex2 15 7 3 < rerun/inputB_falsifier.txt > rerun/hitsB_ext_vertex2_rerun.txt       # about 10 min
./indep/ext_indep2 15 6 3 < rerun/inputB_falsifier.txt > indep/hitsB_falsifier_input_mine.txt
./indep/ext_indep2 15 6 3 < rerun/inputB_mine.txt > indep/hitsB_mine_input_mine.txt
zcat $F/hits_caseB.txt.gz > rerun/hitsB_stored.txt
python3 compare_hits.py rerun/hitsB_stored.txt indep/hitsB_falsifier_input_mine.txt
python3 compare_hits.py rerun/hitsB_stored.txt rerun/hitsB_ext_vertex2_rerun.txt
python3 compare_hits.py rerun/hitsB_stored.txt indep/hitsB_mine_input_mine.txt
./indep/ext_indep2 15 6 3 < $F/G_R12_AP.txt > indep/hitsA_classes_mine.txt
# --- C5: filters and control
./indep/filter_hits HIT < indep/hitsA_all_mine.txt | tail -n 1
./indep/filter_hits HIT < indep/hitsB_falsifier_input_mine.txt | tail -n 1
./indep/filter_hits HIT < indep/hitsB_mine_input_mine.txt | tail -n 1
python3 control_sample.py; ./indep/filter_hits HIT < control_sample_hits.txt | tail -n 1
# --- Step 8 remarks (descriptive)
python3 breakdown_A.py indep/hitsA_all_mine.txt
./indep/filter_hits FOUND < indep/mine_12_10_5_deg3.txt > rerun/filterA_R.txt; python3 classes_of.py rerun/filterA_R.txt SURVIVOR rerun/classesA_Oplus.txt
python3 -c "import json; reps=json.load(open('$F/classes_B_reps.json')); open('indep/classesB49_found.txt','w').write(''.join('FOUND: '+' '.join('(%d,%d,%d)'%tuple(e) for e in es)+'\n' for es,f7 in reps))"
./indep/filter_hits FOUND < indep/classesB49_found.txt | tail -n 1
python3 classes_of.py indep/mine_15_11_6_deg3.txt FOUND rerun/classesB_mine.txt; ./indep/filter_hits FOUND < rerun/classesB_mine.txt | tail -n 1
# --- C6: witness for f(16) <= 10
python3 witness_16.py
