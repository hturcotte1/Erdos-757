#!/bin/bash
# recompute every cell whose only source was the cost study / the d4 worker, from REFEREED seeds only (CELLDIR out/cells_ref2 = symlinks to the refereed lists; missing dependencies are recomputed in-process)
cd "$(dirname "$0")"
export CELLDIR=$PWD/out/cells_ref2 ENGINELOG=$PWD/out/engine_ref2.log WORKDIR=$PWD/out/work_ref PROGRESS_TSV=$PWD/progress_ref2.tsv NPROC=2 MD=10 SORTMEM=400M
echo -e "cell\tclasses\tinputs\tnodes\tseconds\tbad_tau\thits_in_C\troute\tutc" > progress_ref2.tsv
for k in $(cat ref2_keys.txt); do nice -n 5 timeout 10800 python3 src/run1.py $k >> out/run_ref2.log 2>&1; done
