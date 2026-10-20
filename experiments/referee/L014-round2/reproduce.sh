#!/bin/bash
# Referee L014 round 2 -- commands used (scratch; large outputs in out/, git-ignored). Run from this directory.
set -e
# nauty 2.8.8 (unmodified, from the pynauty-2.8.8.1 sdist on PyPI, sha256 454d3b0e...83f2): genbg, genbgL, labelg
#   pip download pynauty==2.8.8.1 --no-deps --no-binary :all: -d out/dl; tar -xzf out/dl/pynauty-2.8.8.1.tar.gz -C out/src
#   (cd out/src/pynauty-2.8.8.1/src/nauty2_8_8 && ./configure && make genbg genbgL labelg); cp genbg genbgL labelg out/nbin/
gcc -O2 -o bin/myext src/myext.c; gcc -O2 -o bin/myext2 src/myext2.c; gcc -O2 -o bin/gfilt src/gfilt.c; gcc -O2 -o bin/gfilt2 src/gfilt.c; gcc -O2 -o bin/hg2g6 src/hg2g6.c
python3 arith_decomp.py --compare > arith_decomp_output.txt            # top branch arithmetic, decompositions (bf + dp, with/without K8) vs engine, 24 branches
python3 mytree.py > mytree_output.txt                                   # own dry run of the tree (no K8 guard)
python3 c23_check.py > c23_check_output.txt                             # witness C23
python3 test_myext.py myext > test_myext_output.txt; python3 test_myext.py myext2 > test_myext2_output.txt   # programs vs brute force
mkdir -p out/tracked && tar -xzf ../../prover/L014/cells.tar.gz -C out/tracked && zcat ../../prover/L014/cell_15_13_6_D3.txt.gz > out/tracked/cells/cell_15_13_6_D3.txt
(cd out/tracked && sha256sum -c ../../../../prover/L014/checksums_cells.txt)
python3 gen_my_inputs.py out/tracked/cells 23 21 10 3 3 9 out/final_inputs.txt              # 133,804 inputs
./bin/myext 9 10 3 2 1 < out/final_inputs.txt > out/final_hits.txt                         # (run in two halves: out/final_hits_00/01.txt)
python3 p3_certify.py out/final_hits_00.txt out/final_hits_01.txt 10 > p3_certify_final_output.txt
./verify_lists.sh > verify_lists_output.txt
./run_direct_all.sh > run_direct_all_output.txt                         # all 86 direct cells by genbg
python3 gen_my_inputs.py out/tracked/cells 21 18 9 3 3 8 out/in_21_18_9.txt; ./bin/myext 8 9 3 2 1 0 < out/in_21_18_9.txt > out/ext_21_18_9_hits.txt
python3 gen_my_inputs.py out/tracked/cells 19 17 8 3 3 7 out/in_19_17_8.txt; ./bin/myext 7 8 3 2 2 1 < out/in_19_17_8.txt > out/ext19.txt
python3 canon_cmp.py 19 17 <(grep '^MEMBER' out/ext19.txt) out/tracked/cells/cell_19_17_8_D3.txt
python3 gen_my_inputs.py out/tracked/cells 15 13 6 3 3 5 out/in_15_13_6.txt; ./bin/myext2 5 6 3 2 2 1 < out/in_15_13_6.txt > out/ext15.txt
./classes.sh 15 13 out/c_mine_15_13_6.txt out/ext15.txt; ./classes.sh 15 13 out/c_prov_15_13_6.txt out/tracked/cells/cell_15_13_6_D3.txt
./run_18_14_7.sh
python3 gen_my_inputs.py out/tracked/cells 22 18 9 3 3 8 out/in_22_18_9.txt; ./bin/myext2 8 9 3 2 2 1 < out/in_22_18_9.txt > out/ext22.txt
./classes.sh 22 18 out/c_mine_22_18_9.txt out/ext22.txt; ./classes.sh 22 18 out/c_prov_22_18_9.txt out/tracked/cells/cell_22_18_9_D3.txt
for k in "15 12 6 3" "17 13 7 3" "20 12 7 3" "21 15 8 3" "14 12 6 4"; do ./run_onelevel.sh $k; done
for c in "17 11 6 3" "20 11 7 3" "20 11 7 2" "20 12 7 2" "20 10 7 3"; do set -- $c; out/nbin/genbg -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) | ./bin/gfilt2 $1 $3 1 1 > out/g_$1_$2_$3_D$4.txt; done
MDIR=11 python3 myengine.py 21 18 9 3; python3 compare_mycells.py > compare_mycells_output.txt   # bottom-up, own lists only
python3 canon_cmp.py 23 21 out/tracked/cells/cell_23_21_10_D4.txt ../../prover/L012/route4_classes.txt.gz
