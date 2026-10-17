#!/bin/bash
# Referee round 2 for L012 (results/proofs/L012-n23-record-no-degree-4.md).  All programs in src/ are the referee's own.
# Inputs read (never modified): experiments/prover/L012/route4_classes.txt.gz, cells.tar.gz, out/route{4,20}_inputs.txt,
# out/realize_r4_part0{0,1}.txt (comparison only), bin/canon (tested only); data/census_n14_m12_classes.jsonl.gz;
# experiments/20261014-1005-census-dfs/results/realized_n12.json.gz; nauty 2.8.8 sources (unmodified, for genbg).
# Large files go to out/ and logs/ (git-ignored).  nice 5, at most 2 processes.
set -e
cd /home/user/Erdos-757/experiments/referee/L012-round2
P=/home/user/Erdos-757/experiments/prover/L012
ND=/home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; NB=/home/user/Erdos-757/experiments/referee/L010-round1/out/nauty_build
mkdir -p out logs out/cells_x
gcc -O2 -w -o out/rz src/rz.c -lm; gcc -O2 -w -DDUMP -o out/rz_dump src/rz_dump.c -lm
gcc -O2 -w -o out/xr src/xr.c; gcc -O2 -w -o out/fr src/fr.c
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -I$NB -I$ND -o out/genbg $ND/genbg.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
tar xzf $P/cells.tar.gz -C out/cells_x; zcat $P/route4_classes.txt.gz > out/r4_699.txt
# 1. arithmetic, degree bounds, decompositions (no HY) vs every recorded branch
python3 src/arith_bf.py > logs/arith_bf.out
# 2. realization: A_base control, the 699 (float+verify and exact Bareiss), census controls, Python Fraction cross-check, n=23 controls
python3 src/abase_ctrl.py
nice -n 5 ./out/rz 23 < out/r4_699.txt > out/rz_699_f.txt; nice -n 5 ./out/rz 23 e < out/r4_699.txt > out/rz_699_e.txt
python3 src/census_ctrl.py 14; python3 src/census_ctrl.py 12; python3 src/census14_twosided.py
for i in 698 0 350; do python3 src/py_solve_check.py $i; done
python3 src/grow23_ctrl.py
# 3. validation of xr and fr against brute force
python3 src/bf_xr.py; python3 src/bf_fr.py; python3 src/bf_fr_dense.py
# 4. routes 4 and 20 from the cell lists (inputs rebuilt and compared with the prover's), BLISS classes with explicit maps
python3 src/build_routes.py 4; python3 src/build_routes.py 20
nice -n 5 ./out/xr 22 4 3 10 < out/route4_in.txt 2> logs/r4_xr.err | nice -n 5 ./out/fr 23 print > out/r4_surv.txt
sed 's/^SURV[^:]*: //' out/r4_surv.txt | grep '^HIT' > out/r4_surv_hits.txt
python3 src/bliss_classify.py 23 out/r4_699.txt out/r4_surv_hits.txt
nice -n 5 ./out/xr 22 3 2 10 < out/route20_in.txt 2> logs/r20_xr.err | nice -n 5 ./out/fr 23 print > out/r20_surv.txt
# (optional, stopped after 3,227 graphs in the review run) direct realization test of the labelled survivors
# nice -n 5 ./out/rz 23 < out/r4_surv_hits.txt > out/rz_r4_surv.txt
# 5. the engine: top level of all 25 recursive cells from the lower lists; all 94 direct cells by genbg
python3 - << 'PY'
import json, glob, os
rec = []
for fn in sorted(glob.glob('out/cells_x/cells/cell_*.txt')):
    key = tuple(int(x) for x in os.path.basename(fn)[5:-4].replace('D', '').split('_'))
    info = [json.loads(l[5:]) for l in open(fn) if l.startswith('INFO ')][0]
    if info['route'] == 'recurse': rec.append((sum(b.get('inputs', 0) for b in info['branches']), key))
open('out/rec_cells.txt', 'w').write(''.join('%d %d %d %d\n' % k for i, k in sorted(rec)))
PY
./src/run_all_rec.sh > logs/run_all_rec.log 2>&1
python3 src/genbg_check.py 120 > logs/genbg_all.log 2>&1
# 6. the prover's canon: relabelling invariance and faithfulness; degree statistics of the 699
python3 src/canon_check.py
