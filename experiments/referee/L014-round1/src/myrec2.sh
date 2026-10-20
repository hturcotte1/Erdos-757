#!/bin/bash
# usage: myrec2.sh n m t D NPAR : own recomputation of the recursion list cell(n,m,t,D) from the prover's lower lists, streamed:
#   own decompositions + own input builder -> myext2 (own extension + filter) -> hg2g6 -> labelg -> sort -u ; class-set comparison.
cd /home/user/Erdos-757/experiments/referee/L014-round1
n=$1; m=$2; t=$3; D=$4; NPAR=${5:-1}; P=out/rec/c_${n}_${m}_${t}_D${D}; mkdir -p out/rec out/tmp
set -o pipefail
s=$(date +%s)
nice -n 10 python3 src/build_inputs.py out/pcells/cells $n $m $t $D $P > $P.build.txt || { echo "build failed"; exit 1; }
cat $P.build.txt
rm -f $P.keys.part* $P.sum.part* $P.cnt.part*
for f in ${P}_d*_tp*.txt; do
  d=$(echo $f | sed 's/.*_d\([0-9]*\)_tp\([0-9]*\).txt/\1/'); tp=$(echo $f | sed 's/.*_d\([0-9]*\)_tp\([0-9]*\).txt/\2/')
  [ -s $f ] || continue
  split -n r/$NPAR -d $f ${f%.txt}.in
  pids=""
  for q in ${f%.txt}.in*; do
    b=$(basename $q)
    ( nice -n 10 ./bin/myext2 $((n-1)) $t $d $((d-1)) < $q | awk -v S=$P.sum.part.$b -v C=$P.cnt.part.$b '/^FOUND/{print; k++; next} {print > S} END{print k+0 > C}' \
      | ./bin/hg2g6 $n 2>/dev/null | ./bin/labelg -q 2>/dev/null | LC_ALL=C sort -u -S 500M -T out/tmp > $P.keys.part.$b ) &
    pids="$pids $!"
  done
  for p in $pids; do wait $p || { echo "pipeline failed"; exit 1; }; done
  for q in ${f%.txt}.in*; do b=$(basename $q); sed "s/^/  d=$d tp=$tp $b /" $P.sum.part.$b; rm -f $q; done
done
LC_ALL=C sort -u -m $P.keys.part.* > $P.mykeys
grep '^FOUND' out/pcells/cells/cell_${n}_${m}_${t}_D${D}.txt | ./bin/hg2g6 $n 2>/dev/null | ./bin/labelg -q | LC_ALL=C sort > $P.theirkeys
nl=$(cat $P.cnt.part.* | awk '{s+=$1} END{print s+0}')
na=$(wc -l < $P.mykeys); nb=$(wc -l < $P.theirkeys); ub=$(uniq $P.theirkeys | wc -l)
oa=$(LC_ALL=C comm -23 $P.mykeys <(uniq $P.theirkeys) | wc -l); ob=$(LC_ALL=C comm -13 $P.mykeys <(uniq $P.theirkeys) | wc -l)
echo "RESULT cell($n,$m,$t,$D) my_connected_survivor_lines=$nl my_classes=$na prover_lines=$nb prover_classes=$ub only_mine=$oa only_prover=$ob $( [ $oa -eq 0 ] && [ $ob -eq 0 ] && echo CLASS-SETS-EQUAL || echo DIFFERENT) secs=$(( $(date +%s) - s ))"
rm -f $P.keys.part.* $P.cnt.part.* $P.sum.part.*
