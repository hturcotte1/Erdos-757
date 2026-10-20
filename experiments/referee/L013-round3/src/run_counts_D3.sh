#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L013-round3
for c in "22 12" "22 13" "23 11" "23 12" "24 13"; do set -- $c; s=$(date +%s); r=$(nice -n 10 timeout 900 ./bin/genbg -c -Z1 -d3:1 -D3:3 -u $2 $1 $((3*$2)):$((3*$2)) 2>&1 | tail -1); e=$(date +%s); echo "count ($1,$2) D<=3 (swapped): $r [$((e-s))s]"; done
