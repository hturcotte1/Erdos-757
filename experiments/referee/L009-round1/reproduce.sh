#!/bin/bash
# Referee L009 round 1 (f(18) = 11): every command of the review, from scratch.  Large outputs go to out/ (git-ignored).
# nauty 2.8.8 source: PyPI sdist pynauty-2.8.8.1 (pip download --no-deps --no-binary :all: pynauty==2.8.8.1),
# sha256 454d3b0e605d649d13478afb090daef4a152f15c4a337a391fe69fded7e683f2, unpacked to out/dl, copied to out/nauty, ./configure --disable-popcnt; make genbg labelg.
set -e
cd /home/user/Erdos-757/experiments/referee/L009-round1
P=/home/user/Erdos-757/experiments/prover/L009; ND=out/nauty
# --- build: referee programs (src/) and the prover's programs (recompiled from their sources, outputs only under out/)
gcc -O3 -march=native -DMAXN=WORDSIZE -DWORDSIZE=64 -DPRUNE1=refprune -DOUTPROC=refout -DSUMMARY=refsummary -I$ND -o bin/genbg_ref $ND/genbg.c src/hooks.c $ND/gtools.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O2 -DMAXN=0 -I$ND -o bin/canon src/canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O2 -o bin/bf src/bf.c; gcc -O2 -o bin/ext1 src/ext1.c
for p in enum_conn ext_indep2 ext_indep3 filter_hits; do gcc -O2 -o bin/${p}_prover $P/indep/$p.c; done
# --- 1. arithmetic (window cells, slack cells with/without HY, decompositions, degree bounds)
python3 src/cells.py
# --- 2. validation of genbg+refprune+canon and of the prover's enum_conn against brute force (18 small cells) and bf (10,7,4,3)
./src/validate_small.sh; ./bin/bf 10 7 4 3
# --- 3. component cells with genbg (Delta<=3), class sets vs the prover's labelled lists
for c in "6 3 2" "8 5 3" "10 7 4" "10 8 4" "13 8 5" "13 9 5" "16 10 6"; do set -- $c
  TAU0=$3 ./bin/genbg_ref -q -c -Z1 -d1:3 -D3:3 $1 $2 $((3*$2)):$((3*$2)) 2>out/err_$1_$2_$3.txt > out/g_$1_$2_$3.txt; grep REFSUMMARY out/err_$1_$2_$3.txt
  f=$P/indep/cell_$1_$2_$3.txt; if [ -f $f ]; then cat $f; else zcat $f.gz; fi | grep '^FOUND' | ./bin/canon $1 | awk '{print $1}' | sort -u > out/p_$1_$2_$3.cls
  ./bin/canon $1 < out/g_$1_$2_$3.txt | awk '{print $1}' | sort -u > out/g_$1_$2_$3.cls; cmp out/p_$1_$2_$3.cls out/g_$1_$2_$3.cls && echo "($1,$2,$3) class sets identical"
  grep 'C=1' out/g_$1_$2_$3.txt | ./bin/canon $1 | awk '{print $1}' | sort -u > out/gC_$1_$2_$3.cls; wc -l < out/gC_$1_$2_$3.cls; done
# --- 4. empty cells and Lemma 17 directly with genbg
for c in "16 9 6 9" "16 9 6 3" "18 10 7 10" "13 8 5 8" "18 11 7 3" "17 12 7 3"; do set -- $c
  TAU0=$3 ./bin/genbg_ref -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) 2>&1 >/dev/null | grep REFSUMMARY; done
# --- 5. Lemma R for (14,12,6) directly (no rebuild): all connected linear (14,12,tau>=6), Delta<=3
TAU0=6 ./bin/genbg_ref -q -c -Z1 -d1:3 -D3:3 14 12 36:36 2>out/err_14_12_6.txt > out/g_14_12_6.txt; grep REFSUMMARY out/err_14_12_6.txt
grep 'C=1' out/g_14_12_6.txt | ./bin/canon 14 | awk '{print $1}' | sort -u > out/gC_14_12_6.cls
./bin/canon 14 < $P/indep/T14_conn.txt | awk '{print $1}' | sort -u > out/pT14.cls; cmp out/pT14.cls out/gC_14_12_6.cls && echo "T14 == direct"
# --- 6. referee class-level rebuild (Lemma R) and final step, referee code only
python3 src/build_inputs.py
./bin/ext1 13 6 3 < out/in14_classlevel.txt > out/x14.txt; ./bin/ext1 16 7 3 < out/in17_classlevel.txt > out/x17.txt
grep "C=1 conn=1" out/x14.txt | ./bin/canon 14 | awk '{print $1}' | sort -u > out/x14C.cls; cmp out/x14C.cls out/gC_14_12_6.cls && echo "rebuild14 == direct"
grep "C=1 conn=1" out/x17.txt | ./bin/canon 17 | awk '{print $1}' | sort -u > out/x17C.cls
zcat $P/indep/T17_conn.txt.gz | ./bin/canon 17 | awk '{print $1}' | sort -u > out/pT17.cls; cmp out/pT17.cls out/x17C.cls && echo "T17 == referee rebuild"
python3 src/build_final_inputs.py
./bin/ext1 17 8 3 < out/in18_classlevel.txt > out/x18.txt
# --- 7. direct genbg enumeration of connected linear (17,13,tau>=7), Delta<=3 (two parts, about 1 CPU-hour in total)
./src/run_direct17.sh  # runs part 0/2 and part 1/2 sequentially (here they ran in parallel: part 0 by this script, part 1 by src/run_direct17_part1.sh)
cat out/g_17_13_7_part0.txt out/g_17_13_7_part1.txt > out/g_17_13_7_all.txt; grep "C=1" out/g_17_13_7_all.txt | ./bin/canon 17 | awk "{print \$1}" | sort -u > out/d17C.cls; cmp out/d17C.cls out/x17C.cls && cmp out/d17C.cls out/pT17.cls && echo "direct17 == rebuild == prover"
# --- 8. the prover's labelled pipeline C2-C7 re-run with outputs under out/pr
(cd out/pr && ../../src/rerun_prover.sh > rerun.log 2>&1)
# --- 9. witness A_18 and filter controls
python3 witness/check_A18.py
./bin/filter_hits_prover HIT < controls/controls.txt | tail -1
