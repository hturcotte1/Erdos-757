#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L007-round2
s=$(date +%s)
./rerun/enum_conn 14 11 6 3 1 > rerun/mine_14_11_6_deg3.txt
e=$(date +%s)
echo "elapsed_s=$((e-s))" > rerun/mine_14_11_6_deg3.time
