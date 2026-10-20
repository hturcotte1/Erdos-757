#!/bin/bash
# Referee L008 round 3: every computation of the review, in order (run from this directory).  Nauty 2.8.8 source: PyPI sdist
# pynauty-2.8.8.1 (pip download --no-deps --no-binary :all: pynauty==2.8.8.1), unpacked at $ND; headers nauty.h, gtools.h,
# naututil.h = the .in templates with the configure placeholders filled (the round-1 copies were verified to differ from the
# templates only at '@...@' lines and reused).  P = prover folder, F = falsifier folder.
set -e
ND=${ND:-/path/to/pynauty-2.8.8.1/src/nauty2_8_8}; HD=${HD:-/home/user/Erdos-757/experiments/referee/L008-round1/nauty_build}
P=/home/user/Erdos-757/experiments/prover/L008; F=/home/user/Erdos-757/experiments/20261017-0300-n16-via-i11
mkdir -p bin out
gcc -O2 -o bin/enum_conn src/enum_conn.c; gcc -O2 -o bin/ext_indep2 src/ext_indep2.c; gcc -O2 -o bin/filter_hits src/filter_hits.c
gcc -O2 -o bin/ext_vertex2 $F/ext_vertex2.c; gcc -O2 -o bin/conn_dfs3 $F/conn_dfs3.c
gcc -O3 -DMAXN=WORDSIZE -DWORDSIZE=32 -DPRUNE1=r3prune -DOUTPROC=r3out -DSUMMARY=r3summary -I$HD -I$ND -o bin/genbg_r3 $ND/genbg.c src/r3_hooks.c $ND/gtools.c $ND/schreier.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/naurng.c
gcc -O2 -DWORDSIZE=64 -DMAXN=0 -I$HD -I$ND -o bin/r3canon src/r3canon.c $ND/nauty.c $ND/nautil.c $ND/naugraph.c $ND/schreier.c $ND/naurng.c
gcc -O2 -o bin/r3_bf src/r3_bf.c
# 1. arithmetic (Steps 1, 3, 4, Corollary 4)
python3 scripts/arith_own.py
# 2. realizable data (A_base, records, C16, Fibonacci, gluing, census)
python3 scripts/r3_realizable.py
# 3. my orderly generation (genbg + own tau/F7/P3 prunes) and class comparison with the authors' labelled lists
TAU0=5 bin/genbg_r3 -q -c -Z1 -d1:3 -D3:3 12 10 30:30 > out/g_12_10_5_d3.txt                      # 197
TAU0=5 F7PRUNE=1 P3PRUNE=1 bin/genbg_r3 -q -c -Z1 -d1:3 -D3:3 12 10 30:30 > out/g_12_10_5_d3_Oplus.txt   # 149
TAU0=6 bin/genbg_r3 -q -c -Z1 -d1:3 -D3:3 15 11 33:33 > out/g_15_11_6_d3.txt                      # 49
TAU0=6 F7PRUNE=1 P3PRUNE=1 bin/genbg_r3 -q -c -Z1 -d1:3 -D3:3 15 11 33:33 > out/g_15_11_6_d3_Oplus.txt   # 19
bin/r3canon FOUND 12 < out/g_12_10_5_d3.txt | awk '{print $1}' | sort > out/cls_g12.txt
zcat $P/indep/mine_12_10_5_deg3.txt.gz | bin/r3canon FOUND 12 | awk '{print $1}' | sort -u > out/cls_prover12.txt
zcat $F/R12_labelled.txt.gz | bin/r3canon FOUND 12 | awk '{print $1}' | sort -u > out/cls_fals12.txt
cmp out/cls_g12.txt out/cls_prover12.txt; cmp out/cls_g12.txt out/cls_fals12.txt
bin/r3canon FOUND 15 < out/g_15_11_6_d3.txt | awk '{print $1}' | sort > out/cls_g15.txt
(zcat $F/g15_11_6_part0.txt.gz; zcat $F/g15_11_6_part1.txt.gz) | bin/r3canon FOUND 15 | awk '{print $1}' | sort -u > out/cls_fals15.txt
zcat $P/indep/mine_15_11_6_deg3.txt.gz | bin/r3canon FOUND 15 | awk '{print $1}' | sort -u > out/cls_prover15.txt
cmp out/cls_g15.txt out/cls_fals15.txt; cmp out/cls_g15.txt out/cls_prover15.txt
for c in "5 3 2" "8 4 3" "10 6 4" "11 5 4" "12 9 5" "13 7 5" "15 9 6" "16 8 6" "15 10 6"; do set -- $c; TAU0=$3 bin/genbg_r3 -u -q -c -Z1 -d1:3 -D$2:3 $1 $2 $((3*$2)):$((3*$2)); done   # all 0
TAU0=6 bin/genbg_r3 -q -c -Z1 -d1:3 -D3:3 14 11 33:33 > out/g_14_11_6_d3.txt; TAU0=6 bin/genbg_r3 -q -c -Z1 -d1:3 -D11:3 14 11 33:33 > out/g_14_11_6_nodeg.txt   # 1, 3
TAU0=6 F7PRUNE=1 bin/genbg_r3 -u -q -c -Z1 -d1:3 -D11:3 14 11 33:33   # 0
# 4. brute-force validation (labelled, no symmetry reduction) of genbg_r3 and enum_conn on all cells n<=8
python3 scripts/validate_small.py 3 9
# 5. my definitional extension + filter pipeline (class level), and the route without Step 4
python3 scripts/r3_extend.py A out/g_12_10_5_d3.txt > out/r3_hits_A.txt; python3 scripts/r3_extend.py B out/g_15_11_6_d3.txt > out/r3_hits_B.txt
TAU0=6 bin/genbg_r3 -q -Z1 -d0:3 -D3:3 15 11 33:33 > out/g_15_11_6_d3_ALL.txt     # 261 (any connectivity)
python3 scripts/r3_extend.py C out/g_15_11_6_d3_ALL.txt > out/r3_hits_ALL.txt
# 6. authors' computations re-run (SHA-256 against $P/checksums_large_outputs.txt)
(cd $P && python3 decomp.py 16) | diff - $P/decomp_output.txt
bin/enum_conn 12 10 5 3 1 > out/enum_conn_12_10_5_deg3.txt; bin/conn_dfs3 12 10 5 3 0 0 > out/conn_dfs3_12_10_5.txt
python3 $P/build_inputs.py A out/enum_conn_12_10_5_deg3.txt out/inputA_all.txt; zcat $F/G_B_conn15.txt.gz > out/inputB_falsifier.txt
bin/ext_indep2 15 6 3 < out/inputA_all.txt > out/hitsA_ext_indep2.txt; bin/ext_indep2 15 6 3 < out/inputB_falsifier.txt > out/hitsB_ext_indep2.txt
bin/ext_vertex2 15 7 3 < out/inputA_all.txt > out/hitsA_ext_vertex2.txt
bin/filter_hits HIT < out/hitsA_ext_indep2.txt | tail -1; bin/filter_hits HIT < out/hitsB_ext_indep2.txt | tail -1
bin/enum_conn 15 11 6 3 1 > out/enum_conn_15_11_6_deg3.txt      # about 25-70 min depending on load
sha256sum out/*.txt
# hit classes: mine (class level) vs the authors' labelled hits
for c in A B; do bin/r3canon HIT 16 < out/r3_hits_$c.txt | awk '{print $1}' | sort -u > out/cls_hits${c}_mine.txt; bin/r3canon HIT 16 < out/hits${c}_ext_indep2.txt | awk '{print $1}' | sort -u > out/cls_hits${c}_authors.txt; cmp out/cls_hits${c}_mine.txt out/cls_hits${c}_authors.txt; done
# 7. witness, judge, controls
(cd out && python3 $P/witness_16.py); (cd /home/user/Erdos-757 && python3 judge/judge.py experiments/referee/L008-round3/out/r3-C16-check.json)
bin/filter_hits C < out/controls.txt
# 8. K8-free Lemma A' (optional): the 38 cheap cells (see review table) and the (15,13,>=7) O+ cell
TAU0=7 F7PRUNE=1 P3PRUNE=1 bin/genbg_r3 -u -q -c -Z1 -d1:3 -D13:3 15 13 39:39
