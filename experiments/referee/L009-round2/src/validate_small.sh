#!/bin/bash
# Referee L009 round 2: validate genbg+r2hooks (and the prover's enum_conn) against the brute force bf2 on small cells.
# For each cell: class sets (labelg canonical forms, colour classes kept apart) of bf2, genbg_r2 and enum_conn must coincide,
# and the labelled count of bf2 must equal sum over genbg classes of n!/|Aut|.
R=/home/user/Erdos-757/experiments/referee/L009-round2; B=$R/out/bin; ND=$R/out/nauty; O=$R/out/val; mkdir -p $O
cd $R
for c in "6 3 2 3" "7 5 3 3" "7 5 3 5" "7 5 2 3" "8 5 3 3" "8 5 3 5" "8 6 3 3" "8 6 3 6" "8 4 3 4" "8 4 2 2" "9 4 3 3" "9 5 3 3" "9 6 3 3" "9 6 4 6" "9 7 3 3" "9 7 4 7" "9 6 3 6" "9 5 3 5" "10 5 4 5" "10 6 4 6" "10 6 4 3" "10 7 4 3"; do
  set -- $c; n=$1; m=$2; t=$3; d=$4; tag=${n}_${m}_${t}_${d}
  s=$(date +%s.%N)
  timeout 900 nice -n 5 $B/bf2 $n $m $t $d 1 > $O/bf_$tag.txt
  bfl=$(tail -n 1 $O/bf_$tag.txt | sed 's/.*labelled=//')
  grep '^E:' $O/bf_$tag.txt | python3 src/hg2g6.py $n | src/canon.sh $n $m | sort -u > $O/bf_$tag.cls
  TAU0=$t nice -n 5 $B/genbg_r2 -q -c -Z1 -d1:3 -D$d:3 $n $m $((3*m)):$((3*m)) > $O/gb_$tag.txt 2> $O/gb_$tag.err
  cut -f1 $O/gb_$tag.txt | src/canon.sh $n $m | sort -u > $O/gb_$tag.cls
  nice -n 5 $B/enum_conn_prover $n $m $t $d 1 > $O/ec_$tag.txt
  grep '^FOUND' $O/ec_$tag.txt | python3 src/hg2g6.py $n | src/canon.sh $n $m | sort -u > $O/ec_$tag.cls
  # labelled count from genbg classes: sum n!/|Aut|
  gl=$(cut -f1 $O/gb_$tag.txt | $ND/countg --a -q 2>/dev/null | python3 -c "
import sys,re,math
n=$n; tot=0
for l in sys.stdin:
    mm=re.match(r'\s*(\d+)\s+graphs?\s*:\s*groupsize=(\S+)', l) or re.match(r'\s*(\d+)\s+graphs?\s*:\s*a=(\S+)', l)
    if mm: tot+=int(mm.group(1))*math.factorial(n)//int(float(mm.group(2)))
print(tot)")
  e=$(date +%s.%N)
  ng=$(wc -l < $O/gb_$tag.cls); nb=$(wc -l < $O/bf_$tag.cls); ne=$(wc -l < $O/ec_$tag.cls)
  same1=$(cmp -s $O/bf_$tag.cls $O/gb_$tag.cls && echo yes || echo NO); same2=$(cmp -s $O/ec_$tag.cls $O/gb_$tag.cls && echo yes || echo NO)
  echo "cell ($n,$m,tau>=$t,D<=$d): classes bf2=$nb genbg=$ng enum_conn=$ne | bf2==genbg $same1 | enum_conn==genbg $same2 | labelled bf2=$bfl genbg_sum_n!/aut=$gl | $(grep R2SUMMARY $O/gb_$tag.err | sed 's/R2SUMMARY //;s/prune1_calls.*//') [$(python3 -c "print(round($e-$s,1))") s]"
done
