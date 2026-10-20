#!/bin/bash
# Referee: recompute a recursion cell (n,m,t,D) with d=3 branches from the prover's lower lists: own inputs (ref_gen_inputs.py),
# own extension search (refext2, graph6 output of connected members of C with tau >= t), labelg canonical forms, compare with the prover's list.
R=/home/user/Erdos-757/experiments/referee/L014-round3; L=$R/out/nauty/src/nauty2_8_8/labelg
n=$1; m=$2; t=$3; D=$4; key=${n}_${m}_${t}_${D}; W=$R/out/rc_$key; mkdir -p $W
nice -n 10 timeout 3600 python3 $R/ref_gen_inputs.py $R/out/cells/cells $n $m $t $D $W/inputs.txt > $W/gen.log 2>&1 || { echo "$key gen failed"; exit 1; }
# only one branch (d=3, t'=t-1) is expected for these cells; refext2 needs the branch parameters
tp=$((t-1))
nice -n 10 timeout 7000 $R/out/refext2 $((n-1)) $tp $t 3 2 0 G6 < $W/inputs.txt > $W/g6.txt 2> $W/err.txt; echo "refext2 exit $?" >> $W/err.txt
grep -v "^SUMMARY" $W/g6.txt | $L -q | LC_ALL=C sort -u > $W/mine.g6
python3 $R/ref_found2g6.py $n $m < $R/out/cells/cells/cell_${n}_${m}_${t}_D${D}.txt 2>/dev/null | $L -q | LC_ALL=C sort -u > $W/prover.g6
a=$(wc -l < $W/mine.g6); b=$(wc -l < $W/prover.g6)
if cmp -s $W/mine.g6 $W/prover.g6; then r=EQUAL; else r=DIFFERENT; fi
echo "$key inputs=$(wc -l < $W/inputs.txt) $(tail -1 $W/err.txt | head -c 300) | mine=$a prover=$b $r"
