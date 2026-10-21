#!/bin/bash
# (L016) C5: audit (filters16.py) of every new list used: run A's 45 lists, run F's cell(24,16,9,3), run B2's two lists, the worker's
# cell(25,19,10,3) (and run F's heavy lists when they exist)
cd /home/user/Erdos-757/experiments/prover/L016
{
for k in $(cat listA.txt); do set -- $(echo $k | tr ',' ' '); nice -n 10 timeout 600 python3 filters16.py out/cells/cell_$1_$2_$3_D$4.txt $1 $2 $3 $4 50 1; done
nice -n 10 timeout 900 python3 filters16.py out/cellsF/cell_24_16_9_D3.txt 24 16 9 3 200 2416
nice -n 10 timeout 900 python3 filters16.py out/cellsB/cell_26_22_11_D3.txt 26 22 11 3 36 2622
nice -n 10 timeout 900 python3 filters16.py out/cellsB/cell_27_25_12_D3.txt 27 25 12 3 0 2725
nice -n 10 timeout 900 python3 filters16.py out/worker_cell_25_19_10_D3.txt 25 19 10 3 200 2510
for k in 25,19,10,3 26,22,11,3 27,25,12,3; do set -- $(echo $k | tr ',' ' '); f=out/cellsF/cell_$1_$2_$3_D$4.txt; [ -e $f ] && nice -n 10 timeout 900 python3 filters16.py $f $1 $2 $3 $4 200 $1$2; done
} > audit_output.txt 2>&1
echo AUDIT_ALL_DONE >> audit_output.txt
