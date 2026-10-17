#!/bin/bash
# Compare class sets (canon3) of my genbg3 lists with the prover's labelled lists.  Usage: cmp3.sh "n m t PROVER_ALL PROVER_INC" ...
# PROVER_ALL: file with FOUND lines (all Delta<=3), or '-' ; PROVER_INC: file with SURVIVOR lines (in C), or '-'.  gz files allowed.
cd /home/user/Erdos-757/experiments/referee/L011-round3
rd() { case "$1" in *.gz) zcat "$1";; *) cat "$1";; esac; }
for spec in "$@"; do set -- $spec; n=$1; m=$2; t=$3; PA=$4; PC=$5
  grep '^G:' out/g_${n}_${m}_${t}_d3.txt | ./bin/canon3 $n | cut -d' ' -f1 | sort -u > out/c_mine_all.cls
  grep '^SURV:' out/C_${n}_${m}_${t}_d3.txt | ./bin/canon3 $n | cut -d' ' -f1 | sort -u > out/c_mine_C.cls
  ra="-"; rc="-"
  if [ "$PA" != "-" ]; then rd $PA | grep '^FOUND' | ./bin/canon3 $n | cut -d' ' -f1 | sort -u > out/c_prov_all.cls; ra="$(wc -l < out/c_prov_all.cls) $(cmp -s out/c_mine_all.cls out/c_prov_all.cls && echo EQ || echo DIFF)"; fi
  if [ "$PC" != "-" ]; then rd $PC | grep '^SURVIVOR' | ./bin/canon3 $n | cut -d' ' -f1 | sort -u > out/c_prov_C.cls; rc="$(wc -l < out/c_prov_C.cls) $(cmp -s out/c_mine_C.cls out/c_prov_C.cls && echo EQ || echo DIFF)"; fi
  echo "($n,$m,$t): mine all=$(wc -l < out/c_mine_all.cls) inC=$(wc -l < out/c_mine_C.cls) | prover all-classes: $ra | prover inC-classes: $rc"
done
