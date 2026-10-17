#!/bin/bash
# Referee L009: direct orderly generation (nauty genbg + referee tau-prune) of ALL connected linear 3-graphs with
# 17 vertices, 13 edges, max degree <= 3 and tau >= 7, split into 2 parts (split level moved up by -X-3), run sequentially.
cd /home/user/Erdos-757/experiments/referee/L009-round1
for r in 0 1; do
  s=$(date +%s); TAU0=7 timeout 5400 nice -n 5 ./bin/genbg_ref -c -Z1 -d1:3 -D3:3 -X-3 17 13 39:39 $r/2 2> out/err_17_13_7_part$r.txt > out/g_17_13_7_part$r.txt; echo "part $r rc=$? wall=$(( $(date +%s) - s )) s" >> out/direct17_status.txt
done
echo ALLDONE >> out/direct17_status.txt
