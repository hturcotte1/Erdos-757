#!/bin/bash
# genbg (2 parallel parts) + gfilt + class comparison for recursion cells of the run
cd /home/user/Erdos-757/experiments/referee/L014-round1
for c in "15 13 6 3" "17 11 6 3" "15 12 6 3" "16 11 6 3" "15 11 6 3" "19 12 7 3" "17 13 7 3" "18 12 7 3"; do
  set -- $c; n=$1; m=$2; t=$3; D=$4
  ./src/run_genbg_part.sh ./bin/genbg $n $m $t $D 0 2 5400 > /dev/null &
  ./src/run_genbg_part.sh ./bin/genbg $n $m $t $D 1 2 5400 > /dev/null &
  wait
  cat logs/gp_${n}_${m}_${t}_D${D}_0_2.time logs/gp_${n}_${m}_${t}_D${D}_1_2.time
  cat out/gp_${n}_${m}_${t}_D${D}_0_2.txt out/gp_${n}_${m}_${t}_D${D}_1_2.txt | grep '^FOUND' > out/g_${n}_${m}_${t}_D${D}.txt
  ./src/cmp_classes.sh $n out/g_${n}_${m}_${t}_D${D}.txt out/pcells/cells/cell_${n}_${m}_${t}_D${D}.txt
done > logs/rec_cells_genbg.txt 2>&1
echo ALLDONE >> logs/rec_cells_genbg.txt
