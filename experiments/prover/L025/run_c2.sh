#!/bin/bash
# C2 runs (sequential, one process at a time)
cd "$(dirname "$0")"
I=../../20261027-0300-transversal-richness/inputs
O=../L017/out/L013/cells
timeout 4200 nice -n 10 python3 lemmas25.py file:$I/cell_6_3_2.txt file:$I/cell_9_4_3.txt file:$I/cell_10_8_4.txt file:$I/cell_13_9_5.txt file:$I/cell_16_10_6.txt file:$I/cell_23_16_9.txt file:$I/cell_20_15_8.txt file:$I/cell_17_14_7.txt --hubsample 10 > lemmas_slack2_output.txt 2>&1
timeout 3000 nice -n 10 python3 lemmas25.py file:$O/cell_11_6_4_D3.txt file:$O/cell_12_6_4_D3.txt file:$O/cell_13_6_4_D3.txt file:$O/cell_11_7_4_D3.txt file:$O/cell_14_7_5_D3.txt file:$O/cell_15_8_5_D3.txt file:$O/cell_18_9_6_D3.txt file:$O/cell_19_12_7_D3.txt file:$O/cell_12_7_4_D3.txt file:$O/cell_13_8_5_D3.txt --hubsample 10 > lemmas_highslack_output.txt 2>&1
