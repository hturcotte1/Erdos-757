#!/bin/bash
# Referee round 2 (L008): class-set comparison of the prover's enum_conn (canonical BFS growth) with bfs_enum (generate and
# deduplicate) on intermediate cells n = 10..13 (beyond labelled brute force), D in {3, inf}, thresholds T0 = lo-1, lo-2.
cd /home/user/Erdos-757/experiments/referee/L008-round2
tot=0; bad=0
for n in 10 11 12 13; do for m in $(seq $(( n / 2 )) $(( n - 2 ))); do
  [ $n -gt $((2*m+1)) ] && continue
  lo=$(( (3*n+2*m)/11 + 1 ))
  for t in $((lo-1)) $((lo-2)); do [ $t -lt 1 ] && continue
    for D in 3 100; do
      timeout 120 ./rerun/bin/enum_conn $n $m $t $D 1 > out/tmp_ec.txt || { echo "TIMEOUT enum_conn $n $m $t $D"; continue; }
      timeout 120 ./bin/bfs_enum $n $m $t $D 1 1 > out/tmp_bfs.txt 2>/dev/null || { echo "TIMEOUT bfs $n $m $t $D"; continue; }
      a=$(./bin/canon_list FOUND $n < out/tmp_ec.txt | awk '{print $1}' | sort -u | md5sum); b=$(./bin/canon_list FOUND $n < out/tmp_bfs.txt | awk '{print $1}' | sort -u | md5sum)
      c=$(grep -c FOUND out/tmp_bfs.txt); tot=$((tot+1))
      if [ "$a" != "$b" ]; then bad=$((bad+1)); echo "MISMATCH n=$n m=$m t=$t D=$D"; fi
      echo "n=$n m=$m t>=$t D=$D classes=$c"
    done; done; done; done
echo "cells compared: $tot mismatches: $bad"
