#!/bin/bash
# Referee L014 round 2: one-level recomputation of cell(21,15,8,3) (single branch d=3, t'=7, S'=7; 121,532 inputs from the tracked
# lists), in 3 parallel parts: myext3 (FAST: Hall-form (P3), tau implied) -> connected members -> hg2g6 -> labelg -> sort -u.
set -o pipefail
H=/home/user/Erdos-757/experiments/referee/L014-round2; cd $H
part=$(printf 'a%.0s' $(seq 1 21))$(printf 'b%.0s' $(seq 1 15))
split -n l/3 -d out/ol_21_15_8_D3_in_d3_tp7.txt out/in2115_p
for p in 00 01 02; do
  ( nice -n 10 ./bin/myext3 7 8 3 2 2 1 < out/in2115_p$p | tee >(grep '^SUMMARY' > out/ext2115_sum_$p.txt) | grep '^MEMBER tau=8 ' \
      | ./bin/hg2g6 2>/dev/null | ./out/nbin/labelg -q -f$part | LC_ALL=C sort -u -S 600M -T $H/out > out/c2115_$p.txt; echo "part $p exit $?" ) &
done
wait
LC_ALL=C sort -u -m out/c2115_0*.txt > out/c_mine_21_15_8.txt
./classes.sh 21 15 out/c_prov_21_15_8.txt out/tracked/cells/cell_21_15_8_D3.txt
cat out/ext2115_sum_*.txt
echo "mine $(wc -l < out/c_mine_21_15_8.txt) prover $(wc -l < out/c_prov_21_15_8.txt)"
cmp out/c_mine_21_15_8.txt out/c_prov_21_15_8.txt && echo "(21,15,8,3) IDENTICAL"
