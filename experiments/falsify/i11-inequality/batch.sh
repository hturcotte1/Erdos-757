#!/bin/bash
cd /home/user/Erdos-757/experiments/falsify/i11-inequality
for c in "15 9 6" "15 10 6" "19 9 7" "18 10 7" "18 11 7"; do
  timeout 1800 nice -n 5 ./conn_dfs $c >> conn_batch.log 2>&1 || echo "TIMEOUT/INCOMPLETE $c" >> conn_batch.log
done
