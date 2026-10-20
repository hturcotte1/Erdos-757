#!/bin/bash
# usage: myrec.sh n m t D [NPAR]: own recomputation of the recursion list cell(n,m,t,D) from the prover's lower lists
#   (own decompositions + own input builder + myext2 + labelg) and class comparison with the prover's list.
cd /home/user/Erdos-757/experiments/referee/L014-round1
n=$1; m=$2; t=$3; D=$4; NPAR=${5:-1}; P=out/rec/c_${n}_${m}_${t}_D${D}; mkdir -p out/rec
set -o pipefail
s=$(date +%s)
nice -n 10 python3 src/build_inputs.py out/pcells/cells $n $m $t $D $P > $P.build.txt || { echo "build failed"; exit 1; }
cat $P.build.txt
: > $P.found.txt
for f in ${P}_d*_tp*.txt; do
  d=$(echo $f | sed 's/.*_d\([0-9]*\)_tp\([0-9]*\).txt/\1/'); tp=$(echo $f | sed 's/.*_d\([0-9]*\)_tp\([0-9]*\).txt/\2/')
  [ -s $f ] || continue
  if [ $NPAR -gt 1 ]; then
    split -n r/$NPAR -d $f ${f%.txt}.part
    for q in ${f%.txt}.part*; do nice -n 10 ./bin/myext2 $((n-1)) $t $d $((d-1)) < $q > $q.out & done; wait
    for q in ${f%.txt}.part??; do grep '^SUMMARY' $q.out | sed "s/^/  d=$d tp=$tp part $(basename $q) /"; grep '^FOUND' $q.out >> $P.found.txt; rm -f $q $q.out; done
  else
    nice -n 10 ./bin/myext2 $((n-1)) $t $d $((d-1)) < $f > $f.out || { echo "myext2 failed"; exit 1; }
    grep '^SUMMARY' $f.out | sed "s/^/  d=$d tp=$tp /"; grep '^FOUND' $f.out >> $P.found.txt; rm -f $f.out
  fi
done
echo "survivor lines $(wc -l < $P.found.txt), secs $(( $(date +%s) - s ))"
./src/cmp_classes.sh $n $P.found.txt out/pcells/cells/cell_${n}_${m}_${t}_D${D}.txt
