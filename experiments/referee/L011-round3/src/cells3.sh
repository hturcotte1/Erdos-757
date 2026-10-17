#!/bin/bash
# Referee round 3: enumerate component / window cells with genbg3 (TAU0 prune; optional F7 prune), then filter to class C.
# Usage: cells3.sh "n m T0 D [F7PRUNE]" ...   -> out/g_n_m_T0_dD[_F].txt, out/C_n_m_T0.txt (SURV lines), logs/cells3.txt
cd /home/user/Erdos-757/experiments/referee/L011-round3
for spec in "$@"; do
  set -- $spec; n=$1; m=$2; t=$3; D=$4; F=${5:-0}; suf=""; [ "$F" = "1" ] && suf="_F"
  o=out/g_${n}_${m}_${t}_d${D}${suf}.txt; s=$(date +%s.%N)
  TAU0=$t F7PRUNE=$F nice -n 5 ./bin/genbg3 -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) > $o 2> $o.err
  e=$(date +%s.%N)
  ./bin/filt3 $n notau quiet surv < $o > out/C_${n}_${m}_${t}_d${D}${suf}.txt
  echo "cell ($n,$m,>=$t) D<=$D F7PRUNE=$F: $(grep R3SUM $o.err) classes=$(grep -c '^G:' $o) $(grep FSUM out/C_${n}_${m}_${t}_d${D}${suf}.txt) wall=$(echo "$e - $s" | bc)" >> logs/cells3.txt
done
