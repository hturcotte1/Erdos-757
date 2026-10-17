#!/bin/bash
# Referee L012: direct enumeration of cells with unmodified nauty genbg (connected, C4-free bipartite incidence graphs = connected
# linear 3-graphs; first class = vertices with degree 1..D, second class = edges of degree 3), decoded and filtered by gfilt
# (tau == t exactly, F7-free, P3).  Usage: genbg_cells.sh "n m t D" ...   Output out/g_n_m_t_Dd.txt, summary in logs/genbg_cells.txt
cd /home/user/Erdos-757/experiments/referee/L012-round1
for spec in "$@"; do
  set -- $spec; n=$1; m=$2; t=$3; D=$4
  s=$(date +%s)
  nice -n 5 ./out/bin/genbg -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) | nice -n 5 ./out/bin/gfilt $n $m $t $D > out/g_${n}_${m}_${t}_D${D}.txt 2> out/g_${n}_${m}_${t}_D${D}.err
  e=$(date +%s)
  p=$(grep -c '^FOUND' /home/user/Erdos-757/experiments/prover/L012/out/cells/cell_${n}_${m}_${t}_D${D}.txt 2>/dev/null)
  echo "cell ($n,$m,$t,$D): genbg+gfilt classes $(grep -c '^FOUND' out/g_${n}_${m}_${t}_D${D}.txt) | prover $p | $(cat out/g_${n}_${m}_${t}_D${D}.err) | ${e}-${s}s" >> logs/genbg_cells.txt
done
