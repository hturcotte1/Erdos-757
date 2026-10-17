#!/bin/bash
# Referee L011 r2: enumerate connected linear (n,m,>=t) 3-graphs with max degree <= D with genbg + own hook.
# Usage: bash src/cells.sh "n m t D" ...   Output out/g_n_m_t_dD.txt, stderr logs/g_n_m_t_dD.err
cd "$(dirname "$0")/.."
for c in "$@"; do set -- $c; n=$1; m=$2; t=$3; D=$4
  s=$(date +%s)
  TAU0=$t nice -n 5 ./bin/genbg_h -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) > out/g_${n}_${m}_${t}_d$D.txt 2> logs/g_${n}_${m}_${t}_d$D.err
  echo "($n,$m,$t) D<=$D: classes=$(wc -l < out/g_${n}_${m}_${t}_d$D.txt) $(grep HSUM logs/g_${n}_${m}_${t}_d$D.err) wall=$(( $(date +%s)-s ))s"
done
