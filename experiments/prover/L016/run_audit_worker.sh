#!/bin/bash
# (L016) audit (filters16.py) of the worker's stored lists of the heavy cells
cd /home/user/Erdos-757/experiments/prover/L016; W=../../20261017-2150-i11-n27
nice -n 10 python3 filters16.py out/worker_cell_25_19_10_D3.txt 25 19 10 3 200 2510 > out/audit_worker_25_19_10_3.txt 2>&1
nice -n 10 python3 filters16.py $W/out/cells/cell_24_16_9_D3.txt 24 16 9 3 200 2416 > out/audit_worker_24_16_9_3.txt 2>&1
nice -n 10 python3 filters16.py $W/out/cells/cell_26_22_11_D3.txt 26 22 11 3 36 2622 > out/audit_worker_26_22_11_3.txt 2>&1
