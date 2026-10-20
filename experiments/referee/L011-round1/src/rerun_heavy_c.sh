#!/bin/bash
# Referee L011: re-run (copies of the prover's programs) of C6 parts 01-03 and C8 parts 00-02 (+ F7/P3 filter).
cd /home/user/Erdos-757/experiments/referee/L011-round1/out/rerun
for p in 01 02 03; do s=$(date +%s); ./bin/ext_indep5 20 8 3 < out/in21_17_part$p > out/hits21_17_part$p.txt; echo "C6 part$p: $(tail -n 1 out/hits21_17_part$p.txt) [$(( $(date +%s) - s )) s]"; done
