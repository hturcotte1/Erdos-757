#!/bin/bash
# Referee L014 round 1 -- every computation of results/reviews/L014-f23-equals-14__referee__<UTC>.md
# (run from anywhere; large files in out/, logs in logs/, binaries in bin/: all git-ignored). About 2-3 CPU-hours.
set -e
cd /home/user/Erdos-757/experiments/referee/L014-round1
mkdir -p bin out/dl out/nauty_src out/pcells logs
# nauty 2.8.8, unmodified, from the official site; genbg, genbgL, labelg built with its own configure/make
curl -sS -L -o out/dl/nauty2_8_8.tar.gz https://users.cecs.anu.edu.au/~bdm/nauty/nauty2_8_8.tar.gz   # sha256 159d2156810a6bb240410cd61eb641add85088d9f15c888cdaa37b8681f929ce
tar xzf out/dl/nauty2_8_8.tar.gz -C out/nauty_src
(cd out/nauty_src/nauty2_8_8 && ./configure --disable-popcnt --disable-clz && make genbg genbgL labelg)
cp out/nauty_src/nauty2_8_8/{genbg,genbgL,labelg} bin/
# own programs
gcc -O2 -Wall -o bin/myext src/myext.c; gcc -O2 -Wall -o bin/myext2 src/myext2.c; gcc -O2 -Wall -o bin/gfilt src/gfilt.c; gcc -O2 -o bin/hg2g6 src/hg2g6.c
# the prover's cell lists (tracked copies), checked against its SHA-256 list
tar xzf ../../prover/L014/cells.tar.gz -C out/pcells; zcat ../../prover/L014/cell_15_13_6_D3.txt.gz > out/pcells/cells/cell_15_13_6_D3.txt
(cd out/pcells && sha256sum -c ../../../../prover/L014/checksums_cells.txt | grep -c ': OK$')
awk '{print $2,$3,$4,$5,$6}' ../../prover/L014/tree_23_21_10_3.txt | tr -d '(),' | awk 'NF>=5{printf "%s,%s,%s,%s %s\n",$1,$2,$3,$4,$5}' | grep -v nontrivial > out/tree_keys.txt
# 1. decompositions of every recursion branch (own brute force) vs the INFO lines; INFO counter audit; certificate table
python3 src/decomp_bf.py out/pcells/cells out/tree_keys.txt > logs/decomp_bf.txt
python3 src/info_audit.py out/pcells/cells > logs/info_audit.txt
python3 src/my_tree.py out/tree_keys.txt > logs/my_tree.txt
# 2. the final step: own inputs, own exhaustive re-insertion (myext: all disjoint triples, no pruning), own classifier with witnesses
python3 src/build_top_inputs.py out/pcells/cells > out/top_inputs.txt 2> logs/build_top_inputs.txt
./bin/myext 22 10 3 2 < out/top_inputs.txt > out/top_hits.txt; tail -2 out/top_hits.txt
python3 src/classify.py 23 out/top_hits.txt out/top_members.txt
./bin/myext2 22 10 3 2 < out/top_inputs.txt | tail -1
python3 src/sat_final_sample.py out/top_inputs.txt out/top_hits.txt 14 > logs/sat_final_sample.txt
# 3. explicit set C23 (own exact check; judge on a scratch copy)
python3 src/c23_check.py > logs/c23_check.txt
(cd /home/user/Erdos-757 && python3 judge/judge.py experiments/referee/L014-round1/out/C23-referee-temp.json)
# 4. genbg (unmodified) + own filter for all 86 direct cells of the tree and 10 recursion cells; labelg class-set comparison
for c in "14 10 5 3" "13 10 5 3" "14 12 6 3" "11 9 4 3"; do ./src/run_genbg.sh $c 1800; done
./src/all_direct.sh
for p in 0 1; do ./src/run_genbg_part.sh ./bin/genbg 20 12 7 3 $p 2 7200; done; cat out/gp_20_12_7_D3_[01]_2.txt | grep '^FOUND' > out/g_20_12_7_D3.txt
./src/cmp_classes.sh 20 out/g_20_12_7_D3.txt out/pcells/cells/cell_20_12_7_D3.txt
./bin/genbg -q -c -Z1 -d1:3 -D3:3 20 11 33:33 | ./bin/gfilt 20 11 7 3 > out/g_20_11_7_D3.txt; ./src/cmp_classes.sh 20 out/g_20_11_7_D3.txt out/pcells/cells/cell_20_11_7_D3.txt
./src/rec_cells_genbg.sh
# 5. own one-level recomputation of every recursion cell from the prover's lower lists (own decompositions, builder, myext2, labelg)
for c in "19 17 8 3" "22 18 9 3" "21 15 8 3" "18 14 7 3" "15 13 6 3" "15 12 6 3" "16 11 6 3" "17 11 6 3" "17 13 7 3" "18 12 7 3" "19 12 7 3" "20 12 7 3" "15 11 6 3" "14 12 6 3" "17 14 7 3" "21 18 9 3" "23 21 10 4"; do ./src/myrec2.sh $c 2; done
# 6. control: the run's cell(23,21,10,4) vs L012's 699 classes
zcat ../../prover/L012/route4_classes.txt.gz > out/l012_route4_699.txt; ./src/cmp_classes.sh 23 out/l012_route4_699.txt out/pcells/cells/cell_23_21_10_D4.txt
