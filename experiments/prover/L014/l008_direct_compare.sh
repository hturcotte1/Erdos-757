#!/bin/bash
# (L014) C8: the direct enumeration `enum_conn 15 11 6 3` of certificate L008 (experiments/prover/L008/indep/mine_15_11_6_deg3.txt.gz,
# 50,606 labelled graphs, read only) reduced with this run's filt/canon to classes in C with tau = 6, compared with the recursion list
# cell(15,11,6,3) of this run; and the same for L008's `enum_conn 12 10 5 3` against cell(12,10,5,3) (direct in this run too).
cd /home/user/Erdos-757/experiments/prover/L014
for spec in "15 11 6 mine_15_11_6_deg3" "12 10 5 mine_12_10_5_deg3"; do
  set -- $spec
  zcat ../L008/indep/$4.txt.gz | ./bin/filt FOUND $1 tau $3 > out/l008_$4_filt.txt
  echo "L008 $4: $(tail -n1 out/l008_$4_filt.txt)"
  grep '^SURVIVOR' out/l008_$4_filt.txt | cut -d'#' -f1 | ./bin/canon $1 2>/dev/null | LC_ALL=C sort -u > out/l008_$4_keys.txt
  grep '^FOUND:' out/cells/cell_$1_$2_$3_D3.txt | ./bin/canon $1 2>/dev/null | LC_ALL=C sort -u > out/l008_$4_mine.txt
  echo "  classes: L008 direct $(wc -l < out/l008_$4_keys.txt), this run $(wc -l < out/l008_$4_mine.txt), $(cmp -s out/l008_$4_keys.txt out/l008_$4_mine.txt && echo IDENTICAL || echo DIFFERENT)"
done
