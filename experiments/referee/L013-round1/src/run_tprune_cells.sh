#!/bin/bash
# genbg with the tau-only PRUNE1 hook (sound: tau(final) <= tau(partial) + #edges still to add), then hfilt.
cd /home/user/Erdos-757/experiments/referee/L013-round1
KF=$1; OD=$2; TO=$3; mkdir -p $OD
while read n m t D; do
  f=$OD/cell_${n}_${m}_${t}_D${D}.txt
  if [ -s $f ] && grep -q SUMMARY $f; then continue; fi
  s=$(date +%s.%N)
  PRUNE_T=$t timeout $TO nice -n 10 ./bin/genbg_tprune -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) 2>/dev/null | nice -n 10 ./bin/hfilt $n $m $t $D print > $f.tmp
  rc=${PIPESTATUS[0]}
  e=$(date +%s.%N)
  if [ "$rc" = "0" ]; then mv $f.tmp $f; echo "($n,$m,$t,$D) TPRUNE $(tail -1 $f | sed 's/SUMMARY //') secs=$(echo "$e - $s" | bc)"; else echo "($n,$m,$t,$D) genbg_tprune rc=$rc (timeout?)"; rm -f $f.tmp; fi
done < $KF
