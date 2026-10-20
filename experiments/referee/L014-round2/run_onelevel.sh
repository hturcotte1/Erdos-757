#!/bin/bash
# Referee L014 round 2: one-level recomputation of cell(n,m,t,D) from the prover's component lists (files only read; components
# verified separately), every branch (d, t') by my own branch rule and decompositions, extension by bin/myext2 (connected members of
# C, kept iff tau == t), canonical forms by labelg (own nauty build), compared with the prover's list as sets of classes.
set -o pipefail
H=/home/user/Erdos-757/experiments/referee/L014-round2; cd $H
n=$1; m=$2; t=$3; D=$4; tag=${n}_${m}_${t}_D${D}
part=$(printf 'a%.0s' $(seq 1 $n))$(printf 'b%.0s' $(seq 1 $m))
rm -f out/ol_${tag}_keys_*.txt
python3 -c "
from math import ceil
n,m,t,D=$n,$m,$t,$D
for d in range(max(1,ceil(3*m/n)),D+1):
    for tp in (t-1,t):
        Sp=3*(n-1)+2*(m-d)-11*tp
        if Sp>=0 and tp>=0: print(d,tp)
" | while read d tp; do
  python3 gen_my_inputs.py out/tracked/cells $n $m $t $D $d $tp out/ol_${tag}_in_d${d}_tp${tp}.txt | tail -1
  nice -n 10 ./bin/myext2 $tp $t $d $((d-1)) 2 1 < out/ol_${tag}_in_d${d}_tp${tp}.txt | tee >(grep '^SUMMARY' > out/ol_${tag}_sum_d${d}_tp${tp}.txt) \
     | grep "^MEMBER tau=$t " | ./bin/hg2g6 2>/dev/null | ./out/nbin/labelg -q -f$part | LC_ALL=C sort -u -S 800M -T $H/out > out/ol_${tag}_keys_d${d}_tp${tp}.txt
  echo "branch d=$d tp=$tp pipeline_exit=$? $(cat out/ol_${tag}_sum_d${d}_tp${tp}.txt) classes_in_branch=$(wc -l < out/ol_${tag}_keys_d${d}_tp${tp}.txt)"
  rm -f out/ol_${tag}_in_d${d}_tp${tp}.txt
done
LC_ALL=C sort -u -m out/ol_${tag}_keys_*.txt > out/ol_${tag}_mine.txt
./classes.sh $n $m out/ol_${tag}_prov.txt out/tracked/cells/cell_${tag}.txt > /dev/null 2>&1
a=$(wc -l < out/ol_${tag}_mine.txt); b=$(wc -l < out/ol_${tag}_prov.txt)
if cmp -s out/ol_${tag}_mine.txt out/ol_${tag}_prov.txt; then s=IDENTICAL; else s=DIFFERENT; fi
echo "ONELEVEL ($n,$m,$t,$D) mine_classes=$a prover_classes=$b $s"
