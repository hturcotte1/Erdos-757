#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L013-round2
for spec in "23 20 10 3 9" "26 21 11 3 10" "24 19 10 3 9" "25 17 10 3 9" "21 18 9 3 8"; do set -- $spec
  f=out/inp/in_$1_$2_$3_d$4.txt; s=out/inp/sample_$1_$2_$3_d$4.txt
  python3 -c "
import random,sys
L=open('$f').read().splitlines(); r=random.Random(2026); idx=sorted(r.sample(range(len(L)),min(8,len(L))))
# add inputs most likely to have hits: those with the most vertices of degree<=EP is hard to know; just random
open('$s','w').write('\n'.join(L[i] for i in idx)+'\n')"
  for mode in ext brute; do timeout 1500 nice -n 19 ./bin/refx $mode $(($1-1)) $5 $3 $4 $(($4-1)) < $s | grep SUMMARY | sed "s/^/($1,$2,$3) /"; done
done
