#!/bin/bash
# referee L019: folding-lemma test on the remaining stored cells and on random linear 3-graphs (one process at a time)
D=/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs
cd /home/user/Erdos-757/experiments/referee/L019-round1-opus
for spec in 10_7_4:300 14_12_6:300 17_13_7:300 12_10_5:300 15_11_6:300 13_9_5:300 10_8_4:300 16_10_6:300 8_5_3:300 9_4_3:300 6_3_2:300 17_14_7:80 19_16_8:40 20_15_8:40 22_17_9:25 23_16_9:12 23_21_10:12 26_22_11:6; do
  c=${spec%%:*}; K=${spec##*:}
  timeout 1500 nice -n 10 python3 test_fold.py cells $D/cell_$c.txt $K
done
timeout 1500 nice -n 10 python3 test_fold.py random 2500 7
