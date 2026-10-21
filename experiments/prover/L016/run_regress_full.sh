#!/bin/bash
# (L016) full-cell regressions of ext_d_fast: all inputs of L014's top cell (23,21,10,3) (L014 counters: nodes 48,029,683,
# hits_F7free 4,249, hits_in_C 0; noprune: 49,109,927 nodes, 10,986 extensions), and the inputs of (26,22,11,3) rebuilt from the
# worker's cell(25,19,10,3) and the refereed lists (out/cellsB): a 1,000-input sample, original (MAXP 640) against fast.
cd /home/user/Erdos-757/experiments/prover/L016
nice -n 10 ./bin/ext_d_fast 22 9 10 3 2 < out/regress/inputs_23_21_10_3.txt | tail -1 > out/regress/full_23_21_10_3_fast.txt
nice -n 10 ./bin/ext_d_fast 22 9 10 3 2 noprune < out/regress/inputs_23_21_10_3.txt | grep -c '^HIT' > out/regress/full_23_21_10_3_fast_noprune_hits.txt
nice -n 10 ./bin/ext_d_fast 22 9 10 3 2 noprune < out/regress/inputs_23_21_10_3.txt | tail -1 >> out/regress/full_23_21_10_3_fast_noprune_hits.txt
CELLDIR=$PWD/out/cellsB ENGINELOG=/dev/null nice -n 10 python3 gen_inputs.py 26 22 11 3 out/regress/inputs_26_22_11_3_workerlists.txt > out/regress/gen_26_22_11_3_workerlists.txt 2>&1
nice -n 10 python3 regress.py out/regress/inputs_26_22_11_3_workerlists.txt 1000 31 bin/ext_d bin/ext_d_fast 25 10 11 3 2 > out/regress/r_26_22_11.txt 2>&1
echo done >> out/regress/r_26_22_11.txt
