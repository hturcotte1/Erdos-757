#!/bin/bash
# (L016) post-checks after run F (each step under a timeout; outputs in the top directory or out/)
cd /home/user/Erdos-757/experiments/prover/L016; W=../../20261017-2150-i11-n27
H="24,16,9,3 25,19,10,3 26,22,11,3 27,25,12,3"
python3 top_info16.py out/cellsF $H > top_info_heavy_output.txt
for k in $H; do CELLDIR=$PWD/out/cellsF ENGINELOG=/dev/null python3 input_counts.py $PWD/out/cellsF $(echo $k | tr ',' ' '); done > input_counts_output.txt 2>&1
# comparison with the worker (lists and branch data) for all 49 new keys
cp listA.txt out/keys49.txt; for k in $H; do echo $k >> out/keys49.txt; done
mkdir -p out/mine49; for k in $(cat listA.txt); do f=cell_$(echo $k | awk -F, '{print $1"_"$2"_"$3"_D"$4}').txt; cp out/cells/$f out/mine49/; done
for k in $H; do f=cell_$(echo $k | awk -F, '{print $1"_"$2"_"$3"_D"$4}').txt; cp out/cellsF/$f out/mine49/; done
python3 compare_cells16.py out/mine49 $W/out/cells out/keys49.txt > compare_cells_output.txt
args=""; for k in $(cat out/keys49.txt); do args="$args $k=out/mine49"; done; python3 compare_branches16.py $W/out/cells $args > compare_branches_output.txt
# audits of the four heavy lists of run F
for k in 25,19,10,3 26,22,11,3 27,25,12,3; do set -- $(echo $k | tr ',' ' '); f=out/cellsF/cell_$1_$2_$3_D$4.txt; nice -n 5 timeout 1800 python3 filters16.py $f $1 $2 $3 $4 200 $1$2; done > audit_F_output.txt 2>&1
# closure checks of the three non-empty heavy lists
for k in 25,19,10,3 26,22,11,3; do nice -n 5 timeout 2400 python3 closure.py out/cellsF $(echo $k | tr ',' ' ') all; done > closure_F_output.txt 2>&1
# unpruned final step of the top cell
CELLDIR=$PWD/out/cellsF ENGINELOG=/dev/null nice -n 5 timeout 1800 python3 ext_validate.py 27 25 12 3 out/extval 2000 > extval_27_25_12_3_output.txt 2>&1
cat out/extval_27_1*.txt > extval_sparse_output.txt
echo POST_DONE
