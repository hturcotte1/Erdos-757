#!/bin/bash
# Referee L011: class sets of the prover's enum_conn (copy) vs referee genbg+rhooks for all small cells n<=10, D in {2,3}, every m, T0 in {0, max}.
cd /home/user/Erdos-757/experiments/referee/L011-round1
E=out/rerun/bin/enum_conn; tot=0; bad=0
for n in 3 4 5 6 7 8 9 10; do for D in 2 3; do for m in $(seq 1 $(( n*D/3 ))); do
  [ $n -gt $((2*m+1)) ] && continue
  for t in 0 1 2 3 4 5; do
    [ $t -gt $m ] && continue
    $E $n $m $t $D 1 > out/tec_e.txt
    TAU0=$t ./bin/rgenbg -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) > out/tec_g.txt 2>/dev/null
    a=$(grep '^FOUND' out/tec_e.txt | ./bin/rcanon $n FOUND | cut -d' ' -f1 | LC_ALL=C sort -u | sha256sum)
    b=$(grep '^G' out/tec_g.txt | ./bin/rcanon $n G | cut -d' ' -f1 | LC_ALL=C sort -u | sha256sum)
    tot=$((tot+1)); if [ "$a" != "$b" ]; then bad=$((bad+1)); echo "DIFF n=$n D=$D m=$m t=$t"; fi
  done; done; done; done
echo "enum_conn vs genbg class sets: $tot comparisons, $bad differences"
