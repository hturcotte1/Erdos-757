#!/bin/bash
# Referee L009 round 2: component cells and empty window cells with genbg_r2 (tau prune only), class sets vs the prover's lists.
R=/home/user/Erdos-757/experiments/referee/L009-round2; P=/home/user/Erdos-757/experiments/prover/L009; O=$R/out/cells; cd $R
for c in "6 3 2 3" "8 5 3 3" "10 7 4 3" "10 8 4 3" "13 9 5 3" "16 10 6 3" "13 8 5 3" "13 8 5 8" "16 9 6 3" "16 9 6 9" "18 10 7 10" "18 11 7 3"; do
  set -- $c; n=$1; m=$2; t=$3; d=$4; tag=${n}_${m}_${t}_${d}; s=$(date +%s.%N)
  TAU0=$t nice -n 5 out/bin/genbg_r2 -q -c -Z1 -d1:3 -D$d:3 $n $m $((3*m)):$((3*m)) > $O/g_$tag.txt 2> $O/g_$tag.err
  e=$(date +%s.%N)
  cut -f1 $O/g_$tag.txt | src/canon.sh $n $m | sort -u > $O/g_$tag.cls
  grep "C=1" $O/g_$tag.txt | cut -f1 | src/canon.sh $n $m | sort -u > $O/gC_$tag.cls
  f=$P/indep/cell_${n}_${m}_${t}.txt; cmpres="(no prover list)"
  if [ "$d" = "3" ] && { [ -f $f ] || [ -f $f.gz ]; }; then
     if [ -f $f ]; then cat $f; else zcat $f.gz; fi | grep '^FOUND' | python3 src/hg2g6.py $n | src/canon.sh $n $m | sort -u > $O/p_$tag.cls
     cmp -s $O/p_$tag.cls $O/g_$tag.cls && cmpres="prover class set == genbg class set ($(wc -l < $O/p_$tag.cls))" || cmpres="DIFFERENT prover=$(wc -l < $O/p_$tag.cls)"
  fi
  echo "cell ($n,$m,tau>=$t,D<=$d): classes=$(wc -l < $O/g_$tag.cls) inC=$(wc -l < $O/gC_$tag.cls) | $cmpres | $(grep R2SUMMARY $O/g_$tag.err | sed 's/R2SUMMARY //;s/prune1_calls=[0-9]* //') [$(python3 -c "print(round($e-$s,1))") s]"
done
