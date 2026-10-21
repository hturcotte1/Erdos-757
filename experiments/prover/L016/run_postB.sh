#!/bin/bash
# (L016) checks of run B2's lists (out/cellsB: refereed seeds + the worker's cell(25,19,10,3)): branch data, input counts, audit,
# closure, the unpruned final step of the top cell (27,25,12,3).
cd /home/user/Erdos-757/experiments/prover/L016
python3 top_info16.py out/cellsB 26,22,11,3 27,25,12,3 > top_info_B2_output.txt
for k in 26,22,11,3 27,25,12,3; do python3 input_counts.py $PWD/out/cellsB $(echo $k | tr ',' ' '); done > input_counts_B2_output.txt 2>&1
nice -n 10 timeout 900 python3 filters16.py out/cellsB/cell_26_22_11_D3.txt 26 22 11 3 36 2622 > audit_B2_26_22_11_3.txt 2>&1
nice -n 10 timeout 1800 python3 closure.py out/cellsB 26 22 11 3 all > closure_B2_26_22_11_3.txt 2>&1
CELLDIR=$PWD/out/cellsB ENGINELOG=/dev/null nice -n 10 timeout 1800 python3 ext_validate.py 27 25 12 3 out/extvalB 2000 > extval_27_25_12_3_B2_output.txt 2>&1
echo POSTB_DONE >> extval_27_25_12_3_B2_output.txt
