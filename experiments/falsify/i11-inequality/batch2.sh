#!/bin/bash
cd /home/user/Erdos-757/experiments/falsify/i11-inequality
for c in "8 4 3" "10 6 4" "11 5 4" "13 7 5" "12 9 5" "15 9 6" "15 10 6" "16 8 6" "17 12 7" "18 10 7" "18 11 7" "19 9 7" "16 13 7" "16 14 7"; do
  timeout 3000 nice -n 5 ./conn_dfs2 $c >> conn2_batch.log 2>&1 ; [ $? -ne 0 ] && echo "TIMEOUT/INCOMPLETE $c" >> conn2_batch.log
done
