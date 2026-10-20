#!/bin/bash
# usage: run_genbg_part.sh GENBG N M T D RES MOD [timeout_s] -> out/gp_N_M_T_D<D>_RES_MOD.txt
cd /home/user/Erdos-757/experiments/referee/L014-round1
G=$1; N=$2; M=$3; T=$4; D=$5; R=$6; MO=$7; TO=${8:-7200}
s=$(date +%s)
set -o pipefail
nice -n 10 timeout $TO $G -q -c -Z1 -d1:3 -D$D:3 $N $M $((3*M)):$((3*M)) $R/$MO | ./bin/gfilt $N $M $T $D > out/gp_${N}_${M}_${T}_D${D}_${R}_${MO}.txt
rc=$?
e=$(date +%s)
echo "cell ($N,$M,$T,$D) part $R/$MO rc=$rc secs=$((e-s)) $(tail -1 out/gp_${N}_${M}_${T}_D${D}_${R}_${MO}.txt)" | tee logs/gp_${N}_${M}_${T}_D${D}_${R}_${MO}.time
