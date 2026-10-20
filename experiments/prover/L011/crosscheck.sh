#!/bin/bash
# (L011) Cross-checks of ext_indep5 against the falsifier's ext_vertex2 (different tau test) on random input samples; usage: crosscheck.sh NAME NG TG
cd /home/user/Erdos-757/experiments/prover/L011
n=$1; NG=$2; TG=$3; s=$(date +%s)
./bin/ext_vertex2 $NG $((TG+1)) 3 < out/s$n.txt > out/hits_s${n}_ev2.txt
./indep/ext_indep5 $NG $TG 3 < out/s$n.txt > out/hits_s${n}_mine.txt
e=$(date +%s)
echo "$n ev2: $(tail -n 1 out/hits_s${n}_ev2.txt) | mine: $(tail -n 1 out/hits_s${n}_mine.txt) | $(python3 compare_hits.py out/hits_s${n}_ev2.txt out/hits_s${n}_mine.txt) [$((e-s)) s]" > out/cross_$n.done
