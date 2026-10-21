#!/bin/bash
# Reproduction of every computation cited in results/proofs/L016-i11-n27-f27-equals-16.md (run from this directory; about 4 CPU-hours
# on 3 cores, most of it run F; large files in out/, git-ignored).  Read-only inputs: the C sources of experiments/prover/L012/indep,
# nauty 2.8.8 (the copy used by L012-L014), L012's engine.py/decomp22.py, L014's stream.py, run_cells.py, tree.py, gen_inputs.py,
# input_counts.py, decomp_check.py, ext_validate.py, pyverify.py (copied, byte-identical), the refereed cell lists of L013 and L014
# (seeds), and, for the comparisons only (C8), the worker's experiments/20261017-2150-i11-n27/.
set -e
cd /home/user/Erdos-757/experiments/prover/L016
SP=/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad
ND=/home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; NB=/home/user/Erdos-757/experiments/referee/L010-round1/out/nauty_build
S=../L012/indep; W=../../20261017-2150-i11-n27
# --- C2: builds
mkdir -p bin bin256 src fast/bin out/cells out/logs out/regress
sed 's/^#define MAXP 256$/#define MAXP 640/' $S/ext_d.c > src/ext_d_maxp640.c          # the one-line change (0.6)
# src/ext_d_fast.c: src/ext_d_maxp640.c + bcov (0.7); tracked in this directory (written by the prover, see ext_d_fast_diff.txt)
gcc -O2 -Wall -o bin/enum_conn $S/enum_conn.c; gcc -O2 -Wall -o bin/filt $S/filt.c; gcc -O2 -Wall -o bin/ext_d src/ext_d_maxp640.c
gcc -O2 -Wall -o bin256/ext_d $S/ext_d.c; gcc -O2 -Wall -o bin/ext_d_fast src/ext_d_fast.c
gcc -O2 -Wall -o bin/realize $S/realize.c; gcc -O2 -Wall -o bin/realize_extra $S/realize_extra.c
gcc -O2 -DWORDSIZE=64 -DMAXN=64 -I$NB -I$ND -o bin/canon $S/canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
cp bin/canon bin/filt bin/enum_conn fast/bin/; cp bin/ext_d_fast fast/bin/ext_d
for f in engine.py decomp22.py; do [ -e $f ] || cp ../L012/$f .; done
for f in stream.py run_cells.py tree.py gen_inputs.py input_counts.py decomp_check.py ext_validate.py pyverify.py; do [ -e $f ] || cp ../L014/$f .; done
cp engine.py decomp22.py stream.py run_cells.py fast/
bash build_check16.sh > build_check16_output.txt
# --- seeds: the refereed lists of L013 and L014
mkdir -p $SP/seedL013 $SP/seedL014 out/seed_refereed; tar xzf ../L013/cells.tar.gz -C $SP/seedL013; tar xzf ../L014/cells.tar.gz -C $SP/seedL014
zcat ../L014/cell_15_13_6_D3.txt.gz > $SP/seedL014/cells/cell_15_13_6_D3.txt
python3 seed_check.py $SP/seedL013/cells $SP/seedL014/cells > seed_check_output.txt
cp $SP/seedL013/cells/* out/seed_refereed/; cp $SP/seedL014/cells/* out/seed_refereed/
cp out/seed_refereed/* out/cells/
# --- C1: arithmetic, plan, trees, decompositions
python3 arith16.py > arith16_output.txt
(cd /home/user/Erdos-757 && python3 -m e757.fn_bounds) > fn_bounds_output.txt
mkdir -p $SP/plancells; cp out/seed_refereed/* $SP/plancells/
CELLDIR=$SP/plancells ENGINELOG=/dev/null python3 plan16.py 27,13,10,2 27,18,11,2 27,14,10,3 27,19,11,3 27,25,12,3 > out/plan_all_from_refereed.txt
mkdir -p out/dummycells
for k in "27 13 10 2" "27 14 10 3" "27 18 11 2" "27 19 11 3" "27 25 12 3"; do f=tree_$(echo $k | tr ' ' '_').txt
  CELLDIR=$PWD/out/dummycells ENGINELOG=/dev/null python3 tree.py $k > $f
  CELLDIR=$PWD/out/dummycells ENGINELOG=/dev/null python3 decomp_check.py $f > decomp_check_$(echo $k | tr ' ' '_')_output.txt; done
# --- C3: run A (45 small lists incl. the four sparse top cells), then run F (the four heavy lists, ext_d_fast)
bash run_A.sh
mkdir -p out/cellsF out/workF; cp out/cells/* out/cellsF/
NP=3 NI=5 TO=7200 bash run_F1.sh 24,16,9,3 25,19,10,3 26,22,11,3 27,25,12,3
python3 top_info16.py out/cells 27,13,10,2 27,14,10,3 27,18,11,2 27,19,11,3 > top_info_sparse_output.txt
# --- run B2 (cross-check, item (b)): (26,22,11,3), (27,25,12,3) from the worker's cell(25,19,10,3)
mkdir -p out/cellsB out/workB; cp out/seed_refereed/* out/cellsB/; zcat $W/cell_25_19_10_D3.txt.gz > out/cellsB/cell_25_19_10_D3.txt
zcat $W/cell_25_19_10_D3.txt.gz > out/worker_cell_25_19_10_D3.txt
bash run_B2.sh; bash run_postB.sh
# --- C4: unpruned final steps of the sparse tops; post-checks of run F (C3, C4, C8)
bash run_extval_sparse.sh
bash run_post_light.sh
# --- C5: audits and closure checks (run_after24.sh: closure of run F's (24,16,9,3) and of the worker's (25,19,10,3) against out/cellsF)
CELLDIR=$PWD/out/cells ENGINELOG=/dev/null python3 closure.py out/cells 23 13 8 3 all > out/closure_23_13_8_3.txt
bash run_after24.sh
cat out/closure_23_13_8_3.txt out/closure_F_24_16_9_3.txt out/closure_worker_25_19_10_3.txt closure_B2_26_22_11_3.txt > closure_output.txt
bash run_audit_all.sh
# --- C6: regressions of ext_d_fast (and MAXP 256 vs 640)
CELLDIR=$PWD/out/seed_refereed ENGINELOG=/dev/null python3 gen_inputs.py 23 21 10 3 out/regress/inputs_23_21_10_3.txt > out/regress/gen_23_21_10_3.txt
python3 regress.py out/regress/inputs_23_21_10_3.txt 3000 21 bin256/ext_d bin/ext_d 22 9 10 3 2 > out/regress/r_23_21_10.txt
python3 regress.py out/regress/inputs_23_21_10_3.txt 1000 22 bin/ext_d bin/ext_d_fast 22 9 10 3 2 >> out/regress/r_23_21_10.txt
python3 regress.py out/regress/inputs_23_21_10_3.txt 1000 23 bin256/ext_d bin/ext_d_fast 22 9 10 3 2 noprune >> out/regress/r_23_21_10.txt
mkdir -p out/cellsW; cp out/cellsB/* out/cellsW/; cp $W/out/cells/cell_24_16_9_D3.txt out/cellsW/; for k in $(cat listA.txt); do f=cell_$(echo $k | awk -F, '{print $1"_"$2"_"$3"_D"$4}').txt; [ -e out/cellsW/$f ] || cp out/cells/$f out/cellsW/; done
CELLDIR=$PWD/out/cellsW ENGINELOG=/dev/null python3 gen_inputs.py 25 19 10 3 out/regress/inputs_25_19_10_3_workerlists.txt > out/regress/gen_25_19_10_3_workerlists.txt
# (out/regress/rec_24_16_9_D3_d3_tp8_c0.in is a copy of run F's input file out/workF/rec_24_16_9_D3_d3_tp8_c0.in, taken while run F ran)
bash run_regress_full.sh          # also builds out/regress/inputs_26_22_11_3_workerlists.txt from out/cellsB
bash run_regress_more.sh
# --- C8 chunk level (the worker's chunk files are unpacked first)
mkdir -p out/wchunks; tar xzf $W/chunks_25_19_10_d3_tp9.tar.gz -C out/wchunks
python3 chunk_check.py out/regress/inputs_25_19_10_3_workerlists.txt out/wchunks/chunks/25_19_10_D3_d3_tp9 bin/ext_d_fast 1 29 40 48 49 51 69 74 > chunk_check_output.txt
# --- comparisons of the 48 lists available before run F finished (C8)
# (see the certificate; compare_cells48_output.txt, compare_branches48_output.txt)
# --- C7: the explicit set; tarball of the new lists
python3 c27_construction.py > c27_construction_output.txt
bash make_tarball.sh
cp out/progress_A.jsonl out/progress_F.jsonl out/progress_B2.jsonl .
bash run_auditF.sh   # audit and closure of run F's own heavy lists (after run F)
bash run_G.sh; bash run_chunks_gosper.sh   # top cell and chunks 1, 40, 74 with the Gosper build
