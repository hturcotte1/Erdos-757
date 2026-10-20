#!/bin/bash
# usage: run_genbg.sh N M T D [timeout_s]  -> out/g_N_M_T_D<D>.txt (survivors + SUMMARY), logs/genbg_N_M_T_D<D>.time
cd /home/user/Erdos-757/experiments/referee/L014-round1
N=$1; M=$2; T=$3; D=$4; TO=${5:-3600}
s=$(date +%s)
set -o pipefail
nice -n 10 timeout $TO ./bin/genbg -q -c -Z1 -d1:3 -D$D:3 $N $M $((3*M)):$((3*M)) | ./bin/gfilt $N $M $T $D > out/g_${N}_${M}_${T}_D${D}.txt
rc=$?
e=$(date +%s)
echo "cell ($N,$M,$T,$D) rc=$rc secs=$((e-s)) $(tail -1 out/g_${N}_${M}_${T}_D${D}.txt)" | tee logs/genbg_${N}_${M}_${T}_D${D}.time
