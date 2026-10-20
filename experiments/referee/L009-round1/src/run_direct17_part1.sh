#!/bin/bash
# Referee L009: part 1/2 of the direct genbg enumeration of connected linear (17,13,tau>=7) 3-graphs with max degree <= 3
# (part 0/2 was started by run_direct17.sh with identical arguments).
cd /home/user/Erdos-757/experiments/referee/L009-round1
s=$(date +%s); TAU0=7 timeout 5000 nice -n 5 ./bin/genbg_ref -c -Z1 -d1:3 -D3:3 -X-3 17 13 39:39 1/2 2> out/err_17_13_7_part1.txt > out/g_17_13_7_part1.txt; echo "part 1 rc=$? wall=$(( $(date +%s) - s )) s" >> out/direct17_status.txt
