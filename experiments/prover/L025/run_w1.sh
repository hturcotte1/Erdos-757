#!/bin/bash
# follow-up runs (sequential, one process at a time):
#  (1) C2 on the slack-2 cell (17,14,7) (the first run stopped before it without output),
#  (2) C2 on slack-8/9 cells (Lemma 6 needs avoided triples),
#  (3) W1 consistency test.
cd "$(dirname "$0")"
I=../../20261027-0300-transversal-richness/inputs
O=../L017/out
timeout 2400 nice -n 10 python3 lemmas25.py file:$I/cell_17_14_7.txt --hubsample 10 > lemmas_slack2_17_14_7_output.txt 2>&1
echo "exit $?" >> lemmas_slack2_17_14_7_output.txt
timeout 1800 nice -n 10 python3 lemmas25.py file:$O/L014/cells/cell_5_2_1_D3.txt file:$O/L014/cells/cell_7_5_2_D3.txt file:$O/L014/cells/cell_10_6_3_D3.txt file:$O/L014/cells/cell_13_7_4_D3.txt file:$O/L014/cells/cell_16_8_5_D3.txt file:$O/L014/cells/cell_19_9_6_D3.txt --hubsample 10 > lemmas_slack89_output.txt 2>&1
echo "exit $?" >> lemmas_slack89_output.txt
timeout 2400 nice -n 10 python3 w1_pendant.py $O/L014/cells/cell_5_2_1_D3.txt $O/L014/cells/cell_7_5_2_D3.txt $O/L014/cells/cell_10_6_3_D3.txt $O/L014/cells/cell_13_7_4_D3.txt $O/L014/cells/cell_16_8_5_D3.txt $O/L014/cells/cell_19_9_6_D3.txt $O/L012/cells/cell_7_4_2_D3.txt $O/L012/cells/cell_10_5_3_D3.txt $O/L014/cells/cell_11_9_4_D3.txt $O/L012/cells/cell_13_6_4_D3.txt $O/L014/cells/cell_20_12_7_D3.txt $O/L014/cells/cell_14_10_5_D3.txt $O/L014/cells/cell_17_11_6_D3.txt > w1_output.txt 2>&1
echo "exit $?" >> w1_output.txt
