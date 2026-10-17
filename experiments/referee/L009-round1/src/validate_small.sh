#!/bin/bash
# Referee L009: validate genbg+refprune (and the prover's enum_conn) against brute force on small cells.
# For each cell (n m T D): brute-force labelled count (all / in C) vs genbg sum of n!/|Aut| over classes (all / in C);
# and the class set of the prover's enum_conn output vs the genbg class set.
cd /home/user/Erdos-757/experiments/referee/L009-round1
run() {
  n=$1; m=$2; T=$3; D=$4
  bf=$(nice -n 5 ./bin/bf $n $m $T $D)
  TAU0=$T nice -n 5 ./bin/genbg_ref -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) 2>/dev/null > out/v_g.txt
  ga=$(./bin/canon $n < out/v_g.txt | python3 src/lcount.py)
  gc=$(grep 'C=1' out/v_g.txt | ./bin/canon $n | python3 src/lcount.py)
  nice -n 5 ./bin/enum_conn_prover $n $m $T $D 1 > out/v_e.txt
  ./bin/canon $n < out/v_e.txt | awk '{print $1}' | sort -u > out/v_e_cls.txt
  ./bin/canon $n < out/v_g.txt | awk '{print $1}' | sort -u > out/v_g_cls.txt
  if cmp -s out/v_e_cls.txt out/v_g_cls.txt; then ec=SAME; else ec=DIFFERENT; fi
  echo "cell ($n,$m,>=$T,D<=$D): $bf | genbg all: $ga | genbg in C: $gc | enum_conn classes $(wc -l < out/v_e_cls.txt) vs genbg $(wc -l < out/v_g_cls.txt): $ec"
}
for c in "6 3 2 3" "7 5 3 3" "7 5 3 5" "8 5 3 3" "8 5 3 5" "8 6 3 3" "8 6 3 6" "8 4 3 4" "9 4 3 3" "9 4 3 4" "9 5 3 3" "9 6 3 3" "9 6 4 6" "9 7 3 3" "9 7 4 7" "9 6 3 6" "10 5 4 5" "10 6 4 6"; do run $c; done
