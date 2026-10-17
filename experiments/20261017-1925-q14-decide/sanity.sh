#!/bin/bash
# Step 4 sanity: recompute already-known cells in a fresh CELLDIR (all other cells symlinked, the target removed) and compare the class sets.
# usage: sanity.sh <plain|stream> n m t   (D=3)
cd "$(dirname "$0")"
mode=$1; n=$2; m=$3; t=$4; d=out/sanity_${mode}_${n}_${m}_${t}; rm -rf $d; mkdir -p $d
for f in out/cells/cell_*.txt; do b=$(basename $f); [ $b = cell_${n}_${m}_${t}_D3.txt ] || ln -s $(realpath $f) $d/$b; done
export PROGRESS=$PWD/out/sanity_progress.tsv CELLDIR=$PWD/$d ENGINELOG=$PWD/$d/engine.log NPROC=2 MD=10
if [ $mode = plain ]; then s0=$(date +%s); nice -n 5 timeout 3000 python3 engine.py $n $m $t 3 | tail -1; echo "plain engine wall $(( $(date +%s) - s0 )) s"
else s0=$(date +%s); nice -n 5 timeout 3000 python3 run_one.py $n $m $t 3 | tail -1; echo "stream wall $(( $(date +%s) - s0 )) s"; fi
python3 - <<PY
import re
def cls(p): return sorted(l.strip() for l in open(p) if l.startswith('FOUND:'))
a=cls('out/cells/cell_${n}_${m}_${t}_D3.txt'); b=cls('$d/cell_${n}_${m}_${t}_D3.txt')
print('SANITY $mode (${n},${m},${t},3): reference', len(a), 'recomputed', len(b), 'identical sets', a==b)
PY
