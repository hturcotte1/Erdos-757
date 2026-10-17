#!/bin/bash
# Exact commands for experiments/20261017-1735-q14-cell-sizes (run from this directory). NPROC=1, nice 19, MD=10. Not set -e: a timeout must not stop the sequence.
cd "$(dirname "$0")"; mkdir -p out/cells
S=../20261017-1720-i11-n26
for f in engine.py decomp22.py run_cells.py; do cp $S/$f .; done
[ -e bin ] || ln -s ../prover/L012/bin bin
[ -e out/seeded ] || { cp $S/out/cells/cell_* out/cells/; ls out/cells > out/seeded; }   # 167 cell files (1645 + cells25 + n26 run)
python3 decomps.py > decompositions.txt
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log NPROC=1 MD=10
left() { echo $(( (DEADLINE - $(date +%s)) / 60 )); }
START=$(date +%s); DEADLINE=$(( START + 3*3600 - 600 ))
runc() { # timeout_min n m tau D   (min(timeout, remaining))
  [ $1 -gt $(left) ] && set -- $(left) "${@:2}"
  nice -n 19 timeout $(( $1 * 60 )) python3 run_one.py $2 $3 $4 $5 > out/run_$2_$3_$4.log 2>&1
  rc=$?; [ $rc -eq 0 ] || pkill -f "$PWD/bin/"
  [ $rc -eq 0 ] || printf '(%s,%s,%s,%s)\tKILLED_rc%s\t>%s\t-\t-\t-\t-\n' $2 $3 $4 $5 $rc $(( $1 * 60 )) >> progress.tsv
  return $rc
}

ok=1
for c in "15 13 6" "18 14 7" "21 15 8"; do runc 50 $c 3 || ok=0; done
if [ $ok -eq 1 ]; then
  runc 30 19 17 8 3
  t=$(left); [ $t -gt 60 ] && t=60; [ $t -gt 5 ] && runc $t 22 18 9 3
  t=$(left); [ $t -gt 5 ] && runc $t 23 21 10 3
fi
