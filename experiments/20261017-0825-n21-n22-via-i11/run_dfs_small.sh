#!/bin/bash
cd /home/user/Erdos-757/experiments/20261017-0825-n21-n22-via-i11
for c in "21 11 8 2" "21 12 8 2" "20 14 8 2"; do
  s=$(date +%s); nice -n 10 ./conn_dfs3 $c 0 0 > out/D_$(echo $c|tr ' ' '_').txt; e=$(date +%s); echo "$c secs=$((e-s)) $(tail -1 out/D_$(echo $c|tr ' ' '_').txt | cut -c1-200)" >> dfs_small.log
done
