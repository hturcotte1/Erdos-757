#!/bin/bash
# Referee L016 round 2: commands in the order they were run (2026-10-21 01:22-03:15 UTC). One CPU-heavy process at a time.
set -e
R=/home/user/Erdos-757/experiments/referee/L016-round2; CF=/home/user/Erdos-757/experiments/prover/L016/out/cellsF; cd $R
# nauty 2.8.8 (unmodified) from the tarball of earlier referees; labelg, genbg; genbg30 with MAXN1=30; genbg30_prune with own PRUNE1
mkdir -p out/nauty && tar xzf ../L014-round3/out/nauty/nauty2_8_8.tar.gz -C out/nauty
(cd out/nauty/nauty2_8_8 && ./configure --disable-popcnt --disable-clz && make labelg genbg)
ND=$R/out/nauty/nauty2_8_8
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -DMAXN1=30 -I$ND -o out/nauty/genbg30 $ND/genbg.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O3 -w -DWORDSIZE=64 -DMAXN=WORDSIZE -DMAXN1=30 -DPRUNE1=rprune -I$ND -o bin/genbg30_prune $ND/genbg.c src/rprune.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O3 -march=native -w -o bin/rext src/rext.c; gcc -O2 -o bin/c27check src/c27check.c
python3 src/recompute.py 14 12 6 3 $CF; python3 src/recompute.py 19 16 8 3 $CF; python3 src/recompute.py 17 14 7 3 $CF     # R2
python3 src/recompute.py 24 16 9 3 $CF --save out/mine_24_16_9_3.g6 > out/recompute_24_16_9_3.txt                        # R13
python3 src/arith.py > out/arith_output.txt; (cd /home/user/Erdos-757 && python3 -m e757.fn_bounds) > out/fn_bounds_output.txt  # R3
(./bin/c27check 16 < out/c27.txt; echo "0 136 200 243 246 249 272 286 298 323 400 528 596 1056" | ./bin/c27check 8; echo "0 136 200 243 246 249 272 286 298 323 400 528 596" | ./bin/c27check 8) > out/c27check_output.txt  # R4
python3 src/seedcmp.py > out/seedcmp_output.txt                                                                          # R5
python3 src/regress_fast.py > out/regress_fast_output.txt                                                                # R6
echo "8 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23" > out/maxp_test.in                                 # R7: run the 3 builds with args 25 8 9 3 2
python3 src/verify_runA.py all > out/verify_runA_output.txt                                                              # R9
python3 src/genbg_cells.py $CF 600 18,11,6,2 19,11,6,2 20,13,7,2 21,12,7,2 22,12,7,2 23,14,8,2 24,12,8,2 27,13,10,2 > out/genbg_runA_tp_output.txt
python3 src/decomp_all.py > out/decomp_all_output.txt                                                                    # R8
python3 src/top27.py $CF > out/top27_output.txt                                                                          # R11
python3 src/filters.py $CF/cell_24_16_9_D3.txt $CF/cell_25_19_10_D3.txt $CF/cell_26_22_11_D3.txt $CF/cell_27_25_12_D3.txt $CF/cell_23_13_8_D3.txt > out/filters_output.txt  # R12
python3 src/closure.py $CF 26 22 11 > out/closure_26_22_11_3.txt                                                         # R16
python3 src/sparse_unpruned.py $CF > out/sparse_unpruned_output.txt                                                      # R10
python3 src/chunks25.py $CF > out/chunks25_output.txt                                                                    # R14
bash src/run_after.sh; bash src/run_after2.sh        # R15 (26,22,11,3), R16 closures, R17 pruned genbg (27,14,10,3)
bash src/run_gbp_more.sh                              # R17 pruned genbg (27,18,11,2), (27,19,11,3)
