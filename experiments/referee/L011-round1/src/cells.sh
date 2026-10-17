#!/bin/bash
# Referee L011: component / window cells with genbg + rhooks.  Usage: cells.sh "n m T0 D [CMODE]" ...
# Output out/g_<n>_<m>_<T0>_d<D>[_C].txt (lines "G: ... tau=t"), summary line appended to logs/cells.txt.
cd /home/user/Erdos-757/experiments/referee/L011-round1
for spec in "$@"; do
  set -- $spec; n=$1; m=$2; t=$3; D=$4; C=${5:-0}
  suf=""; [ "$C" = "1" ] && suf="_C"
  o=out/g_${n}_${m}_${t}_d${D}${suf}.txt
  s=$(date +%s.%N)
  TAU0=$t CMODE=$C nice -n 5 ./bin/rgenbg -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) > $o 2> $o.err
  e=$(date +%s.%N)
  echo "cell ($n,$m,>=$t) D<=$D CMODE=$C: $(grep RSUM $o.err) lines=$(grep -c '^G:' $o) wall=$(echo "$e - $s" | bc)" >> logs/cells.txt
done
