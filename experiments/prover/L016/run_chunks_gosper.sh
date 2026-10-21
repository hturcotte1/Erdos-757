#!/bin/bash
# (L016) chunks 1, 40, 74 of the worker's cell(25,19,10,3) run recomputed with the Gosper build bin/ext_d (3 in parallel)
cd /home/user/Erdos-757/experiments/prover/L016
for c in 1 40 74; do nice -n 5 timeout 1500 python3 chunk_check.py out/regress/inputs_25_19_10_3_workerlists.txt out/wchunks/chunks/25_19_10_D3_d3_tp9 bin/ext_d $c > out/chunk_gosper_$c.txt 2>&1 & done
wait
cat out/chunk_gosper_1.txt out/chunk_gosper_40.txt out/chunk_gosper_74.txt > chunk_check_gosper_output.txt
