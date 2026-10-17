#!/bin/bash
# brute force (bf) vs my genbg vs the prover's enum_conn, class sets via canon, on all small cells (n<=8 all m; n=9 m<=5), D in {2,3}, every T0
cd /home/user/Erdos-757/experiments/referee/L010-round3
cmpd=0; tot=0
for n in 5 6 7 8 9; do for m in $(seq 2 $((n-2))); do
  if [ $n -gt $((2*m+1)) ]; then continue; fi; if [ $n -eq 9 ] && [ $m -gt 5 ]; then continue; fi
  for D in 2 3; do
    ./bin/bf $n $m 0 $D > out/bf_${n}_${m}_d${D}.txt
    for t in 0 1 2 3 4; do
      grep ^FOUND out/bf_${n}_${m}_d${D}.txt | ./bin/myfilter FOUND $n all | awk -v t=$t '{for(i=1;i<=NF;i++) if($i ~ /^tau=/){split($i,a,"="); if (a[2]+0>=t) print}}' | sed 's/.*| //' | ./bin/canon $n | sort -u > out/v_bf.txt
      TAU0=$t ./bin/genbg32 -q -c -Z1 -d1:3 -D$D:3 $n $m $((3*m)):$((3*m)) 2>/dev/null | ./bin/canon $n | sort -u > out/v_gb.txt
      out/rerun/enum_conn $n $m $t $D 1 | grep ^FOUND | ./bin/canon $n | sort -u > out/v_ec.txt
      tot=$((tot+1)); a=$(wc -l < out/v_bf.txt); b=$(wc -l < out/v_gb.txt); c=$(wc -l < out/v_ec.txt)
      if cmp -s out/v_bf.txt out/v_gb.txt && cmp -s out/v_bf.txt out/v_ec.txt; then :; else cmpd=$((cmpd+1)); echo "MISMATCH n=$n m=$m t=$t D=$D: bf=$a genbg=$b enum_conn=$c"; fi
      [ $t -eq 0 ] && echo "n=$n m=$m D=$D: labelled $(tail -1 out/bf_${n}_${m}_d${D}.txt | sed 's/.*labelled=//; s/ found.*//'), classes bf=$a genbg=$b enum_conn=$c"
    done
  done
done; done
echo "validate_small: comparisons=$tot mismatches=$cmpd"
