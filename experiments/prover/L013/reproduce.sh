#!/bin/bash
# Reproduction of every computation cited in results/proofs/L013-i11-on-C-n-le-26.md (run from this directory; about 1 CPU-hour for
# the main run plus about 1 CPU-hour of cross-checks on a 4-core machine; NPROC=2, nice 19).  Large files go to out/ (git-ignored).
# Inputs from earlier certificates: the C sources of L012 (experiments/prover/L012/indep/, unchanged), engine.py and decomp22.py of L012
# (byte-identical copies here), nauty 2.8.8 sources (unmodified, the referee's download folder), L012's cells.tar.gz and abase_pattern.txt
# and the L004 census file (comparisons and controls only), the worker's cell directories (comparison only).
set -e
cd "$(dirname "$0")"
ND=/home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; NB=/home/user/Erdos-757/experiments/referee/L010-round1/out/nauty_build
S=../L012/indep; W1=../../20261017-1645-i11-n23-n24; W2=../../20261017-1720-i11-n26
mkdir -p bin out/cells out/cells_D4 out/cells_dummy
# --- C2: build the L012 programs from source and compare with ../L012/bin (all six byte-identical); the engine files are byte-identical copies
gcc -O2 -Wall -o bin/enum_conn $S/enum_conn.c; gcc -O2 -Wall -o bin/filt $S/filt.c; gcc -O2 -Wall -o bin/ext_d $S/ext_d.c
gcc -O2 -Wall -o bin/realize $S/realize.c; gcc -O2 -Wall -o bin/realize_extra $S/realize_extra.c
gcc -O2 -DWORDSIZE=64 -DMAXN=64 -I$NB -I$ND -o bin/canon $S/canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
for b in enum_conn filt ext_d realize realize_extra canon; do cmp bin/$b ../L012/bin/$b && echo "$b identical to ../L012/bin/$b"; done > build_check_output.txt
cp ../L012/engine.py ../L012/decomp22.py . ; diff engine.py ../L012/engine.py; diff decomp22.py ../L012/decomp22.py; diff ../L012/indep/enum_conn.c ../L007/indep/enum_conn.c
sha256sum bin/* engine.py decomp22.py ../L012/indep/*.c >> build_check_output.txt
# --- C1: arithmetic (window cells, degree bounds, counting, record cells, lower bounds) and the n = 27 remark
python3 arith13.py > arith13_output.txt
python3 n27_remark.py > n27_remark_output.txt
# --- C3: the main run (fresh cell directory), top-level cells in induction order n = 23, 24, 25, then 26
rm -rf out/cells/* out/engine.log top_results.jsonl
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log NPROC=2 MD=10 TOPJSONL=$PWD/top_results.jsonl
nice -n 19 timeout 10800 python3 run_top.py 23 13 9 2 23 14 9 3 23 20 10 3 24 12 9 2 24 13 9 3 24 18 10 3 25 16 10 2 25 17 10 3 25 22 11 3 > out/run_top_n23_25.log 2>&1
nice -n 19 timeout 7200 python3 run_top.py 26 14 10 2 26 15 10 3 26 21 11 3 > out/run_top_n26.log 2>&1
unset CELLDIR ENGINELOG TOPJSONL
T='23 13 9 2 23 14 9 3 23 20 10 3 24 12 9 2 24 13 9 3 24 18 10 3 25 16 10 2 25 17 10 3 25 22 11 3 26 14 10 2 26 15 10 3 26 21 11 3'
python3 top_table.py out/cells $T > top_table_output.txt; python3 top_types.py out/cells $T > top_types_output.txt
# --- C4: independent audit of every cell file (pure Python re-verification, branch sets, decompositions by two generators, products, ext_d counters)
python3 verifier_unit_tests.py > verifier_unit_tests_output.txt; python3 canon_fixed_points.py out/cells > canon_fixed_points_output.txt
nice -n 19 python3 check_cells.py out/cells 10 > check_cells_output.txt
python3 cells_summary.py out/cells > cells_summary_output.txt
# --- C5/C10: known counts, comparisons with L012's cell lists and the worker's runs (representative sets and branch counters), arithmetic comparison
mkdir -p out/l012cells out/w25 out/w26; tar xzf ../L012/cells.tar.gz -C out/l012cells; tar xzf $W1/cells25.tar.gz -C out/w25; tar xzf $W2/cells26.tar.gz -C out/w26
for k in 12_10_5_D3 10_7_4_D3 22_17_9_D3 19_16_8_D3; do echo "cell($k): mine $(grep -c '^FOUND' out/cells/cell_$k.txt), L012 $(grep -c '^FOUND' out/l012cells/cells/cell_$k.txt)"; done > known_counts_output.txt || true
python3 compare_arith.py > compare_arith_output.txt
python3 compare_runs.py out/cells L012=out/l012cells/cells W2324=$W1/out/cells W25=out/w25/cells25 W26=$W2/out/cells tsv:W2324table=$W1/cells_table.tsv > compare_runs_output.txt
# --- C6: direct enumeration of recursion cells (MD = 99, fresh directories); then load_bearing.py (which load-bearing lists rest on the recursion only)
rm -f crosscheck_direct.jsonl; bash run_crosscheck1.sh; bash run_crosscheck2.sh; bash run_crosscheck2b.sh; bash run_crosscheck2c.sh; bash run_crosscheck3.sh; bash run_crosscheck4.sh; bash run_crosscheck5.sh; bash run_crosscheck6.sh
python3 load_bearing.py > load_bearing_output.txt
# --- C7: re-validation of the final extension steps (noprune + pure-Python filter on all inputs; brute force on 3 sampled inputs per branch)
bash run_ext_validate.sh
# --- C8: positive controls (A_base and the 2,910 census patterns in cell(14,12,6,4); random members of C in recursion cells)
rm -rf out/cells_D4/* out/engine_D4.log top_results_D4.jsonl; CELLDIR=$PWD/out/cells_D4 ENGINELOG=$PWD/out/engine_D4.log NPROC=1 TOPJSONL=$PWD/top_results_D4.jsonl python3 run_top.py 14 12 6 4 > out/run_D4.log 2>&1
python3 check_cells.py out/cells_D4 10 > check_cells_D4_output.txt; python3 abase_control.py > abase_control_output.txt
rm -f positive_control.jsonl; bash run_positive.sh; bash run_positive2.sh
# --- tracked copy of the cell lists
tar czf cells.tar.gz -C out cells
