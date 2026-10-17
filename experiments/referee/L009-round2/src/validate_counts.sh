#!/bin/bash
# Referee L009 round 2, part 2 of the small-cell validation (cells too large to canonicalise every labelled brute-force graph):
# labelled count of bf2 (no symmetry breaking) must equal sum over genbg_r2 classes of n!/|Aut| (countg); class sets of genbg_r2 and of
# the prover's enum_conn must coincide (labelg canonical forms, colour classes kept apart).
R=/home/user/Erdos-757/experiments/referee/L009-round2; B=$R/out/bin; ND=$R/out/nauty; O=$R/out/val; mkdir -p $O
cd $R
for c in "$@"; do
  set -- $c; n=$1; m=$2; t=$3; d=$4; tag=${n}_${m}_${t}_${d}
  s=$(date +%s.%N)
  bfl=$(nice -n 5 $B/bf2 $n $m $t $d 0 | tail -n 1 | sed 's/.*labelled=//')
  TAU0=$t nice -n 5 $B/genbg_r2 -q -c -Z1 -d1:3 -D$d:3 $n $m $((3*m)):$((3*m)) > $O/gb_$tag.txt 2> $O/gb_$tag.err
  cut -f1 $O/gb_$tag.txt | src/canon.sh $n $m | sort -u > $O/gb_$tag.cls
  nice -n 5 $B/enum_conn_prover $n $m $t $d 1 > $O/ec_$tag.txt
  grep '^FOUND' $O/ec_$tag.txt | python3 src/hg2g6.py $n | src/canon.sh $n $m | sort -u > $O/ec_$tag.cls
  gl=$(cut -f1 $O/gb_$tag.txt | $ND/countg --a -q 2>/dev/null | python3 -c "
import sys,re,math
n=$n; tot=0
for l in sys.stdin:
    mm=re.match(r'\s*(\d+)\s+graphs?\s*:\s*groupsize=(\S+)', l)
    if mm: tot+=int(mm.group(1))*math.factorial(n)//int(float(mm.group(2)))
print(tot)")
  e=$(date +%s.%N)
  ng=$(wc -l < $O/gb_$tag.cls); ne=$(wc -l < $O/ec_$tag.cls)
  same2=$(cmp -s $O/ec_$tag.cls $O/gb_$tag.cls && echo yes || echo NO); same1=$([ "$bfl" = "$gl" ] && echo yes || echo NO)
  echo "cell ($n,$m,tau>=$t,D<=$d): classes genbg=$ng enum_conn=$ne | enum_conn==genbg $same2 | labelled bf2=$bfl genbg_sum_n!/aut=$gl equal=$same1 | $(grep R2SUMMARY $O/gb_$tag.err | sed 's/R2SUMMARY //;s/prune1_calls.*//') [$(python3 -c "print(round($e-$s,1))") s]"
done
