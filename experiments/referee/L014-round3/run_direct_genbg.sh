#!/bin/bash
# Referee: for every direct cell (n,m,t,D) given as n_m_t_D arguments, enumerate with unmodified genbg, filter with ref_g6filt,
# canonicalize with labelg, and compare with the prover's list (converted by ref_found2g6.py + labelg).
R=/home/user/Erdos-757/experiments/referee/L014-round3; G=$R/out/nauty/src/nauty2_8_8/genbg; L=$R/out/nauty/src/nauty2_8_8/labelg
for key in "$@"; do
  IFS=_ read n m t D <<< "$key"
  nice -n 10 timeout 3600 $G -q -c -Z1 -d1:3 -D$D:3 $n $m 2>/dev/null | nice -n 10 $R/out/ref_g6filt $n $m $t $D 2> $R/out/genbg/filt_$key.log | $L -q | LC_ALL=C sort -u > $R/out/genbg/mine_$key.g6
  st=${PIPESTATUS[0]}
  python3 $R/ref_found2g6.py $n $m < $R/out/cells/cells/cell_${n}_${m}_${t}_D${D}.txt 2>/dev/null | $L -q | LC_ALL=C sort -u > $R/out/genbg/prov_$key.g6
  a=$(wc -l < $R/out/genbg/mine_$key.g6); b=$(wc -l < $R/out/genbg/prov_$key.g6)
  if cmp -s $R/out/genbg/mine_$key.g6 $R/out/genbg/prov_$key.g6; then r=EQUAL; else r=DIFFERENT; fi
  echo "$key genbg_exit=$st mine=$a prover=$b $r $(grep -o 'total=[0-9]*' $R/out/genbg/filt_$key.log)"
done
