#!/bin/bash
# Referee L011 round 3 (results/reviews/L011-f22-equals-13__referee__<UTC>.md): every computation of the review, in order.
# Run from this directory.  Referee code: src/ (written from scratch for this round; no e757, no judge except one run on a scratch
# copy of the witness in out/; the prover's programs are only run as copies in out/prover_copy, out/rerun).  Large files: out/, logs/
# (git-ignored).  nauty 2.8.8 sources: the pynauty-2.8.8.1 sdist already on disk (sha256 454d3b0e...83f2), headers by src/mkhdr3.py
# (template substitution; configure NOT run).  Machine: 4 shared cores, nice 5, at most 2 processes.
set -e
mkdir -p out/dl bin logs out/prover_copy out/rerun
[ -d out/dl/pynauty-2.8.8.1 ] || (cp ../L011-round1/out/dl/pynauty-2.8.8.1.tar.gz out/dl/ && cd out/dl && sha256sum pynauty-2.8.8.1.tar.gz && tar xzf pynauty-2.8.8.1.tar.gz)
ND=$PWD/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; B=$PWD/out/nauty_build
python3 -I src/mkhdr3.py $ND $B
NAU="$ND/gtools.c $ND/schreier.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/naurng.c"
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=64 -DPRUNE1=r3prune -DOUTPROC=r3out -DSUMMARY=r3sum -I$B -I$ND -o bin/genbg3 $ND/genbg.c src/hooks3.c $NAU
gcc -O2 -DWORDSIZE=64 -DMAXN=WORDSIZE -I$B -I$ND -o bin/canon3 src/canon3.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c -lm
gcc -O2 -o bin/filt3 src/filt3.c; gcc -O2 -o bin/ext3 src/ext3.c; gcc -O2 -o bin/bf3 src/bf3.c
cp ../../prover/L011/indep/{enum_conn,ext_indep5,filter_hits,filter_hits2}.c out/prover_copy/; (cd out/prover_copy && for p in enum_conn ext_indep5 filter_hits filter_hits2; do gcc -O2 -o $p $p.c; done)
# 1. arithmetic (window cells, degree bounds, counting, slack cells with/without K8, decompositions by two brute-force generators incl.
#    the isolated vertex, record cells, Remarks 4-5)
python3 -I src/arith3.py > out/arith3.txt
# 2. witness C22 from the definitions (+ frozen judge on the scratch copy out/L011R3-witness-c22.json)
python3 -I src/witness3.py > out/witness3.txt; python3 /home/user/Erdos-757/judge/judge.py out/L011R3-witness-c22.json
# 3. filter controls
./bin/filt3 14 < out/controls.txt
# 4. component cells and window cells with genbg3 (TAU0 prune), membership in C by filt3; direct searches incl. (21,13,>=8) D<=3 with F7 prune
./src/run_cells_all.sh; ./src/run_direct.sh          # logs/cells3.txt
# 5. validation: labelled brute force bf3 vs genbg3 vs the prover's enum_conn (class sets by canon3) on 22 small cells
./src/validate3.sh "6 3 2 3" "6 3 1 3" "6 4 1 3" "7 3 1 3" "7 4 2 3" "7 5 2 3" "7 5 3 3" "8 4 2 3" "8 5 3 3" "8 5 2 3" "8 6 3 3" "8 6 2 3" "8 5 3 2" "8 6 3 2" "9 4 3 3" "9 5 3 3" "9 5 2 3" "9 6 3 3" "9 7 3 3" "9 7 4 3" "9 6 3 2" "9 7 3 2" > logs/validate3.txt
# 6. class-set comparisons with the prover's labelled cell lists (all Delta<=3 and in C), T14, T17
P=/home/user/Erdos-757/experiments/prover/L011/out; L8=/home/user/Erdos-757/experiments/prover/L008/indep; L9=/home/user/Erdos-757/experiments/prover/L009/indep
./src/cmp3.sh "6 3 2 $P/cell_6_3_2.txt $P/filt_6_3_2.txt" "8 5 3 $P/cell_8_5_3.txt $P/filt_8_5_3.txt" "8 6 3 $P/cell_8_6_3.txt $P/filt_8_6_3.txt" "9 4 3 $P/cell_9_4_3.txt $P/filt_9_4_3.txt" "10 7 4 $P/cell_10_7_4.txt $P/filt_10_7_4.txt" "10 8 4 $P/cell_10_8_4.txt $P/filt_10_8_4.txt" "11 7 4 $P/cell_11_7_4.txt $P/filt_11_7_4.txt" "13 8 5 $P/cell_13_8_5.txt $P/filt_13_8_5.txt" "13 9 5 $P/cell_13_9_5.txt $P/filt_13_9_5.txt" "14 8 5 $P/cell_14_8_5.txt $P/filt_14_8_5.txt" "16 10 6 $P/cell_16_10_6.txt $P/filt_16_10_6.txt" "19 11 7 $P/cell_19_11_7.txt $P/filt_19_11_7.txt" "12 10 5 $L8/mine_12_10_5_deg3.txt.gz $P/filt_12_10_5.txt" "15 11 6 $L8/mine_15_11_6_deg3.txt.gz $P/filt_15_11_6.txt" "14 12 6 $L9/T14_conn.txt $P/filt_T14.txt" > logs/cmp3.txt
# (T17: grep ^SURV out/C_17_13_7_d3.txt | canon3 17 vs zcat $L9/T17_conn.txt.gz | canon3 17 -- see the review)
# 7. class-level rebuild and final steps with ext3 (inputs = disjoint unions of my in-C class representatives; mode-all = every Delta<=3 class)
for f in in_c4:"AP AP AP AP out/C_8_5_3_d3.txt:8"; do :; done
python3 -I src/build_inputs3.py out/in_c4.txt AP AP AP AP out/C_8_5_3_d3.txt:8; ./bin/ext3 20 7 3 1 < out/in_c4.txt > out/ext_c4.txt
# X20, X21, C8, C6 inputs: the build_inputs3.py calls of the review (see the transcript in the review); then
./src/classlevel3.sh x20; ./src/classlevel3.sh x21; ./src/classlevel3.sh c8; ./src/classlevel3.sh c6; ./src/queue3d.sh   # logs/classlevel3.txt
# 8. class sets of the prover's labelled hit files vs mine; labelled cross-checks ext3 vs ext_indep5; prover re-runs C4, C5 (queue3b), C7 (rerun_c7)
./src/queue3b.sh; ./src/rerun_c7.sh; ./src/hitclasses3.sh
