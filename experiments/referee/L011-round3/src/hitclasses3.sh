#!/bin/bash
# compare class sets of my class-level hits with the prover's labelled hits (canonical forms on N points)
cd /home/user/Erdos-757/experiments/referee/L011-round3
for spec in "x20 20" "x21 21" "c6 21" "c8 22" "c4 21"; do set -- $spec; name=$1; N=$2
  [ -f out/ext_$name.txt ] || { echo "$name: no class-level output yet"; continue; }
  grep '^HIT' out/ext_$name.txt | sed 's/ |.*//' | ./bin/canon3 $N | cut -d' ' -f1 | sort -u > out/hc_mine_$name.cls
  echo "$name hit classes: mine $(wc -l < out/hc_mine_$name.cls) prover $(wc -l < out/hc_prov_$name.cls) $(cmp -s out/hc_mine_$name.cls out/hc_prov_$name.cls && echo IDENTICAL || echo DIFFERENT)"
done
