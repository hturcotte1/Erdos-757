#!/bin/bash
# Commands used (run from this directory; PYTHONPATH not needed, scripts add the repo root).  nice -n 5 everywhere.
gcc -O2 -march=native -o subsets subsets.c          # exhaustive subset engine (n<=26)
python3 sanity.py                                   # C engine == e757.core.alpha on all subsets of A_base and 12b
python3 test1.py                                    # T1: all subsets of the 7 small_records sets
python3 test23.py n14; python3 test23.py n12        # T2, T3 (all 2,910 / all 54,243)
python3 test23.py small; python3 test23.py abs12; python3 test23.py abs14   # extra: realizable n<=11 classes, abstract (12,10) and (14,12) censuses
python3 test4.py                                    # T4: lp-fit dataset
python3 test6.py; python3 test6b.py                 # T6: Fibonacci, gluings
python3 amalgam.py                                  # one-point amalgams
python3 ext_gen.py n14 EXT14.txt 2; python3 run_c_file.py EXT14.txt ext14_single           # all 141,153 single-point (4,5)-extensions of the 2,910 classes
python3 ext_gen.py n12s54243 EXT12.txt 1; python3 run_c_file.py EXT12.txt ext12_single_all  # all 1,887,566 single-point extensions of the 54,243 classes
python3 abstract_table.py; python3 hist_union.py; python3 frontier_lp.py; python3 polygon.py # O' tables, tau_max union, exact LP polygon
# abstract-class exhaustive cells (connected, unordered linear 3-graphs, strictly larger than class O)
gcc -O2 -o conn_dfs2 conn_dfs2.c; gcc -O2 -o conn_dfs_all conn_dfs.c; python3 isocheck.py   # v1 vs v2 iso-class agreement
python3 verify_cells.py 13
./conn_dfs2 15 9 6; ./conn_dfs2 15 10 6; ./conn_dfs2 16 8 6
# (14,11,6) by vertex extension of the slack-0 (13,8,5) graphs
gcc -O2 -o conn_dfs2_all conn_dfs2_all.c; ./conn_dfs2_all 10 7 4 > conn_all_10_7_4.txt; ./conn_dfs2_all 13 8 5 > conn_all_13_8_5.txt
gcc -O2 -o ext_vertex_all ext_vertex_all.c; ./ext_vertex_all < ext_vertex_input.txt > ext_vertex_hits.txt; python3 analyze_hits.py; python3 crosscheck_ext.py
# independent route: direct DFS with max degree 3
./conn_dfs2_all 14 11 6 3 > conn2_all_14_11_6_deg3.txt; python3 ud_check.py
# SAT (cadical) cells for the ordered class O
python3 sat_cell.py 10 6 4; python3 sat_cell.py 11 5 4; python3 sat_cell.py 8 4 3
