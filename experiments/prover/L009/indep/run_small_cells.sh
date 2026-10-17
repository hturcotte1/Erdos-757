#!/bin/bash
# component and window-cell enumerations for L009 (prover's enum_conn); each line: command and its last output line, plus wall time
cd /home/user/Erdos-757/experiments/prover/L009/indep
run() { s=$(date +%s); ./enum_conn "$@" > "$OUT"; e=$(date +%s); echo "enum_conn $* -> $(tail -n 1 $OUT) [$((e-s)) s]"; }
OUT=cell_6_3_2.txt;   run 6 3 2 3 1
OUT=cell_8_5_3.txt;   run 8 5 3 3 1
OUT=cell_10_7_4.txt;  run 10 7 4 3 1
OUT=cell_10_8_4.txt;  run 10 8 4 3 1
OUT=cell_13_8_5.txt;  run 13 8 5 3 1
OUT=cell_13_9_5.txt;  run 13 9 5 3 1
OUT=cell_16_9_6_deg3.txt;  run 16 9 6 3 0
OUT=cell_16_9_6_anydeg.txt; run 16 9 6 1000 0
OUT=cell_18_10_7_anydeg.txt; run 18 10 7 1000 0
OUT=cell_16_10_6.txt; run 16 10 6 3 1
OUT=cell_18_11_7_deg3.txt; run 18 11 7 3 0
