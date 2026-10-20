#!/bin/bash
# Referee L010 round 2 (results/reviews/L010-f20-equals-12__referee__<UTC>.md): every computation of the review, in order.
# Run from this directory.  Large files go to out/ and logs/ (git-ignored); binaries to bin/ (git-ignored).
# Referee code: src/, witness/ (written from scratch; no e757, no judge code, no prover/falsifier code).  nauty 2.8.8 C sources
# from the pynauty-2.8.8.1 sdist (sha256 454d3b0e605d649d13478afb090daef4a152f15c4a337a391fe69fded7e683f2), copied from
# ../L010-round1/out/dl/ to out/nauty/src, with the config headers generated there by round 1 (template substitution).
# Prover programs are run ONLY as copies in out/prover_copy (two paths patched so that nothing in the prover folder is written).
set -e
R=$(pwd); ND=out/nauty/src; B=out/nauty/hdr; P=/home/user/Erdos-757/experiments/prover
mkdir -p out/nauty bin logs
[ -d $ND ] || cp -r ../L010-round1/out/dl/pynauty-2.8.8.1/src/nauty2_8_8 $ND
[ -d $B ] || (mkdir -p $B && cp ../L010-round1/out/nauty_build/*.h $B/)
NAU="$ND/gtools.c $ND/schreier.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/naurng.c"
for W in 32 64; do gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=$W -DPRUNE1=r2prune -DOUTPROC=r2out -DSUMMARY=r2sum -I$B -I$ND -o bin/genbg_r2_$W $ND/genbg.c src/hooks.c $NAU; done
gcc -O2 -DWORDSIZE=64 -DMAXN=0 -I$B -I$ND -o bin/canon src/canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c -lm
gcc -O3 -DMAXN=WORDSIZE -DWORDSIZE=32 -I$B -I$ND -o bin/geng $ND/geng.c $NAU
gcc -O2 -o bin/bf src/bf.c; gcc -O2 -o bin/ext src/ext.c; gcc -O2 -o bin/myfilter src/myfilter.c; gcc -O2 -o bin/tauf src/tauf.c
# 1. arithmetic: window cells, degree bounds, slack cells (with/without HY), all decompositions incl. isolated vertex; no-HY cells
python3 -I src/arith.py > out/arith.txt
# 2. genbg+hooks vs labelled brute force (n<=9; D in {2,3}; connected and arbitrary; dmin 0/1; every tau threshold; F7PRUNE 0/1)
python3 -I src/validate.py > logs/validate.log
# 3. direct enumerations of ALL G = H - v (any connectivity, isolated vertices allowed), F7-free, Delta<=3
TAU0=7 F7PRUNE=1 ./bin/genbg_r2_32 -q -Z1 -d0:3 -D3:3 18 12 36:36 > out/G18_12_7_d0.txt 2> logs/G18_12_7_d0.err
TAU0=7 F7PRUNE=1 ./bin/genbg_r2_32 -q -Z1 -d0:3 -D3:3 19 10 30:30 > out/G19_10_7_d0.txt 2> logs/G19_10_7_d0.err
TAU0=6 F7PRUNE=1 ./bin/genbg_r2_32 -q -Z1 -d0:3 -D3:3 17 9 27:27 > out/G17_9_6_d0.txt 2> logs/G17_9_6_d0.err
for x in "18 out/G18_12_7_d0.txt" "19 out/G19_10_7_d0.txt" "17 out/G17_9_6_d0.txt"; do set -- $x; grep "p3=1" $2 | python3 -I src/comps.py $1; done
grep "p3=1" out/G18_12_7_d0.txt > out/G18_inC.txt; grep "p3=1" out/G19_10_7_d0.txt > out/G19_inC.txt; grep "p3=1" out/G17_9_6_d0.txt > out/G17_inC.txt
for x in "18 G18_inC inH19 G18" "19 G19_inC inH20 G19" "17 G17_inC inX_all G17"; do set -- $x
  ./bin/canon $1 < out/$2.txt | awk '{print $1}' | sort -u > out/cls_$4_mine.txt
  ./bin/canon $1 -n < $P/L010/out/$3.txt | awk '{print $1}' | sort -u > out/cls_$4_prover_$3.txt; cmp out/cls_$4_mine.txt out/cls_$4_prover_$3.txt; done
# 4. referee extensions on the class representatives (direct exact tau on H, F7, P3, connectivity)
./bin/ext 18 7 3 1 < out/G18_inC.txt > out/ext_G18.txt; tail -1 out/ext_G18.txt
./bin/ext 19 7 3 1 < out/G19_inC.txt > out/ext_G19.txt; tail -1 out/ext_G19.txt; ./bin/ext 19 7 3 0 < out/G19_10_7_d0.txt | tail -1
./bin/ext 17 6 3 0 < out/G17_inC.txt > out/ext_G17.txt; tail -1 out/ext_G17.txt
grep "^HIT" out/ext_G17.txt | grep "conn=1" | ./bin/canon 18 | awk '{print $1}' | sort -u | wc -l
./bin/ext 17 6 3 1 < out/G17_inC.txt | grep "inC=1" | ./bin/canon 18 | awk '{print $1}' | sort -u > out/cls_X_inC_mine.txt; cmp out/cls_X_inC_mine.txt out/cls_G18_mine.txt
# 5. the small window cells directly (no F7 pruning) and the Delta<=2 cells through the dual graph (geng + exact matching)
for c in "19 9 7 9 32" "20 12 8 2 32" "18 12 7 2 32" "20 13 8 2 64"; do set -- $c; TAU0=$3 F7PRUNE=0 ./bin/genbg_r2_$5 -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) > out/direct_$1_$2_$3_D$4.txt 2> logs/direct_$1_$2_$3_D$4.err; done
for c in "12 18 7" "12 16 8" "13 19 8"; do set -- $c; ./bin/geng -cq -D3 $1 $2:$2 | python3 -I src/dualmatch.py $1 $3; done
# 6. component lists of C2/C3 at class level (genbg, connected, Delta<=3) vs the prover's labelled lists; classes in C
bash src/components.sh
# 7. re-run of the prover's pipeline from copies (out/prover_copy, run_cells.sh cd-path and the L007 path patched)
PC=out/prover_copy; mkdir -p $PC/indep $PC/out $PC/bin; cp $P/L010/*.py $P/L010/reproduce.sh $PC/; cp $P/L010/indep/*.c $P/L010/indep/run_cells.sh $PC/indep/
sed -i "s#cd /home/user/Erdos-757/experiments/prover/L010/indep#cd $R/$PC/indep#" $PC/indep/run_cells.sh
sed -i "s#\.\./L007/indep/mine_10_7_4.txt#$P/L007/indep/mine_10_7_4.txt#" $PC/reproduce.sh
(cd $PC && bash reproduce.sh) > logs/prover_rerun.log 2>&1
# 8. labelled cross-checks: my filter on the prover's hit files; Hall-matching P3 vs subset P3; my ext vs ext_indep4 on 8,000 inputs
zcat $P/L010/out/hitsX.txt.gz | ./bin/myfilter HIT 18; zcat $P/L010/out/hitsX.txt.gz | head -200000 | ./bin/myfilter HIT 18 match
zcat $P/L010/out/hitsH19.txt.gz | ./bin/myfilter HIT 19; zcat $P/L010/out/hitsH19.txt.gz | awk 'NR%11==0' | ./bin/myfilter HIT 19 match
./bin/myfilter HIT 20 match < $P/L010/out/hitsH20.txt
grep "^HIT" out/ext_G18.txt | ./bin/canon 19 | awk '{print $1}' | sort -u > out/cls_H19hits_mine.txt
zcat $P/L010/out/hitsH19.txt.gz | grep "^HIT" | ./bin/canon 19 | awk '{print $1}' | sort -u > out/cls_H19hits_prover.txt; cmp out/cls_H19hits_mine.txt out/cls_H19hits_prover.txt
./bin/ext 19 7 3 1 < out/G19_inC.txt | grep "^HIT" | ./bin/canon 20 | awk '{print $1}' | sort -u > out/cls_H20hits_mine.txt
grep "^HIT" $P/L010/out/hitsH20.txt | ./bin/canon 20 | awk '{print $1}' | sort -u > out/cls_H20hits_prover.txt; cmp out/cls_H20hits_mine.txt out/cls_H20hits_prover.txt
python3 -I -c "
import random
L=open('$P/L010/out/inH19.txt').read().splitlines(); random.seed(424242); open('out/inH19_s8000.txt','w').write('\n'.join(random.sample(L,8000))+'\n')"
./bin/ext 18 7 3 1 < out/inH19_s8000.txt > out/ext_inH19_s8000.txt; python3 -I src/cmp_labelled.py 18 out/inH19_s8000.txt $P/L010/out/hitsH19.txt.gz out/ext_inH19_s8000.txt
# 9. controls: F7/P3 detectors (13 control graphs, both filters), non-vacuity (no tau requirement), control19 tau claim
for i in $(seq 1 13); do sed -n "${i}p" src/controls.txt > out/c1.txt; ./bin/myfilter T 20 match < out/c1.txt; $PC/indep/filter_hits T < out/c1.txt | tail -1; done
awk 'NR%9==1' out/G18_inC.txt > out/G18_ctl.txt; ./bin/ext 18 -1 3 0 < out/G18_ctl.txt | tail -1; ./bin/ext 19 -1 3 0 < out/G19_inC.txt | tail -1
./bin/tauf < $PC/out/control19_hits.txt
# 10. enum_conn (prover copy) vs brute force (n<=8) and vs genbg (9<=n<=13) at class level
python3 -I src/test_enum_conn.py 8; python3 -I src/test_enum_conn2.py 13 > logs/test_enum_conn2.log 2>&1
# 11. witness C20 from the definitions; frozen judge on a scratch copy (not a claim file)
python3 -I witness/check_c20.py; python3 /home/user/Erdos-757/judge/judge.py witness/L010R2-witness-c20.json
