#!/bin/bash
# (L016) checks of run F's cell(24,16,9,3) as soon as it exists (comparison with the worker, audit, closure)
cd /home/user/Erdos-757/experiments/prover/L016; W=../../20261017-2150-i11-n27
until grep -q "CELL (24, 16, 9, 3) classes" out/logs/engine_F.log; do sleep 10; done
python3 compare_cells16.py out/cellsF $W/out/cells <(echo 24,16,9,3) > out/compare_24_16_9_3.txt 2>&1
python3 compare_branches16.py $W/out/cells 24,16,9,3=out/cellsF >> out/compare_24_16_9_3.txt 2>&1
nice -n 10 timeout 1800 python3 filters16.py out/cellsF/cell_24_16_9_D3.txt 24 16 9 3 200 2416 > out/audit_F_24_16_9_3.txt 2>&1
nice -n 10 timeout 2400 python3 closure.py out/cellsF 24 16 9 3 all > out/closure_F_24_16_9_3.txt 2>&1
LIST=$PWD/out/worker_cell_25_19_10_D3.txt nice -n 10 timeout 2400 python3 closure.py out/cellsF 25 19 10 3 all > out/closure_worker_25_19_10_3.txt 2>&1
echo AFTER24_DONE >> out/compare_24_16_9_3.txt
