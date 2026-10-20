#!/bin/bash
# Referee L014 round 2: soundness of the lists that enter the final step (every representative a connected member of C with the
# key's (n, m, tau) and max degree <= 3), by bin/myext verify mode (d = 0; P3 by the Hall test).
cd /home/user/Erdos-757/experiments/referee/L014-round2
for k in 22_18_9 19_17_8 12_10_5 10_8_4 8_6_3 14_12_6 3_1_1 21_18_9; do
  IFS=_ read n m t <<< "$k"
  f=out/tracked/cells/cell_${n}_${m}_${t}_D3.txt
  python3 -c "
import re,sys
for l in open('$f'):
    if l.startswith('FOUND:'):
        es=re.findall(r'\((\d+),(\d+),(\d+)\)', l); print($n, len(es), ' '.join(' '.join(e) for e in es))
" | nice -n 10 ./bin/myext_v $t 0 0 3 1 1 | tail -1 | sed "s/^/cell($n,$m,$t,3): /"
done
