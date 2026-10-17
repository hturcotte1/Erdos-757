#!/bin/bash
# Referee L009 round 3: every command of the review, from scratch. Large outputs under out/ (git-ignored).
# nauty 2.8.8 tree (built by referee L009 round 1): experiments/referee/L009-round1/out/nauty (genbg.c, labelg, *.c).
set -e
cd /home/user/Erdos-757/experiments/referee/L009-round3
ND=/home/user/Erdos-757/experiments/referee/L009-round1/out/nauty; P=/home/user/Erdos-757/experiments/prover/L009
mkdir -p bin out/val out/cells out/cmp out/flags out/final logs prover_copy/indep
# --- build (my programs; the prover's sources recompiled in prover_copy/)
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=64 -DPRUNE1=myprune -DOUTPROC=myout -DSUMMARY=mysummary -I$ND -o bin/genbg_my $ND/genbg.c src/myhook.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O2 -o bin/bf src/bf.c; gcc -O2 -o bin/myext src/myext.c; cp $ND/labelg bin/labelg
cp $P/*.py $P/reproduce.sh $P/checksums_large_outputs.txt prover_copy/; cp $P/indep/*.c prover_copy/indep/
(cd prover_copy/indep && gcc -O2 -o enum_conn enum_conn.c && gcc -O2 -o ext_indep2 ext_indep2.c && gcc -O2 -o ext_indep3 ext_indep3.c && gcc -O2 -o filter_hits filter_hits.c)
# --- A. arithmetic
python3 src/cells.py > logs/cells.log
# --- C. brute-force validation of my genbg hook and the prover's enum_conn (small cells)
./src/validate_small.sh > logs/validate_small.log
# --- D. my genbg enumerations (component cells, empty cells, (17,12,7), (14,12,6)); (17,13,7) in two parts (about 9 CPU-min each)
./src/run_cells.sh > logs/run_cells.log
for c in "16 9 6 9" "18 10 7 10" "13 8 5 8"; do set -- $c; TAU0=$3 ./bin/genbg_my -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) > out/cells/g_$1_$2_$3_D$4.txt 2> out/cells/g_$1_$2_$3_D$4.err; done
for r in 0 1; do TAU0=7 ./bin/genbg_my -q -c -Z1 -d1:3 -D3:3 -X-3 17 13 39:39 $r/2 > out/direct_17_13_7_part$r.txt 2> logs/direct_17_13_7_part$r.err; done
cat out/direct_17_13_7_part0.txt out/direct_17_13_7_part1.txt | grep "^G " > out/direct_17_13_7_all.txt
# class-set comparisons (nauty canonical forms of the incidence graphs)
for c in "6 3 2" "8 5 3" "10 7 4" "10 8 4" "13 8 5" "13 9 5" "16 10 6"; do set -- $c; tag=$1_$2_$3
  grep "^G " out/cells/g_${tag}_D3.txt | ./src/classes.sh $1 G > out/cmp/my_$tag.cls
  f=$P/indep/cell_$tag.txt; if [ -f $f ]; then cat $f; else zcat $f.gz; fi | ./src/classes.sh $1 FOUND > out/cmp/pr_$tag.cls; cmp out/cmp/my_$tag.cls out/cmp/pr_$tag.cls && echo "($tag) identical"; done
grep "C=1" out/cells/g_14_12_6_D3.txt | ./src/classes.sh 14 G > out/cmp/myC_14_12_6.cls; ./src/classes.sh 14 FOUND < $P/indep/T14_conn.txt > out/cmp/prT14.cls; cmp out/cmp/myC_14_12_6.cls out/cmp/prT14.cls && echo "T14 identical"
grep "C=1" out/direct_17_13_7_all.txt | ./src/classes.sh 17 G > out/cmp/myC_17_13_7.cls; zcat $P/indep/T17_conn.txt.gz | ./src/classes.sh 17 FOUND > out/cmp/prT17.cls; cmp out/cmp/myC_17_13_7.cls out/cmp/prT17.cls && echo "T17 identical"
./src/classes.sh 17 G < out/direct_17_13_7_all.txt | wc -l   # 80 distinct classes
# --- E. filters: definitional checker vs my hook vs the prover's filter_hits; controls
for tag in 6_3_2_D3 8_5_3_D3 10_7_4_D3 10_8_4_D3 13_8_5_D3 13_8_5_D8 13_9_5_D3 16_10_6_D3 14_12_6_D3 17_12_7_D3; do n=${tag%%_*}
  grep "^G " out/cells/g_$tag.txt > out/flags/g_$tag.txt; python3 src/hyp.py $n < out/flags/g_$tag.txt > out/flags/chk_$tag.txt
  sed 's/^G [^:]*:/X:/' out/flags/g_$tag.txt | ./prover_copy/indep/filter_hits X > out/flags/pf_$tag.txt; python3 src/flagcmp.py out/flags/g_$tag.txt out/flags/chk_$tag.txt out/flags/pf_$tag.txt | tail -n 1; done
python3 src/hyp.py 17 < out/direct_17_13_7_all.txt > out/flags/chk_17_13_7.txt; sed 's/^G [^:]*:/X:/' out/direct_17_13_7_all.txt | ./prover_copy/indep/filter_hits X > out/flags/pf_17_13_7.txt
python3 src/flagcmp.py out/direct_17_13_7_all.txt out/flags/chk_17_13_7.txt out/flags/pf_17_13_7.txt | tail -n 1
python3 src/hyp.py < src/controls.txt; sed 's/^[A-Za-z0-9_]*:/X:/' src/controls.txt | ./prover_copy/indep/filter_hits X | tail -n 1
# --- F. final step with my own extension program (unfiltered lists, in-C lists, labelled sample)
python3 src/add_edge.py 14 < out/cells/g_14_12_6_D3.txt > out/in18_T14_plus_edge_all38.txt
./bin/myext 17 8 3 < out/direct_17_13_7_part0.txt > out/final/ext_part0.txt; ./bin/myext 17 8 3 < out/direct_17_13_7_part1.txt > out/final/ext_part1.txt
./bin/myext 17 8 3 < out/in18_T14_plus_edge_all38.txt > out/final/ext_T14e.txt; grep -h "^HIT" out/final/ext_part0.txt out/final/ext_part1.txt out/final/ext_T14e.txt > out/final/hits_sofar.txt
python3 src/hyp.py 18 < out/final/hits_sofar.txt   # every tau=8 extension: f7=1 p3=0 conn=0
(grep "C=1" out/direct_17_13_7_all.txt; grep "C=1" out/in18_T14_plus_edge_all38.txt) > out/final/inC_inputs.txt; ./bin/myext 17 8 3 < out/final/inC_inputs.txt | tail -n 1
# labelled cross-check on 400 random prover inputs: see the python snippet in the review (seed 757), then
./bin/myext 17 8 3 < out/final/sample400_G.txt | tail -n 1; ./prover_copy/indep/ext_indep3 17 7 3 < out/final/sample400_prover.txt | tail -n 1
# --- G. the prover's pipeline from scratch (C1-C7 + checksums)
./src/rerun_prover.sh > logs/rerun_prover.log 2>&1
# --- H. witness
python3 src/witness.py > logs/witness.log
