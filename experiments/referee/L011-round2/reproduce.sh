#!/bin/bash
# Referee L011 round 2 (results/reviews/L011-f22-equals-13__referee__<UTC>.md): every computation of the review, in order.
# Run from this directory.  Large outputs go to out/ and logs/ (git-ignored; bin/ too).  Referee code in src/ (written from
# scratch: no e757, no judge except one run on a scratch witness copy, no prover/falsifier code; prover programs are run only as
# COPIES in out/rerun/).  nauty 2.8.8 C sources = PyPI sdist pynauty-2.8.8.1.tar.gz, sha256
# 454d3b0e605d649d13478afb090daef4a152f15c4a337a391fe69fded7e683f2 (copied from ../L010-round1/out/dl); headers by src/hdrs.py
# (template substitution; the tarball's configure is not run).  nice 5, at most 2 processes.
set -e
R=$(pwd); ND=$R/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; H=$R/out/nauty_hdr; P=/home/user/Erdos-757/experiments/prover/L011
mkdir -p out/dl bin logs witness
[ -d $ND ] || (cp ../L010-round1/out/dl/pynauty-2.8.8.1.tar.gz out/dl/ && sha256sum out/dl/pynauty-2.8.8.1.tar.gz && cd out/dl && tar xzf pynauty-2.8.8.1.tar.gz)
python3 -I src/hdrs.py $ND $H
NAU="$ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c"
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=64 -DPRUNE1=hprune -DOUTPROC=hout -DSUMMARY=hsum -I$H -I$ND -o bin/genbg_h $ND/genbg.c src/hk.c $NAU
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=64 -DPRUNE1=hprune -DOUTPROC=hout -DSUMMARY=hsum -I$H -I$ND -o bin/genbg_h2 $ND/genbg.c src/hk2.c $NAU
gcc -O2 -DMAXN=WORDSIZE -DWORDSIZE=64 -I$H -I$ND -o bin/canon src/canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c -lm
gcc -O2 -o bin/bf src/bf.c; gcc -O2 -o bin/rf src/rf.c; gcc -O3 -march=native -o bin/ext src/ext.c
# 1. arithmetic (window cells, degree bounds, counting, slack cells with/without K8, decompositions incl. isolated vertex)
python3 -I src/arith.py > out/arith.txt; python3 -I src/records.py > out/records.txt
# 2. genbg+hook vs labelled brute force (sum n!/|Aut| over classes with tau >= T0), n <= 9 (and n = 10 partially)
python3 -I src/validate.py bin 3,4,5,6,7,8 2,3; python3 -I src/validate.py bin 9 2,3; python3 -I src/validate.py bin 10 2,3 > logs/validate_10.txt  # (stopped at n=10,D=3,m=8)
# 3. filter controls and component cells (genbg, tau prune), class comparison with the prover's lists, in-C classes, certificates
./bin/rf 17 < src/controls.txt   # (controls: F7, relabelled/shifted/variant F7, AG(2,3), Fano, Fano-1, Pasch, near-F7s)
bash src/cells.sh "6 3 2 3" "8 5 3 3" "8 6 3 3" "9 4 3 3" "10 7 4 3" "10 8 4 3" "11 6 4 3" "11 7 4 3" "13 8 5 3" "14 7 5 3" "14 8 5 3" "17 8 6 3" "12 10 5 3"
bash src/cells.sh "13 9 5 3" "16 9 6 3" "17 9 6 3" "19 10 7 3" "20 10 7 3" "15 11 6 3" "16 10 6 3" "14 12 6 3" "21 11 8 2" "21 12 8 2" "21 13 8 2" "18 12 7 3" "17 13 7 3" "19 11 7 3"
for c in "6 3 2" "8 5 3" "8 6 3" "9 4 3" "10 7 4" "10 8 4" "11 7 4" "13 8 5" "13 9 5" "14 8 5" "16 10 6" "12 10 5" "15 11 6" "14 12 6" "18 12 7" "17 13 7" "19 11 7"; do set -- $c
  f=out/g_$1_$2_$3_d3.txt; ./bin/rf $1 < $f > out/rf_$1_$2_$3.txt; paste -d' ' out/rf_$1_$2_$3.txt $f | awk '$4=="f7=-" && $5=="p3=-1" && $6=="conn=1"' | sed 's/.*G:/G:/' > out/gC_$1_$2_$3.txt
  python3 -I src/certify.py $1 $f out/rf_$1_$2_$3.txt --tau --inC-full; done
for c in "6 3 2" "8 5 3" "8 6 3" "9 4 3" "10 7 4" "10 8 4" "11 7 4" "13 8 5" "13 9 5" "14 8 5" "16 10 6" "19 11 7"; do set -- $c; python3 -I src/cmp.py $1 out/g_$1_$2_$3_d3.txt $P/out/cell_$1_$2_$3.txt G: FOUND:; done
python3 -I src/cmp.py 12 out/g_12_10_5_d3.txt ../../prover/L008/indep/mine_12_10_5_deg3.txt.gz G: FOUND:; python3 -I src/cmp.py 15 out/g_15_11_6_d3.txt ../../prover/L008/indep/mine_15_11_6_deg3.txt.gz G: FOUND:
for c in "6 3 2" "8 5 3" "8 6 3" "9 4 3" "10 7 4" "10 8 4" "11 7 4" "13 9 5" "14 8 5" "16 10 6" "12 10 5" "15 11 6"; do set -- $c; python3 -I src/cmp.py $1 out/gC_$1_$2_$3.txt $P/out/filt_$1_$2_$3.txt G: SURVIVOR:; done
python3 -I src/cmp.py 14 out/gC_14_12_6.txt $P/out/filt_T14.txt G: SURVIVOR:; python3 -I src/cmp.py 17 out/gC_17_13_7.txt $P/out/filt_T17.txt G: SURVIVOR:
# 4. class-level inputs (multisets of in-C class representatives) and the extension steps with my own ext (tau tested on H) + rf + certify
python3 -I src/build.py out/ci_c4.txt AP AP AP AP 8,5,3
python3 -I src/build.py out/ci_x20_1.txt AP AP AP 10,8,4; python3 -I src/build.py out/ci_x20_2.txt AP AP 13,9,5; python3 -I src/build.py out/ci_x20_3.txt AP 6,3,2 10,7,4
python3 -I src/build.py out/ci_x20_4.txt AP 8,5,3 8,5,3; python3 -I src/build.py out/ci_x20_5.txt AP 16,10,6; python3 -I src/build.py out/ci_x20_8.txt 9,4,3 10,7,4
python3 -I src/build.py out/ci_x21_1.txt I AP AP AP 10,7,4; python3 -I src/build.py out/ci_x21_5.txt AP AP AP AP 8,6,3; python3 -I src/build.py out/ci_x21_6.txt AP AP AP 11,7,4
python3 -I src/build.py out/ci_x21_7.txt AP AP 6,3,2 8,5,3; python3 -I src/build.py out/ci_x21_8.txt AP AP 14,8,5; python3 -I src/build.py out/ci_x21_10.txt AP 8,5,3 9,4,3
python3 -I src/build.py out/ci_c8_a.txt AP AP AP 12,10,5; python3 -I src/build.py out/ci_c8_b.txt AP AP 15,11,6; python3 -I src/build.py out/ci_c8_c.txt AP 8,5,3 10,7,4
python3 -I src/build.py out/ci_c6_a.txt AP AP 14,12,6; python3 -I src/build.py out/ci_c6_b.txt AP 17,13,7; python3 -I src/build.py out/ci_c6_c.txt 10,7,4 10,7,4
cat out/ci_x20_*.txt > out/ci_x20.txt; cat out/ci_x21_*.txt > out/ci_x21.txt; cat out/ci_c8_a.txt out/ci_c8_b.txt out/ci_c8_c.txt > out/ci_c8.txt; cat out/ci_c6_a.txt out/ci_c6_b.txt out/ci_c6_c.txt > out/ci_c6.txt
for spec in "c4 20 8 21" "x20 19 8 20" "x21 20 8 21" "c6 20 9 21" "c8 21 9 22"; do set -- $spec
  ./bin/ext $2 $3 3 < out/ci_$1.txt > out/x_$1.txt; ./bin/rf $4 < out/x_$1.txt > out/rf_x_$1.txt; python3 -I src/certify.py $4 out/x_$1.txt out/rf_x_$1.txt; done
python3 -I src/certify.py 21 out/x_c6.txt out/rf_x_c6.txt --tau
# prover inputs vs class-level inputs (isomorphism classes)
python3 -I src/cmp.py 20 out/ci_c4.txt $P/out/in21_12.txt; python3 -I src/cmp.py 19 out/ci_x20.txt $P/out/inX20_all.txt; python3 -I src/cmp.py 20 out/ci_x21.txt $P/out/inX21_all.txt
python3 -I src/cmp.py 21 out/ci_c8.txt $P/out/in22_16_all.txt.gz; python3 -I src/cmp.py 20 out/ci_c6.txt $P/out/in21_17_all.txt.gz
# superset runs (all Delta<=3 component classes, including the types that are empty in C): out/ca_*.txt via build.py --all (see review)
# 5. labelled cross-check: my ext vs a copy of ext_indep5 on seeded random samples of the prover's labelled inputs (src/samehits.py)
# 6. direct searches: TAU0=8 ./bin/genbg_h -q -c -Z1 -d1:3 -D3:3 21 12 36:36 ; TAU0=8 F7P=1 ./bin/genbg_h2 -q -c -Z1 -d1:3 -D3:3 21 13 39:39
#    (F7-prune validated: on 12 cells the pruned output = the F7-free classes of the unpruned output)
# 7. witness: python3 -I src/witness.py ; python3 /home/user/Erdos-757/judge/judge.py witness/L011R2-witness-c22.json
# 8. re-run of the prover's pipeline from copies in out/rerun (decomp22, enum_conn cells incl. (19,11,7), (21,13,8,2), (20,14,8,2),
#    filter_hits C3, C4, C5, C7, all four parts of C6 (run_c6.sh) and of C8 with filters (run_c8.sh)); compared by cmp / sha256
