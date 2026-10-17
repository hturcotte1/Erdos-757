#!/bin/bash
# Referee L013 round 1 -- every computation of results/reviews/L013-i11-on-C-n-le-26__referee__<UTC>.md
# Run from this directory. out/, logs/, bin/ are git-ignored. Nothing here imports e757, the judge, or the prover's programs;
# the prover's files are only READ as data (cells.tar.gz, L012 cells.tar.gz, worker cells) to be compared with.
set -e
cd /home/user/Erdos-757/experiments/referee/L013-round1
mkdir -p bin out logs out/inputs out/ext
P=/home/user/Erdos-757/experiments/prover/L013
# nauty 2.8.8 sources (unmodified, from the pynauty-2.8.8.1 sdist already on disk; sha256 454d3b0e...83f2)
mkdir -p out/nauty_src && tar xzf /home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1.tar.gz -C out/nauty_src
ND=out/nauty_src/pynauty-2.8.8.1/src/nauty2_8_8; (cd $ND && ./configure > /dev/null)
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -DMAXN1=30 -I$ND -o bin/genbg $ND/genbg.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
# genbg + documented PRUNE1 hook (tau-only bound; source unmodified)
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -DMAXN1=30 -DPRUNE1=prune_tau_only -I$ND -o bin/genbg_tprune $ND/genbg.c src/prune_tau_only.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O2 -Wall -o bin/hfilt src/hfilt.c; gcc -O2 -o bin/myext src/myext.c; gcc -O2 -o bin/myext2 src/myext2.c
# 0. data: the prover's tracked cell lists, L012's and the worker's
mkdir -p out/prover_cells out/l012cells out/w26cells
tar xzf $P/cells.tar.gz -C out/prover_cells; tar xzf /home/user/Erdos-757/experiments/prover/L012/cells.tar.gz -C out/l012cells
tar xzf /home/user/Erdos-757/experiments/20261017-1720-i11-n26/cells26.tar.gz -C out/w26cells
# 1. arithmetic (window, degree bounds, counting, records, Remark 3-5 numbers) and n=27 decomposition counts
python3 src/arith_ref.py > logs/arith_ref.txt
# 2. decompositions: own partition-first generator vs every recursion branch of the 167 cell files, with and without K8
python3 src/decomp_ref.py out/prover_cells/cells > logs/decomp_ref.txt
# 3. unit tests of the filter
python3 src/unit_tests.py > logs/unit_tests.txt
# 4. direct enumeration: unmodified genbg + own filter, all 91 D=2 cells and 28 D=3 cells; compare with VF2
ls out/prover_cells/cells | sed 's/cell_//;s/.txt//;s/D//' | tr '_' ' ' | sort -n -k4 -k1 -k2 -k3 > out/cell_keys.txt
awk '$4==2' out/cell_keys.txt > out/keys_D2.txt; ./src/run_genbg_cells.sh out/keys_D2.txt out/g2 900 > logs/genbg_D2.txt
python3 src/compare_cells.py out/g2 out/prover_cells/cells 400 > logs/compare_D2.txt
./src/run_genbg_cells.sh out/keys_D3_small.txt out/g3 300 > logs/genbg_D3.txt
./src/run_tprune_cells.sh out/keys_tp.txt out/g3 1500 > logs/tprune_D3.txt
./src/run_tprune_cells.sh out/keys_tp2.txt out/g3 1200 > logs/tprune_D3b.txt
python3 src/compare_cells.py out/g3 out/prover_cells/cells 20000 > logs/compare_D3.txt
# 5. own extension program: validation against brute force, then every top-level branch and the 5 residual cells
./src/run_validate.sh > logs/validate_myext.txt
for b in "23 14 9 2 8" "23 14 9 3 8" "23 20 10 3 9" "24 12 9 2 8" "24 13 9 2 8" "24 13 9 3 8" "24 18 10 3 9" "25 17 10 3 9" "25 22 11 3 10" "26 15 10 2 9" "26 15 10 3 9" "26 21 11 3 10" "23 13 9 2 8" "25 16 10 2 9" "26 14 10 2 9" "23 15 9 2 8" "23 15 9 3 8" "24 14 9 2 8" "24 14 9 3 8" "21 18 9 3 8" "24 19 10 3 9" "25 18 10 3 9"; do set -- $b
  python3 src/build_inputs.py out/prover_cells/cells $1 $2 $3 $4 $5 > out/inputs/in_$1_$2_$3_d$4.txt 2> out/inputs/in_$1_$2_$3_d$4.log; done
./src/run_top_ext.sh > logs/top_ext.txt; ./src/run_sub_ext.sh > logs/sub_ext.txt
./bin/myext2 20 9 3 3 < out/inputs/in_21_18_9_d3.txt | tail -1; ./bin/myext2 23 10 3 3 < out/inputs/in_24_19_10_d3.txt | tail -1
# 6. fully independent re-derivations from MY component lists (genbg+hfilt; counting-empty D=2 cells as empty files)
mkdir -p out/gmine; cp out/g2/*.txt out/g3/*.txt out/gmine/
for k in "7 5 2" "8 6 3" "9 7 3" "10 7 3" "10 7 4" "10 8 4" "11 8 4" "11 9 4" "12 10 5" "13 9 5" "13 10 5" "14 10 5" "15 11 6" "16 11 6"; do set -- $k; echo "SUMMARY empty by counting" > out/gmine/cell_$1_$2_$3_D2.txt; done
for b in "24 14 9 2 8 3" "24 14 9 3 8 3" "23 15 9 2 8 3" "23 15 9 3 8 3" "23 14 9 2 8 3" "23 14 9 3 8 3" "24 13 9 2 8 3" "24 13 9 3 8 3" "26 15 10 2 9 3" "26 15 10 3 9 3"; do set -- $b
  python3 src/build_inputs.py out/gmine $1 $2 $3 $4 $5 > out/inputs/mine_$1_$2_$3_d$4.txt; ./bin/myext2 $(($1-1)) $3 $4 $6 < out/inputs/mine_$1_$2_$3_d$4.txt | tail -1; done
# 7. one recursion level of non-empty recursion cells with the own extension program + VF2 reduction
python3 src/build_inputs.py out/prover_cells/cells 17 14 7 3 6 > out/inputs/in_17_14_7_d3.txt
./bin/myext2 16 7 3 3 < out/inputs/in_17_14_7_d3.txt > out/ext/rec_17_14_7_d3.txt; python3 src/iso_compare.py 17 out/ext/rec_17_14_7_d3.txt out/prover_cells/cells/cell_17_14_7_D3.txt
./src/run_rec.sh > logs/rec_check.txt
# 8. reproducibility: prover lists vs L012 and worker lists (exact FOUND-line sets)
python3 src/compare_lists.py > logs/compare_lists.txt
