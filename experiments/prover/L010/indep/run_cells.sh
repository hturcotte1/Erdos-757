#!/bin/bash
# enumerations for certificate L010 with the prover's enum_conn (L007); prints the last output line and wall time of each run
cd /home/user/Erdos-757/experiments/prover/L010/indep
run() { local out=$1; shift; s=$(date +%s); ./enum_conn "$@" > ../out/$out; e=$(date +%s); echo "enum_conn $* -> $(tail -n 1 ../out/$out) [$((e-s)) s]"; }
run cell_8_6_3.txt 8 6 3 3 1
run cell_9_4_3.txt 9 4 3 3 1
run cell_11_6_4.txt 11 6 4 3 1
run cell_11_7_4.txt 11 7 4 3 1
run cell_14_8_5.txt 14 8 5 3 1
run cell_17_9_6.txt 17 9 6 3 1
run cell_16_9_6.txt 16 9 6 3 1
run win_19_9_7_anydeg.txt 19 9 7 1000 0
run win_19_10_7_deg3.txt 19 10 7 3 0
run win_20_12_8_deg2.txt 20 12 8 2 0
run win_18_12_7_deg2.txt 18 12 7 2 0
run win_20_13_8_deg2.txt 20 13 8 2 0
