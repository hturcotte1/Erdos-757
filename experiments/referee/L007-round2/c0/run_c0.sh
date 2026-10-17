#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L007-round2/c0/indep
s=$(date +%s)
for n in 3 4 5 6 7 8 9; do ./bf_cells $n > bf_n$n.txt; done
for n in 3 4 5 6 7 8 9; do cmp bf_n$n.txt /home/user/Erdos-757/experiments/prover/L007/indep/bf_n$n.txt && echo "bf_n$n identical"; done > bf_cmp.log 2>&1
e=$(date +%s); echo "bf_cells elapsed $((e-s)) s" >> bf_cmp.log
s=$(date +%s); python3 compare_bf.py mine > compare_mine.log 2>&1; e=$(date +%s); echo "elapsed $((e-s)) s" >> compare_mine.log
s=$(date +%s); python3 compare_bf.py theirs > compare_theirs.log 2>&1; e=$(date +%s); echo "elapsed $((e-s)) s" >> compare_theirs.log
