#!/bin/bash
# Referee L014 round 2: every direct (m <= 10) cell of the tree of (23,21,10,3) by unmodified genbg (own build) + own filter gfilt2,
# compared with the prover's list as sets of labelg classes.
cd /home/user/Erdos-757/experiments/referee/L014-round2
NB=out/nbin; mkdir -p out/gdir
while read n m t D; do
  gb=genbg; if [ $((n+m)) -gt 32 ] || [ $n -gt 24 ]; then gb=genbgL; fi
  f=out/gdir/g_${n}_${m}_${t}_D${D}.txt
  nice -n 12 $NB/$gb -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) | ./bin/gfilt2 $n $t 1 1 > $f 2> $f.log
  rc=$?
  ./classes.sh $n $m out/gdir/c_mine_${n}_${m}_${t}_D${D}.txt $f > /dev/null 2>&1
  ./classes.sh $n $m out/gdir/c_prov_${n}_${m}_${t}_D${D}.txt out/tracked/cells/cell_${n}_${m}_${t}_D${D}.txt > /dev/null 2>&1
  a=$(wc -l < $f); b=$(grep -c '^FOUND:' out/tracked/cells/cell_${n}_${m}_${t}_D${D}.txt)
  if cmp -s out/gdir/c_mine_${n}_${m}_${t}_D${D}.txt out/gdir/c_prov_${n}_${m}_${t}_D${D}.txt; then s=IDENTICAL; else s=DIFFERENT; fi
  echo "DIRECT ($n,$m,$t,$D) genbg=$gb rc=$rc mine=$a prover=$b classes_mine=$(wc -l < out/gdir/c_mine_${n}_${m}_${t}_D${D}.txt) $s | $(tail -1 $f.log | cut -c1-90)"
done < direct_cells_list.txt
