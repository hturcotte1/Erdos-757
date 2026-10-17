#!/bin/bash
# Referee L011 round 1 (results/reviews/L011-f22-equals-13__referee__<UTC>.md): every computation of the review, in order.
# Run from this directory.  Large files go to out/ and logs/ (git-ignored).  Referee code: src/ (written from scratch; no e757,
# no judge except one extra run on a scratch copy of the witness; prover/falsifier programs are only run as COPIES in out/rerun/).
# nauty 2.8.8 C sources: PyPI sdist pynauty-2.8.8.1 (sha256 454d3b0e605d649d13478afb090daef4a152f15c4a337a391fe69fded7e683f2,
# the same tarball as experiments/referee/L010-round1/out/dl), unpacked to out/dl; headers by src/mkheaders.py (template
# substitution; the sdist's configure script is NOT run).  Machine: nice 5, at most 3 processes.
set -e
R=$(pwd); ND=$R/out/dl/pynauty-2.8.8.1/src/nauty2_8_8; B=$R/out/nauty_build
mkdir -p out/dl bin logs witness
[ -d $ND ] || (cd out/dl && cp ../../../L010-round1/out/dl/pynauty-2.8.8.1.tar.gz . && sha256sum pynauty-2.8.8.1.tar.gz && tar xzf pynauty-2.8.8.1.tar.gz)
python3 -I src/mkheaders.py $ND $B
NAU="$ND/gtools.c $ND/schreier.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/naurng.c"
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=64 -DPRUNE1=rprune -DOUTPROC=rout -DSUMMARY=rsum -I$B -I$ND -o bin/rgenbg $ND/genbg.c src/rhooks.c $NAU
gcc -O2 -DWORDSIZE=64 -DMAXN=WORDSIZE -I$B -I$ND -o bin/rcanon src/rcanon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c -lm
gcc -O2 -o bin/rbf src/rbf.c; gcc -O2 -o bin/rext src/rext.c; gcc -O2 -o bin/rfilt src/rfilt.c
# 1. arithmetic: window cells, degree bounds, counting, slack cells (with/without K8), decompositions (brute force incl. the
#    isolated vertex), record cells, Remark 4
python3 -I src/arith.py > out/arith.txt
# 2. genbg pipeline vs labelled brute force (tau prune), n <= 9, Delta <= 2 and <= 3
python3 -I src/validate.py bin 3,4,5,6,7,8 2,3 > logs/validate_small.txt; python3 -I src/validate.py bin 9 2,3 > logs/validate_9.txt
# 3. filter controls (F7, relabelled/shifted F7, AG(2,3), Fano, Fano-1, Fano-2, Pasch, near-F7, connectivity)
./bin/rfilt 17 X v < out/controls.txt; ./bin/rfilt 7 X v < out/controls_conn.txt
# 4. component cells and window cells (genbg, tau prune), class comparisons with the prover's lists, membership in C
rm -f logs/cells.txt
./src/cells.sh "6 3 2 3" "8 5 3 3" "8 6 3 3" "9 4 3 3" "10 7 4 3" "10 8 4 3" "11 6 4 3" "11 7 4 3" "13 8 5 3" "14 7 5 3" "14 8 5 3" "17 8 6 3"
./src/cells.sh "13 9 5 3" "16 9 6 3" "17 9 6 3" "19 10 7 3" "20 10 7 3" "12 10 5 3" "16 10 6 3" "15 11 6 3" "14 12 6 3" "18 12 7 3" "19 11 7 3" "17 13 7 3"
./src/cells.sh "21 11 8 2" "21 12 8 2" "21 13 8 2" "20 14 8 2" || true   # (20,14,8) D<=2: genbg rejects (42 > 40)
# (comparisons: see logs/cmp_cells.txt, logs/cmp_cells_inC.txt, logs/cells_inC.txt; commands as in the review)
# 5. F7-prune validation (CMODE=1 output = F7-free classes of the CMODE=0 output), then direct searches in C:
#    connected (21,12,>=8) Delta<=3 (tau prune only) and connected (21,13,>=8), (20,14,>=8) Delta<=3 (tau + F7 prune)
TAU0=8 CMODE=0 ./bin/rgenbg -q -c -Z1 -d1:3 -D3:3 21 12 36:36 > out/g_21_12_8_d3.txt 2> logs/g_21_12_8.err
TAU0=8 CMODE=1 ./bin/rgenbg -q -c -Z1 -d1:3 -D3:3 21 13 39:39 > out/gC_21_13_8_direct.txt 2> logs/gC_21_13_8_direct.err
TAU0=8 CMODE=1 ./bin/rgenbg -q -c -Z1 -d1:3 -D3:3 20 14 42:42 > out/gC_20_14_8_direct.txt 2> logs/gC_20_14_8_direct.err
# 6. class-level rebuild/extension steps with the referee's own programs (inputs = disjoint unions of genbg class reps;
#    C = components in C, all = every Delta<=3 class), filters, definitional certificates; then class comparison with the
#    prover's labelled hit files (src/hitclasses.sh; C6 comparison as in the review)
bash src/classlevel.sh > logs/classlevel.txt
bash src/hitclasses.sh
# 7. witness C22 from the definitions (+ the frozen judge on a scratch copy)
python3 -I src/witness.py
# 8. re-run of the prover's pipeline from copies (C1-C5, C7, inputs of C6/C8; C6 part00, C8 part03; C2 (19,11,7))
bash src/rerun_prover.sh; bash src/rerun_heavy_a.sh; bash src/rerun_heavy_b.sh
