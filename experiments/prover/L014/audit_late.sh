#!/bin/bash
# (L014) soundness audit of the last lists (batch 6, seed 19): (22,18,9,3) with 500 random representatives, then (23,21,10,4) with 200.
cd /home/user/Erdos-757/experiments/prover/L014
done_cell() { grep -q '^INFO ' out/cells/cell_$1.txt 2>/dev/null; }
until done_cell 22_18_9_D3; do sleep 15; done
mkdir -p out/audit6a out/audit6b; cp out/cells/cell_22_18_9_D3.txt out/audit6a/
nice -n 10 python3 audit_sample.py out/audit6a 500 19 > out/audit6a_output.txt 2>&1
until done_cell 23_21_10_D4; do sleep 15; done
cp out/cells/cell_23_21_10_D4.txt out/cells/cell_23_21_10_D3.txt out/audit6b/
nice -n 10 python3 audit_sample.py out/audit6b 200 19 > out/audit6b_output.txt 2>&1
cat out/audit6a_output.txt out/audit6b_output.txt > out/audit6_output.txt
