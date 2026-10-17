#!/bin/bash
# Reproduction of every computation cited in results/proofs/L012-n23-record-no-degree-4.md (run from this directory; about 1.5 CPU-hours).
# Large files go to out/ (git-ignored).  Inputs from earlier certificates: L008-L011 labelled lists (consistency checks only), the census
# files data/census_n14_m12_classes.jsonl.gz and experiments/20261014-1005-census-dfs/results/realized_n12.json.gz (controls only);
# nauty 2.8.8 sources (unmodified) from the referee's download folder; the falsifier's logs (comparisons only).
set -e
F=/home/user/Erdos-757/experiments/20261017-1030-n23-record-cell
ND=/home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; NB=/home/user/Erdos-757/experiments/referee/L010-round1/out/nauty_build
mkdir -p out bin
gcc -O2 -Wall -o bin/enum_conn indep/enum_conn.c; gcc -O2 -Wall -o bin/filt indep/filt.c; gcc -O2 -Wall -o bin/ext_d indep/ext_d.c
gcc -O2 -Wall -o bin/realize indep/realize.c; gcc -O2 -Wall -o bin/realize_extra indep/realize_extra.c
gcc -O2 -DWORDSIZE=64 -DMAXN=64 -I$NB -I$ND -o bin/canon indep/canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
# --- C1: arithmetic (degree bounds, decompositions by three generators, record cells)
python3 arith23.py > arith23_output.txt
# --- C2: tool validation
L11=../L011/out
zcat ../L008/indep/mine_12_10_5_deg3.txt.gz | ./bin/filt FOUND 12 | tail -n 1; zcat ../L008/indep/mine_15_11_6_deg3.txt.gz | ./bin/filt FOUND 15 | tail -n 1
zcat $L11/hitsX20.txt.gz | head -200000 | ./bin/filt HIT 20 notau | tail -n 1; zcat $L11/hitsX20.txt.gz | head -200000 | ../L011/indep/filter_hits2 HIT notau | tail -n 1
./bin/ext_d 20 7 8 3 2 noprune < $L11/in21_12.txt > out/t_21_12_noprune.txt; python3 compare_hits.py out/t_21_12_noprune.txt $L11/hits21_12.txt
./bin/ext_d 19 7 8 3 2 noprune < $L11/sX20.txt > out/t_sX20.txt; python3 compare_hits.py out/t_sX20.txt $L11/hits_sX20_mine.txt
bash validate_ext_bf.sh > validate_ext_bf_output.txt
head -300 $L11/sX21.txt > out/t_sX21_in.txt; ./bin/ext_d 20 7 8 3 2 noprune < out/t_sX21_in.txt > out/t_sX21.txt; ../L011/indep/ext_indep5 20 7 3 < out/t_sX21_in.txt > out/t_sX21_ref.txt; python3 compare_hits.py out/t_sX21.txt out/t_sX21_ref.txt
# --- C3: the engine (all cells), route 4 and route 20
rm -rf out/cells out/engine.log; NPROC=3 python3 route.py 4 > out/route4_run.log; NPROC=3 python3 route.py 20 > out/route20_run.log
python3 compare_cells.py route4b.log route20.log > compare_cells_output.txt; python3 compare_branches.py route4b.log route20.log > compare_branches_output.txt
python3 bf_decomp.py > bf_decomp_output.txt
python3 sample.py out/r4_sample_in.txt 7 out/route4_inputs.txt:60; ./bin/ext_d 22 9 10 4 3 < out/r4_sample_in.txt > out/r4_sample_pruned.txt
./bin/ext_d 22 9 10 4 3 noprune < out/r4_sample_in.txt > out/r4_sample_noprune.txt; ./bin/filt HIT 23 notau < out/r4_sample_noprune.txt > out/r4_sample_noprune_filt.txt
grep '^SURVIVOR' out/r4_sample_noprune_filt.txt | sed 's/^SURVIVOR:/HIT:/; s/ #conn=.*//' > out/r4_sample_noprune_C.txt; python3 compare_hits.py out/r4_sample_noprune_C.txt out/r4_sample_pruned.txt
# --- C4: unpruned final step of route 4 and comparison of the 699 classes with the falsifier's raw hits
./bin/ext_d 22 9 10 4 3 noprune < out/route4_inputs.txt > out/r4_noprune_all.txt; tail -n 1 out/r4_noprune_all.txt
./bin/filt HIT 23 notau < out/r4_noprune_all.txt > out/r4_noprune_filt.txt; tail -n 1 out/r4_noprune_filt.txt
grep '^SURVIVOR' out/r4_noprune_filt.txt | sed 's/^SURVIVOR:/HIT:/; s/ #conn=.*//' > out/r4_noprune_C.txt; python3 compare_hits.py out/r4_noprune_C.txt out/route4_hits.txt
grep '^FOUND' out/route4_classes.txt > out/route4_classes_only.txt; ./bin/filt FOUND 23 tau 10 < out/route4_classes_only.txt | tail -n 1
./bin/canon 23 < out/route4_classes_only.txt | sort -u > out/prover_route4_classes_canon.txt
gzip -c out/route4_classes_only.txt > route4_classes.txt.gz; tar czf cells.tar.gz -C out cells; python3 degree_stats.py > degree_stats_output.txt
zcat $F/out/hits_final_route4_a.txt.gz $F/out/hits_final_route4_b.txt.gz | grep '^HIT' | ./bin/canon 23 | sort -u > out/falsifier_route4_classes_canon.txt
cmp out/prover_route4_classes_canon.txt out/falsifier_route4_classes_canon.txt && echo "699 classes identical to the falsifier's"
# --- C5: exact realization of the 699 classes, and its controls
./bin/realize 23 < out/route4_classes_only.txt > out/realize_r4.txt; grep '^TOTAL' out/realize_r4.txt
./bin/realize_extra 23 < out/route4_classes_only.txt > out/realize_extra_r4.txt
python3 abase_check.py > abase_control_output.txt
python3 census_control.py /home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz 14 0 > census_control_output.txt
for i in 1 2 3; do sed -n "${i}p" py_sample.txt > out/py_sample_$i.txt; python3 realize_py.py 23 < out/py_sample_$i.txt; ./bin/realize 23 < out/py_sample_$i.txt | head -1; done > realize_py_crosscheck_output.txt
# --- C6: validation of the engine and of the cell lists
NPROC=2 python3 validate_engine.py > out/validate_engine_run.log
python3 consistency.py > /dev/null
python3 canon_test.py > canon_test_output.txt
python3 probe_route3.py > probe_route3_output.txt
