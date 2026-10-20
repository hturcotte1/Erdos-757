#!/bin/bash
# Referee round 3: class sets of (a) labelled brute force bf3, (b) genbg3 with TAU0 prune, (c) the prover's enum_conn (copy),
# all canonicalized with canon3, must coincide.  Usage: validate3.sh "N M T0 D" ...
cd /home/user/Erdos-757/experiments/referee/L011-round3
for spec in "$@"; do set -- $spec; N=$1; M=$2; T=$3; D=$4
  nice -n 5 ./bin/bf3 $N $M $T $D 1 > out/v_bf.txt; nb=$(grep -c '^L:' out/v_bf.txt)
  grep '^L:' out/v_bf.txt | ./bin/canon3 $N | cut -d' ' -f1 | sort -u > out/v_bf.cls
  TAU0=$T nice -n 5 ./bin/genbg3 -q -c -Z1 -d1:3 -D$D:3 $N $M $((3*M)):$((3*M)) 2>/dev/null | ./bin/canon3 $N | cut -d' ' -f1 | sort -u > out/v_gb.cls
  nice -n 5 ./out/prover_copy/enum_conn $N $M $T $D 1 | grep '^FOUND' | ./bin/canon3 $N | cut -d' ' -f1 | sort -u > out/v_ec.cls
  r1=$(cmp -s out/v_bf.cls out/v_gb.cls && echo EQ || echo DIFF); r2=$(cmp -s out/v_bf.cls out/v_ec.cls && echo EQ || echo DIFF)
  echo "($N,$M,>=$T) D<=$D: labelled=$nb classes bf=$(wc -l < out/v_bf.cls) genbg=$(wc -l < out/v_gb.cls) enum_conn=$(wc -l < out/v_ec.cls) bf-vs-genbg=$r1 bf-vs-enum_conn=$r2"
done
