#!/bin/bash
# Referee L007 round 3: every command run for the review (from this directory). Nice 5, <= 2 processes.
set -e
P=/home/user/Erdos-757/experiments/prover/L007; F=/home/user/Erdos-757/experiments/falsify/i11-inequality
python3 cells_ref3.py                                    # Step 1 / 4.3 / 4.4 / 3.2 / 8.3 arithmetic
gcc -O2 -Wall -o levelgen levelgen.c; gcc -O2 -Wall -o bfref bfref.c; gcc -O2 -Wall -o canonfile canonfile.c; gcc -O2 -o ext_ref ext_ref.c
for n in 3 4 5 6 7 8 9; do ./bfref $n > bf_ref_n$n.txt; done   # own labelled brute force (n=9: 14 s)
python3 compare_ref.py 9                                 # levelgen vs bfref: 41 cells + 447 pruned runs
for c in "5 3 2" "8 4 3" "10 6 4" "11 5 4" "13 7 5" "12 9 5"; do ./levelgen $c 100 0 1 > out/win_$(echo $c|tr ' ' _).txt; done
./levelgen 10 7 4 100 0 1 > out/tight_10_7_4.txt; ./levelgen 13 8 5 100 0 1 > out/tight_13_8_5.txt
./levelgen 14 11 6 3 0 1 > out/route2_14_11_6_d3.txt      # 32 s
./levelgen 14 11 6 100 1 1 > out/direct_14_11_6_f7free.txt # 58 s, F7-pruned, no degree bound
./levelgen 14 11 6 100 0 1 > out/all_14_11_6.txt           # 55 s
# Lemma A without K8: all connected cells n<=13, m<=n-2, lo<=m, F7-pruned (out/lemmaA_noHY.txt)
for n in $(seq 3 13); do for m in $(seq $(( n/2 )) $((n-2))); do [ $n -le $((2*m+1)) ] || continue; lo=$(( (3*n+2*m)/11 + 1 )); [ $lo -le $m ] || continue; echo "$n $m $lo :: $(./levelgen $n $m $lo 100 1 0 | grep FINAL)"; done; done > out/lemmaA_noHY.txt
python3 reff7.py; python3 f7_agree.py; python3 f7_classes.py out/tight_13_8_5.txt out/tight_10_7_4.txt out/route2_14_11_6_d3.txt out/all_14_11_6.txt
(grep CLASS out/tight_13_8_5.txt; grep CLASS out/tight_10_7_4.txt | sed 's/$/ (10,11,12)/') > out/ext_input_classes.txt
./ext_ref < out/ext_input_classes.txt > out/ext_ref_hits.txt; ./canonfile < out/ext_ref_hits.txt | sort -u > out/ext_ref_hit_classes.txt
for f in $P/indep/ext_indep_hits.txt $P/rerun/ext_vertex_hits.txt $F/ext_vertex_hits.txt; do grep HIT $f | ./canonfile | sort -u | cmp - out/ext_ref_hit_classes.txt; done
python3 hits_check.py $P/indep/ext_indep_hits.txt; python3 check_sets.py; python3 check_d14.py
python3 xval.py "10 7 3 100" "10 6 3 100" "10 8 4 100" "11 7 4 100" "11 8 4 100" "11 9 4 100" "12 8 4 100" "12 9 4 3"   # (first run, capped at 590 s)
python3 xval.py "12 10 5 3" "13 9 5 100" "13 10 6 100" "13 8 4 3"
for c in "15 9 6 100" "16 8 6 100" "15 10 6 100"; do ./levelgen $c 0 0 | grep FINAL; done
# authors' programs, recompiled into rerun/ from their sources (see rerun/src), outputs in rerun/out, rerun/c0, rerun/c7
