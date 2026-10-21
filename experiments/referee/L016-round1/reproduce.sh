#!/bin/bash
# Referee L016 round 1 -- every computation of results/reviews/L016-i11-n27-f27-equals-16__referee__*.md (round 1).
# Own code in src/ (written for this review); unmodified nauty 2.8.8 (pynauty-2.8.8.1 sdist, sha256 454d3b0e...83f2) for genbg
# (built with -DMAXN1=30) and labelg; large files in out/ (git-ignored); summaries copied to logs/.
# Run from this directory, one process at a time (nice -n 10, timeouts).
set -e
R=/home/user/Erdos-757/experiments/referee/L016-round1; cd $R; mkdir -p bin out logs out/seeds/L013 out/seeds/L014 out/new
P=/home/user/Erdos-757/experiments/prover; W=/home/user/Erdos-757/experiments/20261017-2150-i11-n27
# 0. builds
mkdir -p out/nauty && tar xzf /home/user/Erdos-757/experiments/referee/L010-round1/out/dl/pynauty-2.8.8.1.tar.gz -C out/nauty
(cd out/nauty/pynauty-2.8.8.1/src/nauty2_8_8 && ./configure --disable-popcnt --disable-clz && make labelg geng && \
  gcc -O3 -w -DMAXN1=30 -DWORDSIZE=64 -DMAXN=WORDSIZE -I. -o $R/bin/genbg30 genbg.c gtools.c nauty.c nautil.c naugraph.c schreier.c naurng.c && cp labelg geng $R/bin/)
for p in myext myext2 g6filt listfilt mytau; do gcc -O2 -Wall -o bin/$p src/$p.c; done
# 1. data: refereed seeds (L013, L014) and the prover's new lists (cells_new.tar.gz)
tar xzf $P/L013/cells.tar.gz -C out/seeds/L013; tar xzf $P/L014/cells.tar.gz -C out/seeds/L014; zcat $P/L014/cell_15_13_6_D3.txt.gz > out/seeds/L014/cell_15_13_6_D3.txt
tar xzf $P/L016/cells_new.tar.gz -C out/new
# 2. validation of my extension program against a Python brute force (small random inputs)
python3 src/bf_validate.py ./bin/myext 400 7; python3 src/bf_validate2.py ./bin/myext2 300 11 same; python3 src/bf_validate2.py ./bin/myext2 200 12
# 3. decompositions (own brute force, with and without K8)
python3 src/mydecomp.py 25 19 10; python3 src/mydecomp.py 26 22 11
# 4. cell(26,22,11,3) one level, and the top cell (27,25,12,3)
python3 src/build_inputs.py 25 19 10 3 out/in_26_22_11.txt
./bin/myext 25 10 3 2 3 < out/in_26_22_11.txt > out/my_26_22_11.out
F26=$(python3 -c "print('a'*26)")
grep '^X:' out/my_26_22_11.out | python3 src/hg2g6.py 26 | ./bin/labelg -q -f$F26 | LC_ALL=C sort -u > out/mine_26_22_11.g6
grep '^FOUND' out/new/cells_new/runF/cell_26_22_11_D3.txt | python3 src/hg2g6.py 26 | ./bin/labelg -q -f$F26 | LC_ALL=C sort -u > out/prov_26_22_11.g6
cmp out/mine_26_22_11.g6 out/prov_26_22_11.g6
python3 src/build_inputs.py 26 22 11 3 out/in_27_25_12.txt; ./bin/myext 26 11 3 2 3 all < out/in_27_25_12.txt > out/my_27_25_12_all.out
# 5. sparse top cells: genbg directly (Delta <= 2) and one level from the lists
./bin/genbg30 -q -c -Z1 -d1:3 -D2:3 27 13 39:39 | ./bin/g6filt 27 13 10 2 > out/gf_27_13_10_2.txt
./bin/genbg30 -c -Z1 -d2:3 -D2:3 27 18 54:54 > out/g_27_18_D2.g6; ./bin/g6filt 27 18 11 2 < out/g_27_18_D2.g6 > out/gf_27_18_11_2.txt
timeout 1200 ./bin/genbg30 -c -Z1 -d1:3 -D3:3 27 14 42:42 2> out/g_27_14_D3.log | ./bin/g6filt 27 14 10 3 > out/gf_27_14_10_3.txt   # direct attempt (time-limited)
for b in "26 11 9 2 27_13_10_2_d2" "26 12 9 2 27_14_10_3_d2" "26 11 9 3 27_14_10_3_d3" "26 16 10 2 27_18_11_2_d2" "26 16 10 3 27_19_11_3_d3"; do set -- $b; python3 src/build_inputs.py $1 $2 $3 $4 out/in_$5.txt; done
for b in "27_13_10_2_d2 9 2 1 2" "27_14_10_3_d2 9 2 1 2" "27_14_10_3_d3 9 3 2 3" "27_19_11_3_d3 10 3 2 3"; do set -- $b; ./bin/myext 26 $2 $3 $4 $5 all < out/in_$1.txt > out/my_$1.out; done
# 6. the 45 run-A lists: 40 max-degree-2 lists by genbg (27,13 and 27,18 above), 5 max-degree-3 lists one level
./src/run_genbg_D2.sh out/runA_D2_keys_b.txt > out/genbg_D2_result.txt
mkdir -p out/onelevel; for k in "25 13 9 3" "26 16 10 3" "23 13 8 3"; do set -- $k; python3 src/onelevel.py $1 $2 $3 $4 out/onelevel/c_$1_$2_$3_$4; done > logs/onelevel_runA_D3.txt
# 7. cell(24,16,9,3) and cell(25,19,10,3) in full (one level each), and 7 chunks of the worker's cell(25,19,10,3) run
python3 src/build_inputs.py 23 14 8 2 out/in_24_16_9_d2.txt; python3 src/build_inputs.py 23 13 8 3 out/in_24_16_9_d3.txt
./src/run_24_16_9.sh > out/result_24_16_9.txt
zcat $W/cell_24_16_9_D3.txt.gz > out/wcell_24_16_9_D3.txt; mkdir -p out/chunks out/wchunks; tar xzf $W/chunks_25_19_10_d3_tp9.tar.gz -C out/wchunks
python3 src/build_chunks.py $W/cell_25_19_10_D3.txt.gz out/wcell_24_16_9_D3.txt 0,34,44,45,54,61,83 out/chunks
./src/run_chunks.sh 0 34 44 45 54 61 83 > out/chunks_result.txt
./src/run_25_19_10_full.sh > out/result_25_19_10_full.txt
# 8. filters and closure
for k in "24 16 9 3" "25 19 10 3" "26 22 11 3" "27 25 12 3"; do set -- $k; ./bin/listfilt $1 $2 $3 $4 < out/new/cells_new/runF/cell_$1_$2_$3_D$4.txt; done
python3 src/closure.py 26 22 11 3 out/new/cells_new/runF/cell_26_22_11_D3.txt out; python3 src/closure.py 25 19 10 3 out/new/cells_new/runF/cell_25_19_10_D3.txt out
# 9. regressions ext_d_fast vs the Gosper builds (file-based samples; random graphs: see the seeds in run_regress.sh)
./src/run_regress.sh > out/regress_result.txt
# 10. C27, A_base, B13; fn_bounds
python3 src/c27_check.py; (cd /home/user/Erdos-757 && python3 -m e757.fn_bounds | grep -E "^n=2[3-9]|^n=30")
