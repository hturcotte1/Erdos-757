#!/bin/bash
R=/home/user/Erdos-757/experiments/referee/L007-round2
F=/home/user/Erdos-757/experiments/falsify/i11-inequality
cd $R
{ for c in "10 6 4" "11 5 4" "10 7 4"; do s=$(date +%s); ./rerun/bf_cell $c; e=$(date +%s); echo "  wall $((e-s)) s"; done; } > misc/bf_cell.log 2>&1
{ for c in "15 9 6" "16 8 6" "15 10 6"; do s=$(date +%s); ./rerun/conn_dfs2 $c | tail -n 1; e=$(date +%s); echo "  wall $((e-s)) s"; done;
  for c in "15 9 6" "16 8 6" "15 10 6"; do s=$(date +%s); ./rerun/enum_conn $c 1000 0 | tail -n 1; e=$(date +%s); echo "  wall $((e-s)) s"; done; } > misc/c6.log 2>&1
{ cd $F; for c in "8 4 3" "10 6 4" "11 5 4"; do s=$(date +%s); python3 -B sat_cell.py $c | tail -n 1; e=$(date +%s); echo "  wall $((e-s)) s"; done; cd $R; } > misc/sat_cell.log 2>&1
cd $R/misc && python3 -B check_witness_records.py > check_witness_records.log 2>&1; python3 -B witness_14_11.py > witness_14_11.log 2>&1
echo done > $R/misc/DONE
