#!/bin/bash
# genbg + gfilt + class comparison for every direct (m <= 10) key of the top tree (except those already done)
cd /home/user/Erdos-757/experiments/referee/L014-round1
grep ' direct' out/tree_keys.txt | awk '{print $1}' | tr ',' ' ' | while read n m t D; do
  if [ ! -f out/g_${n}_${m}_${t}_D${D}.txt ] || ! tail -1 out/g_${n}_${m}_${t}_D${D}.txt | grep -q SUMMARY; then ./src/run_genbg.sh $n $m $t $D 900 > /dev/null; fi
  echo "$(cat logs/genbg_${n}_${m}_${t}_D${D}.time 2>/dev/null | head -1)"
  ./src/cmp_classes.sh $n out/g_${n}_${m}_${t}_D${D}.txt out/pcells/cells/cell_${n}_${m}_${t}_D${D}.txt
done > logs/all_direct.txt 2>&1
echo ALLDONE >> logs/all_direct.txt
