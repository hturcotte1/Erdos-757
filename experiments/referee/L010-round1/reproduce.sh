#!/bin/bash
# Referee L010 round 1 (results/reviews/L010-f20-equals-12__referee__<UTC>.md): every computation of the review, in order.
# Run from this directory.  Large files go to out/ (git-ignored).  Referee code: src/ (written from scratch; no e757, no judge,
# no prover/falsifier code except in step 9, which re-runs COPIES of the prover's programs in out/rerun/).
# nauty 2.8.8 C sources: from the PyPI sdist pynauty-2.8.8.1 (sha256 454d3b0e...83f2), unpacked to out/dl; headers generated
# by src/gen_headers.py (plain template substitution; the sdist's configure script is NOT run).
set -e
R=$(pwd); ND=$R/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; B=$R/out/nauty_build
P8=/home/user/Erdos-757/experiments/prover/L008/indep; P9=/home/user/Erdos-757/experiments/prover/L009/indep; P10=/home/user/Erdos-757/experiments/prover/L010/out
mkdir -p out/dl out/nauty_build bin
[ -f out/dl/pynauty-2.8.8.1.tar.gz ] || (cd out/dl && pip download --no-deps --no-binary :all: pynauty==2.8.8.1 -d . && tar xzf pynauty-2.8.8.1.tar.gz)
python3 -I src/gen_headers.py $ND $B
NAU="$ND/gtools.c $ND/schreier.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/naurng.c"
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=32 -DPRUNE1=refprune -DOUTPROC=refout -DSUMMARY=refsummary -I$B -I$ND -o bin/genbg_ref $ND/genbg.c src/hooks.c $NAU
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=64 -DPRUNE1=refprune -DOUTPROC=refout -DSUMMARY=refsummary -I$B -I$ND -o bin/genbg_ref64 $ND/genbg.c src/hooks.c $NAU
for W in 32 64; do gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=$W -DPRUNE1=refprune2 -DOUTPROC=refout2 -DSUMMARY=refsummary2 -I$B -I$ND -o bin/genbg_C$W $ND/genbg.c src/hooks2.c $NAU; done
gcc -O2 -DWORDSIZE=64 -DMAXN=0 -I$B -I$ND -o bin/canon src/canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c -lm
gcc -O2 -o bin/bf src/bf.c; gcc -O2 -o bin/ref_ext src/ref_ext.c; gcc -O2 -o bin/ref_filter src/ref_filter.c
# 1. arithmetic (window cells, degree bounds, slack cells with/without HY, all decompositions incl. isolated vertices)
python3 -I src/arith.py > out/arith.txt
# 2. genbg pipeline validated against the labelled brute force (n <= 9, D in {2,3}; n <= 8 any degree)
python3 -I src/validate_genbg.py 3:2 4:2 5:2 6:2 7:2 8:2 9:2 3:3 4:3 5:3 6:3 7:3 8:3 9:3 3:9 4:9 5:9 6:9 7:9 8:9
# 3. component cells (Delta <= 3) and the window cells closed by direct enumeration, with genbg (tau-prune only)
g() { TAU0=$3 ./bin/$5 -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) > out/g_$1_$2_$3_d$4.txt; }
for c in "6 3 2" "8 5 3" "8 6 3" "9 4 3" "10 7 4" "11 6 4" "11 7 4" "13 8 5" "14 8 5" "16 9 6" "17 9 6" "12 10 5" "15 11 6" "19 10 7" "18 12 7"; do set -- $c; g $1 $2 $3 3 genbg_ref; done
g 19 9 7 9 genbg_ref; g 18 12 7 2 genbg_ref; g 20 12 8 2 genbg_ref; g 20 13 8 2 genbg_ref64
# 4. class sets of the prover's lists vs genbg; membership in C (referee filter) of all lists
for x in "6 $P9/cell_6_3_2.txt 6_3_2" "8 $P9/cell_8_5_3.txt 8_5_3" "10 $P9/cell_10_7_4.txt 10_7_4" "13 $P9/cell_13_8_5.txt 13_8_5" "8 $P10/cell_8_6_3.txt 8_6_3" "9 $P10/cell_9_4_3.txt 9_4_3" "11 $P10/cell_11_7_4.txt 11_7_4" "14 $P10/cell_14_8_5.txt 14_8_5" "12 $P8/mine_12_10_5_deg3.txt.gz 12_10_5" "15 $P8/mine_15_11_6_deg3.txt.gz 15_11_6"; do set -- $x; python3 -I src/compare_classes.py $1 $2 out/g_$3_d3.txt; done
# F7/P3 controls: F7, relabelled F7, AG(2,3) (F7 and P3-bad), Fano (no F7, P3-bad), Fano minus 2 lines (neither), Pasch (neither)
printf "T: (0,1,2) (0,3,4) (0,5,6) (1,3,5) (2,4,6)\nT: (6,5,4) (6,3,2) (6,1,0) (5,3,1) (4,2,0)\nT: (0,1,2) (3,4,5) (6,7,8) (0,3,6) (1,4,7) (2,5,8) (0,4,8) (1,5,6) (2,3,7) (0,5,7) (1,3,8) (2,4,6)\nT: (0,1,2) (0,3,4) (0,5,6) (1,3,5) (1,4,6) (2,3,6) (2,4,5)\nT: (0,1,2) (0,3,4) (0,5,6) (1,3,5) (1,4,6)\nT: (0,1,2) (0,3,4) (1,3,5) (2,4,5)\n" > out/controls_f7.txt
./bin/ref_filter T < out/controls_f7.txt | tail -1
for c in 6_3_2 8_5_3 8_6_3 9_4_3 10_7_4 11_7_4 13_8_5 14_8_5 12_10_5 15_11_6 11_6_4 16_9_6 17_9_6 19_10_7 18_12_7; do ./bin/ref_filter FOUND < out/g_${c}_d3.txt > out/gC_${c}.txt; tail -1 out/gC_${c}.txt; done
# 5. extension inputs from class representatives (all decompositions; components in C, and all Delta<=3 classes) and the
#    referee extension program (direct tau test on H); certificates for every hit outside C
for x in "17 9 3 C repX_C" "17 9 3 all repX_all" "18 12 1 C repH19_C" "18 12 1 all repH19_all" "19 10 0 C repH20_C" "19 10 0 all repH20_all"; do set -- $x; python3 -I src/build_reps.py $1 $2 $3 $4 out/$5.txt; done
./bin/ref_ext 17 6 3 1 < out/repX_C.txt > out/ext_repX_C.txt; ./bin/ref_ext 17 6 3 1 < out/repX_all.txt > out/ext_repX_all.txt
./bin/ref_ext 18 7 3 1 < out/repH19_C.txt > out/ext_repH19_C.txt; ./bin/ref_ext 18 7 3 1 < out/repH19_all.txt > out/ext_repH19_all.txt
./bin/ref_ext 19 7 3 1 < out/repH20_C.txt > out/ext_repH20_C.txt; ./bin/ref_ext 19 7 3 1 < out/repH20_all.txt > out/ext_repH20_all.txt
grep "_conn" out/ext_repX_C.txt > out/ext_repX_C_conn.txt; python3 -I src/certify_hits.py out/ext_repX_C_conn.txt 6
python3 -I src/certify_hits.py out/ext_repH19_C.txt 7; python3 -I src/certify_hits.py out/ext_repH20_C.txt 7
# 6. direct (no rebuild) enumeration of connected (18,12,>=7), Delta<=3: 9 classes, all contain F7
./bin/ref_filter FOUND < out/g_18_12_7_d3.txt | tail -1
# 7. witness C20 from the definitions
python3 -I witness/check_c20.py
# 8. controls without the tau requirement
python3 -I src/control_ext.py out/repH19_C.txt 18 25 7 | ./bin/ref_filter CTL 19 | tail -1; python3 -I src/control_ext.py out/repH20_C.txt 19 500 7 | ./bin/ref_filter CTL 20 | tail -1
# 9. re-run of the prover's pipeline (copies of the programs), then class/labelled comparisons
mkdir -p out/rerun/bin; cp /home/user/Erdos-757/experiments/prover/L010/indep/{enum_conn,ext_indep4,filter_hits,filter_hits2}.c /home/user/Erdos-757/experiments/20261017-0705-n19-n20-via-i11/ext_vertex2.c out/rerun/bin/
cp /home/user/Erdos-757/experiments/prover/L010/{combine,connected_filter,compare_hits,decomp20}.py out/rerun/
(cd out/rerun/bin && gcc -O2 -Wall -o enum_conn enum_conn.c && gcc -O2 -Wall -o ext_indep4 ext_indep4.c && gcc -O2 -o filter_hits filter_hits.c && gcc -O2 -o filter_hits2 filter_hits2.c && gcc -O2 -o ext_vertex2 ext_vertex2.c)
bash src/rerun_prover.sh > out/rerun/rerun.log 2>&1
for c in "19 9 7 1000" "19 10 7 3" "20 12 8 2" "18 12 7 2" "20 13 8 2"; do set -- $c; out/rerun/bin/enum_conn $1 $2 $3 $4 0 | tail -n1; done
grep "^CHIT" out/ext_repX_C.txt | ./bin/canon x 18 | awk '{print $1}' | sort -u > out/cls_X_inC_mine.txt
grep "^SURVIVOR" out/rerun/filtX.txt | ./bin/canon x 18 | awk '{print $1}' | sort -u > out/cls_X_inC_prover.txt; cmp out/cls_X_inC_mine.txt out/cls_X_inC_prover.txt
grep "HIT" out/ext_repH19_C.txt | ./bin/canon x 19 | awk '{print $1}' | sort -u > out/cls_H19hits_mine.txt
grep "^HIT" out/rerun/hitsH19.txt | ./bin/canon x 19 | awk '{print $1}' | sort -u > out/cls_H19hits_prover.txt; cmp out/cls_H19hits_mine.txt out/cls_H19hits_prover.txt
for x in "inH19 repH19_C 18" "inX_all repX_C 17" "inH20 repH20_C 19"; do set -- $x; ./bin/canon -n $3 < out/rerun/$1.txt | awk '{print $1}' | sort -u > out/cls_prover_$1.txt; ./bin/canon x $3 < out/$2.txt | awk '{print $1}' | sort -u > out/cls_mine_$2.txt; cmp out/cls_prover_$1.txt out/cls_mine_$2.txt; done
# labelled cross-checks of ref_ext against the prover's hits (all C6 inputs; the C4 isolated-vertex type; 3,000 random C5 inputs)
python3 -I - << 'PY'
import random
def conv(src, dst, sample=None, seed=1017):
    L = open(src).read().splitlines()
    if sample: random.seed(seed); L = random.sample(L, sample)
    with open(dst, 'w') as f:
        for l in L:
            a = list(map(int, l.split())); m = a[0]
            f.write('G: ' + ' '.join('(%d,%d,%d)' % tuple(a[1+3*i:4+3*i]) for i in range(m)) + '\n')
conv('out/rerun/inH20.txt', 'out/inH20_prover_fmt.txt'); conv('out/rerun/inX_9.txt', 'out/inX9_fmt.txt'); conv('out/rerun/inH19.txt', 'out/inH19_sample3000.txt', 3000)
PY
./bin/ref_ext 19 7 3 1 < out/inH20_prover_fmt.txt > out/ext_inH20_prover.txt; python3 -I src/cmp_hitsets.py out/ext_inH20_prover.txt out/rerun/hitsH20.txt
./bin/ref_ext 17 6 3 1 < out/inX9_fmt.txt > out/ext_inX9_prover.txt; python3 -I src/cmp_hitsets.py out/ext_inX9_prover.txt out/rerun/hitsX9_mine.txt
./bin/ref_ext 18 7 3 1 < out/inH19_sample3000.txt > out/ext_inH19_sample.txt; python3 -I src/restrict_hits.py 18 out/inH19_sample3000.txt out/rerun/hitsH19.txt out/ext_inH19_sample.txt
# 10. supplementary direct searches in C (tau + F7 pruning, P3 at output): L009 cells and (20,13,8)
for c in "17 12 7 3" "18 10 7 10" "18 11 7 3"; do set -- $c; TAU0=$3 ./bin/genbg_C32 -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) > out/gC_direct_$1_$2_$3.txt; done
# (20,13,8) direct search: attempted, NOT completed (killed after 825 s wall, ~9 CPU-min; parts k/200 take ~36 CPU-s each,
# so a full run needs ~2 CPU-hours).  No claim is made from it.
# TAU0=8 ./bin/genbg_C64 -q -c -Z1 -d1:3 -D3:3 20 13 39:39 > out/gC_direct_20_13_8.txt
# 11. frozen judge on a scratch copy of the witness C20 (not a claim file)
python3 /home/user/Erdos-757/judge/judge.py witness/L010R1-witness-c20.json
