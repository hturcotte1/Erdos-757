#!/bin/bash
# Reproduction of every computation cited in results/proofs/L007-no-nonsaturated-extremal-14-point-sets.md.
# Run from this directory.  F = the falsifier folder whose C sources are recompiled here (their binaries are not used).
set -e
F=/home/user/Erdos-757/experiments/falsify/i11-inequality
mkdir -p bin rerun
# --- arithmetic (Steps 1 and 4) ---
python3 cells.py 16                    # window cells, slack-0 and slack-1 cells
python3 cells_table.py 15              # the table of Step 1
# --- falsifier programs, recompiled from source, re-run (C1, C2, C4, C5, C6) ---
gcc -O2 -o bin/conn_dfs2 $F/conn_dfs2.c; gcc -O2 -o bin/conn_dfs2_all $F/conn_dfs2_all.c; gcc -O2 -o bin/ext_vertex_all $F/ext_vertex_all.c
for c in "5 3 2" "8 4 3" "10 6 4" "11 5 4" "13 7 5" "12 9 5"; do ./bin/conn_dfs2 $c | tail -n 1; done > rerun/window_cells_n13.log
./bin/conn_dfs2_all 10 7 4 > rerun/conn_all_10_7_4.txt; ./bin/conn_dfs2_all 13 8 5 > rerun/conn_all_13_8_5.txt
cmp rerun/conn_all_10_7_4.txt $F/conn_all_10_7_4.txt; cmp rerun/conn_all_13_8_5.txt $F/conn_all_13_8_5.txt
python3 build_input.py                 # rebuilds the 796-line extension input; equal (as a multiset) to $F/ext_vertex_input.txt
./bin/ext_vertex_all < $F/ext_vertex_input.txt > rerun/ext_vertex_hits.txt; cmp rerun/ext_vertex_hits.txt $F/ext_vertex_hits.txt
./bin/conn_dfs2 15 9 6 | tail -n 1; ./bin/conn_dfs2 16 8 6 | tail -n 1; ./bin/conn_dfs2 15 10 6 | tail -n 1     # remark cells (165 s for the last)
./bin/conn_dfs2_all 14 11 6 3 > rerun/conn2_all_14_11_6_deg3.txt                                           # Route II (several minutes)
# --- independent prover programs (C0-C5) ---
cd indep
gcc -O2 -Wall -o enum_conn enum_conn.c; gcc -O2 -o bf_cells bf_cells.c; gcc -O2 -Wall -o ext_indep ext_indep.c
for n in 3 4 5 6 7 8 9; do ./bf_cells $n > bf_n$n.txt; done        # brute force (n=9: about 1 min)
python3 compare_bf.py mine; python3 compare_bf.py theirs           # completeness validation, n <= 9 (about 6 min each)
gcc -O2 -o bf_cell bf_cell.c; for c in "10 6 4" "10 7 4" "11 5 4"; do ./bf_cell $c; done > bf_cell_n10_11.log   # direct brute force (about 2 min)
for c in "15 9 6" "16 8 6"; do ./enum_conn $c 1000 0 | tail -n 1; done > enum_remark_small.log; ./enum_conn 15 10 6 1000 0 > enum_15_10_6.log   # remark cells
for c in "5 3 2" "8 4 3" "10 6 4" "11 5 4" "13 7 5" "12 9 5"; do ./enum_conn $c 1000 0 | tail -n 1; done
./enum_conn 10 7 4 1000 1 > mine_10_7_4.txt; ./enum_conn 13 8 5 1000 1 > mine_13_8_5.txt
python3 iso_compare.py mine_10_7_4.txt ../rerun/conn_all_10_7_4.txt details; python3 iso_compare.py mine_13_8_5.txt ../rerun/conn_all_13_8_5.txt details
./ext_indep < ../rerun/ext_input_rebuilt.txt > ext_indep_hits.txt; python3 compare_hits.py; python3 hits_breakdown.py
./enum_conn 14 11 6 3 1 > mine_14_11_6_deg3.txt                    # Route II, independent (several minutes)
python3 iso_compare.py mine_14_11_6_deg3.txt ../rerun/conn2_all_14_11_6_deg3.txt; python3 member.py mine_14_11_6_deg3.txt ../rerun/conn2_all_14_11_6_deg3.txt
python3 f7check.py ext_indep_hits.txt:HIT ../rerun/ext_vertex_hits.txt:HIT ../rerun/conn_all_13_8_5.txt:FOUND ../rerun/conn_all_10_7_4.txt:FOUND \
   ../rerun/conn2_all_14_11_6_deg3.txt:FOUND mine_14_11_6_deg3.txt:FOUND mine_13_8_5.txt:FOUND mine_10_7_4.txt:FOUND
cd ..
python3 witness_14_11.py; python3 check_witness_records.py; python3 sanity_m11_sets.py 200
# SAT cross-check of three window cells in the ordered class O (falsifier's script, run from its folder; 0.1 s, 41 s, 144 s here)
(cd $F && for c in "8 4 3" "10 6 4" "11 5 4"; do python3 sat_cell.py $c | tail -n 1; done) > rerun/sat_cells.log
