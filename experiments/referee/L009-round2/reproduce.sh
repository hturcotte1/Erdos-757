#!/bin/bash
# Referee L009 round 2 (f(18) = 11): every command of the review, from scratch.  Large outputs go to out/ and logs/ (git-ignored);
# small evidence files are copied to small/.  Machine: 4 shared cores; everything under nice 5, at most 2 processes.
set -e
R=/home/user/Erdos-757/experiments/referee/L009-round2; cd $R; mkdir -p out/dl out/bin out/unpack logs small
# --- nauty 2.8.8 (PyPI sdist pynauty-2.8.8.1, sha256 454d3b0e605d649d13478afb090daef4a152f15c4a337a391fe69fded7e683f2)
[ -f out/dl/pynauty-2.8.8.1.tar.gz ] || pip download --no-deps --no-binary :all: pynauty==2.8.8.1 -d out/dl
sha256sum out/dl/pynauty-2.8.8.1.tar.gz
tar -xzf out/dl/pynauty-2.8.8.1.tar.gz -C out/unpack; rm -rf out/nauty; cp -r out/unpack/pynauty-2.8.8.1/src/nauty2_8_8 out/nauty
(cd out/nauty && ./configure --disable-popcnt > /dev/null && make genbg labelg countg > /dev/null)
ND=out/nauty
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=64 -DPRUNE1=r2prune1 -DPRUNE2=r2prune2 -DOUTPROC=r2out -DSUMMARY=r2summary -I$ND \
    -o out/bin/genbg_r2 $ND/genbg.c src/r2hooks.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O2 -o out/bin/bf2 src/bf2.c; gcc -O2 -o out/bin/ext_r2 src/ext_r2.c; gcc -O2 -o out/bin/cfilter_r2 src/cfilter_r2.c; gcc -O2 -o out/bin/anneal_c src/anneal_c.c -lm
P=/home/user/Erdos-757/experiments/prover/L009
for p in enum_conn ext_indep2 ext_indep3 filter_hits; do gcc -O2 -o out/bin/${p}_prover $P/indep/$p.c; done
# --- A. arithmetic: window cells, slack cells (with and without HY), decompositions, deletion degree bounds
python3 src/arith.py > logs/arith.txt
# --- B. validation of genbg_r2 and the prover's enum_conn against the brute force bf2 (class sets + labelled counts)
./src/validate_small.sh > logs/validate_small.log     # (stopped after the first 14 cells for CPU reasons; see review)
./src/validate_counts.sh "9 7 3 3" "9 7 4 7" "9 6 3 6" "9 5 3 5" "10 5 4 5" > logs/validate_counts.log
# --- C. C-membership tests: definitional checker vs my hook vs the prover's filter_hits vs cfilter_r2 (controls + 146 genbg outputs)
python3 src/defcheck.py HIT < small/controls.txt; out/bin/filter_hits_prover HIT < small/controls.txt | tail -n 1; out/bin/cfilter_r2 < small/controls.txt
cat out/val/gb_*.txt out/direct/d_14_12_6.txt out/direct/d_17_12_7.txt > out/flagcheck_in.txt   # (needs D first; order as in the review)
# --- D. direct genbg enumerations (no Lemma R, no decomposition)
mkdir -p out/direct out/cells out/rebuild
TAU0=6 out/bin/genbg_r2 -q -c -Z1 -d1:3 -D3:3 14 12 36:36 > out/direct/d_14_12_6.txt 2> out/direct/d_14_12_6.err
TAU0=6 F7PRUNE=1 out/bin/genbg_r2 -q -c -Z1 -d1:3 -D3:3 14 12 36:36 > out/direct/d_14_12_6_f7p.txt 2> out/direct/d_14_12_6_f7p.err
TAU0=7 out/bin/genbg_r2 -q -c -Z1 -d1:3 -D3:3 17 12 36:36 > out/direct/d_17_12_7.txt 2> out/direct/d_17_12_7.err
src/run_d17.sh 0; src/run_d17.sh 1          # F7-pruned (17,13,tau>=7), Delta<=3, parts 0/2 and 1/2
src/run_d17_single.sh                        # the same without res/mod splitting
src/run_d17_tauonly.sh                       # tau prune only (no F7 prune): all 80 classes
./src/run_cells.sh > logs/cells.log          # component cells and empty window cells, class sets vs the prover's lists
# --- E. my class-level rebuild (Lemma R) and the final step with my own extension code
python3 src/build_rebuild.py
out/bin/ext_r2 13 6 3 < out/rebuild/in14.txt > out/rebuild/x14.txt; out/bin/ext_r2 16 7 3 < out/rebuild/in17.txt > out/rebuild/x17.txt
out/bin/ext_r2 17 8 3 < out/rebuild/in18_reps.txt | tail -n 1                 # final step, 6 + 2 class representatives
sed 's/.*E://' out/direct/d17_tauonly.txt > out/direct/in18_T17all.txt; sed 's/.*E://' out/direct/d_14_12_6.txt | sed 's/$/ (14,15,16)/' > out/direct/in18_T14all.txt
cat out/direct/in18_T17all.txt out/direct/in18_T14all.txt | out/bin/ext_r2 17 8 3 | tail -n 1                 # final step, all 118 unfiltered tight graphs
python3 src/lemmaR_check.py out/rebuild/T17_reps.txt out/direct/in18_T14reps.txt
# (filters, canonical forms and comparisons: see the review, sections D and E; canonical forms by src/hg2g6.py | src/canon.sh)
# --- F. the prover's pipeline C2-C7 re-run in out/pr with SHA-256 comparison
./src/rerun_prover.sh > logs/rerun_prover.log 2>&1
# --- G. witness A_18, data tests, heuristic annealing
python3 -I witness/check_A18.py > logs/witness.txt; python3 -I src/datatests.py > logs/datatests.txt
for n in 11 12 13 14 15 16 17 18; do for s in 1 2; do out/bin/anneal_c $n 20 $((n*100+s)); done; done > logs/anneal.log
