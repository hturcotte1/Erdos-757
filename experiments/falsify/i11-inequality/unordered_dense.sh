#!/bin/bash
cd /home/user/Erdos-757/experiments/falsify/i11-inequality
for c in "9 8 4" "10 12 5" "11 10 5" "12 14 6" "13 13 6" "11 16 6" "12 20 7" "13 18 7" "13 24 8"; do
  echo "== $c" >> unordered_dense.log
  timeout 600 nice -n 5 ./conn_dfs2_all $c > ud_$(echo $c|tr ' ' '_').txt 2>&1; echo "exit $?" >> unordered_dense.log; tail -1 ud_$(echo $c|tr ' ' '_').txt >> unordered_dense.log
done
