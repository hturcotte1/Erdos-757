#!/bin/bash
# Referee L016 round 1: own extension program on sampled chunks of cell(25,19,10,3); compare with the worker's chunk counters
# and keys (as labelg classes) and test containment in the prover's list.
R=/home/user/Erdos-757/experiments/referee/L016-round1; cd $R
F25=$(python3 -c "print('a'*25)")
W=out/wchunks/chunks/25_19_10_D3_d3_tp9
for c in "$@"; do
  cc=$(printf %05d $c)
  nice -n 10 timeout 1800 ./bin/myext 24 9 3 2 3 < out/chunks/chunk_$cc.txt > out/chunks/my_$cc.out
  grep '^X:' out/chunks/my_$cc.out | python3 src/canon_lines.py 25 | ./bin/labelg -q -f$F25 | LC_ALL=C sort -u > out/chunks/my_$cc.g6
  zcat $W/c$cc.keys.gz | python3 src/canon_lines.py 25 | ./bin/labelg -q -f$F25 | LC_ALL=C sort -u > out/chunks/w_$cc.g6
  eq=$(cmp -s out/chunks/my_$cc.g6 out/chunks/w_$cc.g6 && echo EQUAL || echo DIFFERENT)
  miss=$(LC_ALL=C comm -23 out/chunks/my_$cc.g6 out/prov_25_19_10.g6 | wc -l)
  echo "CHUNK $c $(tail -1 out/chunks/my_$cc.out) | classes mine=$(wc -l < out/chunks/my_$cc.g6) worker=$(wc -l < out/chunks/w_$cc.g6) $eq | not in prover list: $miss | worker meta: $(python3 -c "import json;j=json.load(open('$W/c$cc.meta.json'));e=j['ext'];print('graphs=%d max_min_covers=%d hits_F7free=%d hits_in_C=%d nsurv=%d'%(e['graphs'],e['max_min_covers'],e['hits_F7free'],e['hits_in_C'],j['nsurv']))")"
  rm -f out/chunks/my_$cc.out
done
