#!/bin/bash
# Referee L012: direct enumeration of cells with genbg + the referee's own pruning hooks (mgenbg); compare with the prover's lists.
# Usage: mgenbg_cells.sh TIMEOUT "n m t D" ...   output out/mg_n_m_t_Dd.txt, summary logs/mgenbg_cells.txt
cd /home/user/Erdos-757/experiments/referee/L012-round1
TO=$1; shift
for spec in "$@"; do
  set -- $spec; n=$1; m=$2; t=$3; D=$4; o=out/mg_${n}_${m}_${t}_D${D}.txt
  s=$(date +%s)
  TT=$t timeout $TO nice -n 5 ./out/bin/mgenbg -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) > $o 2> $o.err; rc=$?
  e=$(date +%s)
  p=$(grep -c '^FOUND' /home/user/Erdos-757/experiments/prover/L012/out/cells/cell_${n}_${m}_${t}_D${D}.txt 2>/dev/null)
  echo "cell ($n,$m,$t,$D): rc=$rc mgenbg classes $(grep -c '^FOUND' $o) | prover $p | $(tail -1 $o.err) | $((e-s))s" >> logs/mgenbg_cells.txt
done
echo ALLDONE >> logs/mgenbg_cells.txt
