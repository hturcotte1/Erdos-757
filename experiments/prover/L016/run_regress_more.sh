#!/bin/bash
# (L016) C6: byte-level regressions of bin/ext_d_fast against bin/ext_d (MAXP 640, Gosper) on seeded random samples of the inputs of
# the heavy cells: (24,16,9,3) d=3 (out/regress/rec_24_16_9_D3_d3_tp8_c0.in = inputs[0::3] of run F's d=3 branch, copied at 23:50),
# (25,19,10,3) and (26,22,11,3) (input lists rebuilt by gen_inputs.py from the worker's lists, out/cellsW and out/cellsB), plus wrong-TG
# (bad_tau) cases.  Output: out/regress/r_more.txt
cd /home/user/Erdos-757/experiments/prover/L016; R=out/regress
{
python3 regress.py $R/rec_24_16_9_D3_d3_tp8_c0.in 300 11 bin/ext_d bin/ext_d_fast 23 8 9 3 2
python3 regress.py $R/rec_24_16_9_D3_d3_tp8_c0.in 200 12 bin/ext_d bin/ext_d_fast 23 8 9 3 2 noprune
python3 regress.py $R/inputs_25_19_10_3_workerlists.txt 400 5 bin/ext_d bin/ext_d_fast 24 9 10 3 2
python3 regress.py $R/inputs_25_19_10_3_workerlists.txt 200 6 bin/ext_d bin/ext_d_fast 24 9 10 3 2 noprune
python3 regress.py $R/inputs_26_22_11_3_workerlists.txt 1000 31 bin/ext_d bin/ext_d_fast 25 10 11 3 2
python3 regress.py $R/inputs_26_22_11_3_workerlists.txt 100 32 bin/ext_d bin/ext_d_fast 25 10 11 3 2 noprune
python3 regress.py $R/inputs_26_22_11_3_workerlists.txt 100 33 bin/ext_d bin/ext_d_fast 25 9 11 3 2
python3 regress.py $R/inputs_26_22_11_3_workerlists.txt 100 34 bin/ext_d bin/ext_d_fast 25 11 11 3 2
python3 regress.py $R/inputs_25_19_10_3_workerlists.txt 100 35 bin/ext_d bin/ext_d_fast 24 8 10 3 2
python3 regress.py $R/inputs_25_19_10_3_workerlists.txt 100 36 bin/ext_d bin/ext_d_fast 24 9 9 1 2
} > $R/r_more.txt 2>&1
echo REGRESS_MORE_DONE >> $R/r_more.txt
