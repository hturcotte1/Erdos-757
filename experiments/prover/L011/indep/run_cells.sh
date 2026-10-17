#!/bin/bash
# Enumerations for certificate L011 with the prover's enum_conn (L007, unchanged); prints the last output line and wall time of each run.
# Usage: run_cells.sh LIST   (LIST = small | long1 | long2)
cd /home/user/Erdos-757/experiments/prover/L011/indep
run() { local out=$1; shift; s=$(date +%s); ./enum_conn "$@" > ../out/$out; e=$(date +%s); echo "enum_conn $* -> $(tail -n 1 ../out/$out) [$((e-s)) s]"; }
case "$1" in
small)
  run cell_6_3_2.txt 6 3 2 3 1
  run cell_8_5_3.txt 8 5 3 3 1
  run cell_8_6_3.txt 8 6 3 3 1
  run cell_9_4_3.txt 9 4 3 3 1
  run cell_10_7_4.txt 10 7 4 3 1
  run cell_10_8_4.txt 10 8 4 3 1
  run cell_11_6_4.txt 11 6 4 3 1
  run cell_11_7_4.txt 11 7 4 3 1
  run cell_13_8_5.txt 13 8 5 3 1
  run cell_13_9_5.txt 13 9 5 3 1
  run cell_14_7_5.txt 14 7 5 3 1
  run cell_14_8_5.txt 14 8 5 3 1
  run cell_16_9_6.txt 16 9 6 3 1
  run cell_17_8_6.txt 17 8 6 3 1
  run cell_17_9_6.txt 17 9 6 3 1
  run cell_19_10_7.txt 19 10 7 3 1
  run cell_20_10_7.txt 20 10 7 3 1
  run win_21_11_8_deg2.txt 21 11 8 2 0
  run win_21_12_8_deg2.txt 21 12 8 2 0
  run win_20_14_8_deg2.txt 20 14 8 2 0
  run cell_16_10_6.txt 16 10 6 3 1
  ;;
long1)
  run cell_19_11_7.txt 19 11 7 3 1
  ;;
long2)
  run win_21_13_8_deg2.txt 21 13 8 2 0
  ;;
esac
