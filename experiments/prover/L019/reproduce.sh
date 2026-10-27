#!/bin/bash
# L019 computations (illustrative; exact integer arithmetic; 1 process; run from this directory).
set -e
D=/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs
# C1: folding lemma (Theorem 5) on random linear 3-graphs and on stored class-C lists
timeout 900 nice -n 10 python3 check_folding.py random 3000 1                         > check_folding_output.txt
for c in 10_7_4 12_10_5 14_12_6 15_11_6 17_13_7 13_9_5 10_8_4; do
  timeout 900 nice -n 10 python3 check_folding.py cell $D/cell_$c.txt 40             >> check_folding_output.txt
done
# C2: why folds leave C; tight-set criterion of Theorem 5(d)
for c in 10_7_4 14_12_6 17_13_7 12_10_5 15_11_6; do
  timeout 1500 nice -n 10 python3 fold_block_stats.py $D/cell_$c.txt 12               >> fold_block_stats_output.txt
done
# C3: folds of the small linear vertex-critical violators (F7, two (9,8,4))
timeout 300 nice -n 10 python3 fold_violators.py                                      > fold_violators_output.txt
# C4/C5: degree-2 vertices whose four folds all leave C; per-graph counts
for c in 10_7_4 14_12_6 17_13_7 12_10_5 15_11_6 19_16_8; do
  timeout 1200 nice -n 10 python3 fold_allblocked.py $D/cell_$c.txt 30                >> fold_allblocked_output.txt
done
for c in 10_7_4 14_12_6 17_13_7 12_10_5 15_11_6 22_17_9 26_22_11; do
  timeout 1500 nice -n 10 python3 fold_pergraph.py $D/cell_$c.txt 300                 >> fold_pergraph_output.txt
done
# C6: the two (14,12,6) classes with Delta = 3: every fold at every degree-2 vertex is blocked by adjacency/common neighbour
timeout 900 nice -n 10 python3 fold_reasons_graph.py $D/cell_14_12_6.txt 4,8         > fold_reasons_graph_output.txt
# C7: graphs with degrees in {2,3} satisfying Theorem 6(b) at every degree-2 vertex and having every fold blocked
for c in 10_7_4 14_12_6 17_13_7 12_10_5 15_11_6 19_16_8 22_17_9 26_22_11 10_8_4 13_9_5 16_10_6 17_14_7 20_15_8 23_16_9 8_5_3 9_4_3 6_3_2; do
  timeout 1800 nice -n 10 python3 blocked_and_6b.py $D/cell_$c.txt 100000            >> blocked_and_6b_output.txt
done
timeout 900 nice -n 10 python3 fold_reasons_graph.py $D/cell_10_8_4.txt 39,40,60       > fold_reasons_10_8_4_output.txt
# C8 timeout raised to 5400 s after round 1; the (26,22,11) step, timed alone once, took 4 min 54 s.
for c in 17_13_7 15_11_6 22_17_9 26_22_11; do
  timeout 5400 nice -n 10 python3 nbhd_cover.py $D/cell_$c.txt 100000                 >> nbhd_cover_output.txt
done
