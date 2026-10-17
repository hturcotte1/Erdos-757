#!/bin/bash
# Referee L011: class sets (nauty canonical forms) of the prover's labelled hit files and of the referee's class-level hits.
cd /home/user/Erdos-757/experiments/referee/L011-round1
P=/home/user/Erdos-757/experiments/prover/L011/out
cls() { # name N source(cat-able command)
  local name=$1 N=$2; shift 2
  "$@" | grep '^HIT' | nice -n 5 ./bin/rcanon $N HIT | cut -d' ' -f1 | LC_ALL=C sort -u > out/cls_$name.txt
  echo "$name: $(wc -l < out/cls_$name.txt) classes"
}
cls prover_c4 21 cat $P/hits21_12.txt
cls ref_c4 21 cat out/ext_c4_C.txt
cls prover_x20 20 zcat $P/hitsX20.txt.gz
cls ref_x20 20 cat out/ext_x20_C.txt
cls prover_x21 21 zcat $P/hitsX21.txt.gz
cls ref_x21 21 cat out/ext_x21_C.txt
cls prover_c8 22 zcat $P/hits22_16.txt.gz
cls ref_c8 22 cat out/ext_c8_C.txt
for s in c4 x20 x21 c8; do
  if cmp -s out/cls_prover_$s.txt out/cls_ref_$s.txt; then echo "$s: class sets IDENTICAL"; else echo "$s: class sets DIFFER: $(comm -23 out/cls_prover_$s.txt out/cls_ref_$s.txt | wc -l) prover-only, $(comm -13 out/cls_prover_$s.txt out/cls_ref_$s.txt | wc -l) referee-only"; fi
done
