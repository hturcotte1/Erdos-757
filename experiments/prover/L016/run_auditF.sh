#!/bin/bash
# (L016) audit and closure of run F's own heavy lists (after run F)
cd /home/user/Erdos-757/experiments/prover/L016
for k in 25,19,10,3 26,22,11,3 27,25,12,3; do set -- $(echo $k | tr ',' ' '); nice -n 5 timeout 900 python3 filters16.py out/cellsF/cell_$1_$2_$3_D$4.txt $1 $2 $3 $4 200 $1$2; done > audit_F_output.txt 2>&1
for k in 25,19,10,3 26,22,11,3; do nice -n 5 timeout 900 python3 closure.py out/cellsF $(echo $k | tr ',' ' ') all; done > closure_F_output.txt 2>&1
echo AUDITF_DONE >> closure_F_output.txt
