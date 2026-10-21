#!/bin/bash
# (L016) post-checks after run F (light version used at submission time): branch data, input counts, comparison of all 49 new lists
# with the worker's, the unpruned final step of the top cell from run F's lists.  (The audit and closure of run F's lists are not
# repeated: run F's lists are identical, as sets of canonical forms, to the lists audited and closure-checked in C5.)
cd /home/user/Erdos-757/experiments/prover/L016; W=../../20261017-2150-i11-n27
H="24,16,9,3 25,19,10,3 26,22,11,3 27,25,12,3"
python3 top_info16.py out/cellsF $H > top_info_heavy_output.txt
for k in $H; do CELLDIR=$PWD/out/cellsF ENGINELOG=/dev/null python3 input_counts.py $PWD/out/cellsF $(echo $k | tr ',' ' '); done > input_counts_output.txt 2>&1
cp listA.txt out/keys49.txt; for k in $H; do echo $k >> out/keys49.txt; done
mkdir -p out/mine49; for k in $(cat listA.txt); do f=cell_$(echo $k | awk -F, '{print $1"_"$2"_"$3"_D"$4}').txt; cp out/cells/$f out/mine49/; done
for k in $H; do f=cell_$(echo $k | awk -F, '{print $1"_"$2"_"$3"_D"$4}').txt; cp out/cellsF/$f out/mine49/; done
python3 compare_cells16.py out/mine49 $W/out/cells out/keys49.txt > compare_cells_output.txt
args=""; for k in $(cat out/keys49.txt); do args="$args $k=out/mine49"; done; python3 compare_branches16.py $W/out/cells $args > compare_branches_output.txt
printf "26,22,11,3\n27,25,12,3\n" > out/keysFB.txt; python3 compare_cells16.py out/cellsF out/cellsB out/keysFB.txt > compare_F_B2_output.txt
CELLDIR=$PWD/out/cellsF ENGINELOG=/dev/null nice -n 5 timeout 900 python3 ext_validate.py 27 25 12 3 out/extval 2000 > extval_27_25_12_3_output.txt 2>&1
echo POST_DONE >> compare_cells_output.txt
