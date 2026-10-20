#!/bin/bash
# Referee L014 round 2: one-level recomputation of cell(18,14,7,3) streamed: myext2 (connected members, tau >= 7) -> hg2g6 ->
# labelg (own nauty build, 2-colour partition) -> sort -u; the myext2 SUMMARY line is kept.
set -o pipefail
H=/home/user/Erdos-757/experiments/referee/L014-round2; cd $H
part=$(printf 'a%.0s' $(seq 1 18))$(printf 'b%.0s' $(seq 1 14))
nice -n 10 ./bin/myext2 6 7 3 2 2 1 < out/in_18_14_7.txt | tee >(grep '^SUMMARY' > out/ext18_summary.txt) | grep '^MEMBER' \
  | ./bin/hg2g6 | ./out/nbin/labelg -q -f$part | LC_ALL=C sort -u -S 1200M -T $H/out > out/c_mine_18_14_7.txt
echo "pipeline exit $?"
./classes.sh 18 14 out/c_prov_18_14_7.txt out/tracked/cells/cell_18_14_7_D3.txt
echo "mine $(wc -l < out/c_mine_18_14_7.txt) prover $(wc -l < out/c_prov_18_14_7.txt)"
cmp out/c_mine_18_14_7.txt out/c_prov_18_14_7.txt && echo "(18,14,7,3) IDENTICAL"
cat out/ext18_summary.txt
