#!/bin/bash
# (L016) C8 chunk level: 8 random chunks (random.Random(20261021).sample(range(84), 8)) of the worker's cell(25,19,10,3) run, recomputed
# with ext_d_fast from the input list rebuilt by gen_inputs.py from the worker's cell(24,16,9,3) and the refereed lists (out/cellsW),
# compared with the worker's chunk files (counters and key sets); chunk 74 also with the Gosper build bin/ext_d.
cd /home/user/Erdos-757/experiments/prover/L016
nice -n 10 timeout 3600 python3 chunk_check.py out/regress/inputs_25_19_10_3_workerlists.txt out/wchunks/chunks/25_19_10_D3_d3_tp9 bin/ext_d_fast 1 29 40 48 49 51 69 74 > chunk_check_output.txt 2>&1
nice -n 10 timeout 3600 python3 chunk_check.py out/regress/inputs_25_19_10_3_workerlists.txt out/wchunks/chunks/25_19_10_D3_d3_tp9 bin/ext_d 74 > chunk_check_gosper_output.txt 2>&1
