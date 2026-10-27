#!/bin/bash
# Referee L019: re-run a subset of the prover's computations (copies of the prover's scripts, unmodified) and diff.
D=/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs
cd /home/user/Erdos-757/experiments/referee/L019-round1-opus/rerun
timeout 1500 nice -n 10 python3 check_folding.py random 3000 1 > check_folding_rerun.txt
for c in 10_7_4 12_10_5 14_12_6 15_11_6 17_13_7 13_9_5 10_8_4; do
  timeout 900 nice -n 10 python3 check_folding.py cell $D/cell_$c.txt 40 >> check_folding_rerun.txt
done
for c in 10_7_4 14_12_6 17_13_7 12_10_5 15_11_6; do
  timeout 1500 nice -n 10 python3 fold_block_stats.py $D/cell_$c.txt 12 >> fold_block_stats_rerun.txt
done
timeout 300 nice -n 10 python3 fold_violators.py > fold_violators_rerun.txt
for c in 10_7_4 14_12_6 17_13_7 12_10_5 15_11_6 22_17_9 26_22_11; do
  timeout 1500 nice -n 10 python3 fold_pergraph.py $D/cell_$c.txt 300 >> fold_pergraph_rerun.txt
done
timeout 900 nice -n 10 python3 fold_reasons_graph.py $D/cell_14_12_6.txt 4,8 > fold_reasons_graph_rerun.txt
timeout 900 nice -n 10 python3 fold_reasons_graph.py $D/cell_10_8_4.txt 39,40,60 > fold_reasons_10_8_4_rerun.txt
for c in 10_8_4 14_12_6 12_10_5 23_21_10; do
  timeout 1800 nice -n 10 python3 blocked_and_6b.py $D/cell_$c.txt 100000 >> blocked_and_6b_rerun.txt
done
for c in 17_13_7 15_11_6; do
  timeout 1800 nice -n 10 python3 nbhd_cover.py $D/cell_$c.txt 100000 >> nbhd_cover_rerun.txt
done
# timing probe of the (26,22,11) C8 run: one class, 600 s limit
( time timeout 600 nice -n 10 python3 nbhd_cover.py $D/cell_26_22_11.txt 1 ) >> nbhd_cover_26_probe.txt 2>&1; echo "exit status $?" >> nbhd_cover_26_probe.txt
echo done > rerun.done
