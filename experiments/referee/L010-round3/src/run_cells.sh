#!/bin/bash
# my genbg enumeration of all component cells (Delta<=3) and the window cells closed by direct enumeration; tau pruning only.
cd /home/user/Erdos-757/experiments/referee/L010-round3
g() { local n=$1 m=$2 t=$3 d=$4 bin=$5; local s=$(date +%s.%N); TAU0=$t ./bin/$bin -q -c -Z1 -d1:3 -D$d:3 $n $m $((3*m)):$((3*m)) > out/g_${n}_${m}_${t}_d${d}.txt 2> logs/g_${n}_${m}_${t}_d${d}.err; local e=$(date +%s.%N); echo "cell ($n,$m,>=$t) D<=$d: $(grep -c FOUND out/g_${n}_${m}_${t}_d${d}.txt) found; $(cat logs/g_${n}_${m}_${t}_d${d}.err | tr '\n' ' ') [$(echo "$e - $s" | bc) s]"; }
for c in "6 3 2" "8 5 3" "8 6 3" "9 4 3" "10 7 4" "11 6 4" "11 7 4" "13 8 5" "14 8 5" "16 9 6" "17 9 6" "19 10 7"; do set -- $c; g $1 $2 $3 3 genbg32; done
g 19 9 7 9 genbg32; g 18 12 7 2 genbg32; g 20 12 8 2 genbg32; g 20 13 8 2 genbg64
g 12 10 5 3 genbg32; g 15 11 6 3 genbg32
echo ALLDONE
