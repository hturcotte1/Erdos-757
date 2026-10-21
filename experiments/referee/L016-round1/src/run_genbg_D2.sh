#!/bin/bash
# Referee L016 round 1: every max-degree-2 list of the prover's run A by unmodified genbg + own filter g6filt; class sets
# compared with the prover's lists through labelg (incidence graphs, vertex cell first).
R=/home/user/Erdos-757/experiments/referee/L016-round1; cd $R; mkdir -p out/gD2
while read n m t; do
  F=$(python3 -c "print('a'*$n)")
  nice -n 10 timeout 1500 ./bin/genbg30 -q -c -Z1 -d1:3 -D2:3 $n $m $((3*m)):$((3*m)) 2>/dev/null | ./bin/g6filt $n $m $t 2 > out/gD2/g_${n}_${m}_${t}.txt
  rc=${PIPESTATUS[0]}
  grep '^FOUND' out/gD2/g_${n}_${m}_${t}.txt | python3 src/canon_lines.py $n | ./bin/labelg -q -f$F 2>/dev/null | LC_ALL=C sort -u > out/gD2/mine_${n}_${m}_${t}.g6
  grep '^FOUND' out/new/cells_new/runA/cell_${n}_${m}_${t}_D2.txt | python3 src/canon_lines.py $n | ./bin/labelg -q -f$F 2>/dev/null | LC_ALL=C sort -u > out/gD2/prov_${n}_${m}_${t}.g6
  eq=$(cmp -s out/gD2/mine_${n}_${m}_${t}.g6 out/gD2/prov_${n}_${m}_${t}.g6 && echo EQUAL || echo DIFFERENT)
  echo "D2 ($n,$m,$t) genbg_rc=$rc mine=$(wc -l < out/gD2/mine_${n}_${m}_${t}.g6) prover=$(wc -l < out/gD2/prov_${n}_${m}_${t}.g6) $eq | $(grep G6FILT out/gD2/g_${n}_${m}_${t}.txt | cut -d' ' -f6-) | $(grep 'TAUHIST(in C)' out/gD2/g_${n}_${m}_${t}.txt)"
done < ${1:-out/runA_D2_keys.txt}
