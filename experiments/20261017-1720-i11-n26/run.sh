#!/bin/bash
# Exact commands for experiments/20261017-1720-i11-n26 (run from this directory). NPROC=2, nice 19, 60 min cap per top-level cell.
# Seeding: out/cells <- ../20261017-1645-i11-n23-n24/out/cells (125) + cells25.tar.gz (150 files, superset) => 150 seeded cell files.
set -e
cd "$(dirname "$0")"; mkdir -p out/cells
S=../20261017-1645-i11-n23-n24
for f in engine.py decomp22.py; do cp $S/$f .; diff $S/$f $f; done      # byte-identical (no output = identical)
[ -e bin ] || ln -s ../prover/L012/bin bin
if [ ! -e seed_cells.txt ]; then
  cp $S/out/cells/* out/cells/; mkdir -p tmpx; tar xzf $S/cells25.tar.gz -C tmpx; cp --update=none tmpx/cells25/* out/cells/; rm -r tmpx
  ls out/cells > seed_cells.txt
fi
python3 arith.py > arith_output.txt                          # step 1 (n = 26, 27)
python3 step2_decomps.py 26 > step2_n26_output.txt           # step 2: decompositions / component cell types
python3 step2_decomps.py 27 > step3_n27_output.txt           # step 3: n = 27 arithmetic (no engine run)
python3 step3_n27_q14.py > step3_q14_output.txt              # step 3: is [(23,21,10),(3,1,1)] a decomposition of (26,22) slack 1?
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log NPROC=2 RESJSONL=results_cells.jsonl
nice -n 19 timeout 3600 python3 run_cells.py 26 14 10 2 > out/run_26_14_10.log 2>&1
nice -n 19 timeout 3600 python3 run_cells.py 26 15 10 3 > out/run_26_15_10.log 2>&1
nice -n 19 timeout 3600 python3 run_cells.py 26 21 11 3 > out/run_26_21_11.log 2>&1
python3 collect_new.py                                       # cells_table.tsv (new cells only), results.json
