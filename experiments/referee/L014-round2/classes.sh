#!/bin/bash
# Referee L014 round 2: classes.sh n m OUT FILE...  -> OUT = sorted distinct labelg canonical forms (own nauty build, partition
# 'a'*n 'b'*m keeps vertices and edges apart) of all hypergraphs in FILE... (formats of hg2g6).  Prints the number of graphs and classes.
set -o pipefail
H=/home/user/Erdos-757/experiments/referee/L014-round2
n=$1; m=$2; out=$3; shift 3
part=$(printf 'a%.0s' $(seq 1 $n))$(printf 'b%.0s' $(seq 1 $m))
cat "$@" | grep -E '^(MEMBER|FOUND:|[0-9])' | $H/bin/hg2g6 $n | $H/out/nbin/labelg -q -f$part | LC_ALL=C sort -u -S 1500M -T $H/out > $out
echo "classes.sh n=$n m=$m files=$* classes=$(wc -l < $out)"
