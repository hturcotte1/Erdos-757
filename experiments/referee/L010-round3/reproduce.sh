#!/bin/bash
# Referee L010 round 3: every computation of the review results/reviews/L010-f20-equals-12__referee__<UTC>.md, in order.
# Run from this directory.  Large outputs go to out/ and logs/ (git-ignored by experiments/referee/*/out/ and */logs*/).
# All code in src/ was written from scratch for this round (no e757, no judge, no prover/falsifier/round-1 code; the prover's
# enum_conn.c is compiled as a COPY in out/rerun/ only to reproduce its call counts).  nauty 2.8.8 sources and the generated
# headers are read from the round-1 folder (experiments/referee/L010-round1/out/dl, out/nauty_build), unmodified.
set -e
ND=/home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; B=/home/user/Erdos-757/experiments/referee/L010-round1/out/nauty_build
NAU="$ND/gtools.c $ND/schreier.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/naurng.c"; P=/home/user/Erdos-757/experiments/prover/L010/out
mkdir -p bin out logs out/rerun
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=64 -DPRUNE1=myprune -DOUTPROC=myout -DSUMMARY=mysummary -I$B -I$ND -o bin/genbg64 $ND/genbg.c src/myhooks.c $NAU
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=32 -DPRUNE1=myprune -DOUTPROC=myout -DSUMMARY=mysummary -I$B -I$ND -o bin/genbg32 $ND/genbg.c src/myhooks.c $NAU
gcc -O2 -DWORDSIZE=64 -I$B -I$ND -o bin/canon src/canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O3 -march=native -o bin/myext src/myext.c; gcc -O3 -march=native -o bin/myfilter src/myfilter.c; gcc -O3 -march=native -o bin/bf src/bf.c
cp /home/user/Erdos-757/experiments/prover/L010/indep/enum_conn.c out/rerun/ && gcc -O2 -o out/rerun/enum_conn out/rerun/enum_conn.c
# 1. arithmetic: window cells (with/without the connectivity bound), degree bounds, slack cells (with/without HY), decompositions incl. isolated vertex
python3 -I src/arith.py > out/arith.txt
# 2. filter controls (F7, relabelled F7, AG(2,3), Fano, Fano minus 1 and 2 lines, Pasch, triangle, F7 minus an edge, claw, 2 edges, non-linear)
./bin/myfilter T 0 all < out/controls.txt
# 3. my genbg census of all component cells (Delta<=3) and the five window cells closed by enumeration
bash src/run_cells.sh > logs/run_cells.log
# 4. class sets (prover's labelled lists vs my census) and the direct enumeration of connected (18,12,>=7) with Delta<=3
bash src/classes.sh > logs/classes.log
# 5. labelled brute force vs my genbg vs the prover's enum_conn on small cells (120 comparisons)
bash src/validate_small.sh > logs/validate_small.log
# 6. my extension program on the prover's labelled inputs; hit sets compared with the prover's; my filter on my hits
./bin/myext 19 7 3 1000 < $P/inH20.txt > out/myhits_H20_proverinputs.txt; ./bin/myfilter HIT 20 < out/myhits_H20_proverinputs.txt | tail -1
./bin/myext 17 6 3 1000 < $P/inX_all.txt > out/myhits_X_proverinputs.txt; ./bin/myfilter HIT 18 notau all < out/myhits_X_proverinputs.txt > out/myfilt_X_proverinputs.txt
./bin/myext 17 6 3 1000 < $P/inX_9.txt | tail -1
bash src/run_c5.sh > logs/run_c5.log
# 7. my own class-representative inputs (components in C / all classes), extension, filter; class comparisons with the prover's inputs and hits
for s in X H19 H20; do for mode in C all; do python3 -I src/build_inputs.py $s $mode out/rep_${s}_${mode}.txt; done; done
for x in "X 17 6" "H19 18 7" "H20 19 7"; do set -- $x; for mode in C all; do ./bin/myext $2 $3 3 100 < out/rep_$1_$mode.txt > out/rephits_$1_$mode.txt; ./bin/myfilter HIT $(( $2 + 1 )) all < out/rephits_$1_$mode.txt > out/repfilt_$1_$mode.txt; tail -1 out/repfilt_$1_$mode.txt; done; done
bash src/hitclasses.sh > logs/hitclasses.log
# 8. witness C20 from the definitions
python3 -I src/check_c20.py
# 9. prover's enum_conn call counts (copy), and the (20,13,8) direct in-C search timing (NOT completed; no claim made)
for c in "19 9 7 1000" "19 10 7 3" "20 12 8 2" "18 12 7 2" "20 13 8 2"; do set -- $c; out/rerun/enum_conn $1 $2 $3 $4 0 | tail -1; done
# TAU0=8 F7PRUNE=1 P3PRUNE=1 ./bin/genbg64 -q -c -Z1 -d1:3 -D3:3 20 13 39:39 0/400   (one part of 400 did not finish within 100 s)
