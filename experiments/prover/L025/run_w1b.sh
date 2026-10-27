#!/bin/bash
# Re-runs writing to a scratch folder outside the repository (tracked output files in the repository were
# replaced under the running processes by other agents' 'git pull --rebase --autostash', which lost output);
# the outputs are copied into this folder afterwards.
cd "$(dirname "$0")"
OUT=/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad/L025run
O=../L017/out
timeout 1800 nice -n 10 python3 lemmas25.py file:$O/L014/cells/cell_5_2_1_D3.txt file:$O/L014/cells/cell_7_5_2_D3.txt file:$O/L014/cells/cell_10_6_3_D3.txt file:$O/L014/cells/cell_13_7_4_D3.txt file:$O/L014/cells/cell_16_8_5_D3.txt file:$O/L014/cells/cell_19_9_6_D3.txt --hubsample 10 > $OUT/lemmas_slack89_output.txt 2>&1
echo "exit $?" >> $OUT/lemmas_slack89_output.txt
timeout 3000 nice -n 10 python3 w1_pendant.py $O/L014/cells/cell_5_2_1_D3.txt $O/L014/cells/cell_7_5_2_D3.txt $O/L014/cells/cell_10_6_3_D3.txt $O/L014/cells/cell_13_7_4_D3.txt $O/L014/cells/cell_16_8_5_D3.txt $O/L014/cells/cell_19_9_6_D3.txt $O/L012/cells/cell_7_4_2_D3.txt $O/L012/cells/cell_10_5_3_D3.txt $O/L014/cells/cell_11_9_4_D3.txt $O/L012/cells/cell_13_6_4_D3.txt $O/L014/cells/cell_20_12_7_D3.txt $O/L014/cells/cell_14_10_5_D3.txt $O/L014/cells/cell_17_11_6_D3.txt > $OUT/w1_output.txt 2>&1
echo "exit $?" >> $OUT/w1_output.txt
