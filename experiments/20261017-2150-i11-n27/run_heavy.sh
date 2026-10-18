#!/bin/bash
# heavy chain, resumable (chunked) runner; NPROC=1, nice 19; stops at the absolute cap time CAP_EPOCH (6 h after the start 2026-10-17 21:48:58 UTC)
cd "$(dirname "$0")"
export CELLDIR=$PWD/out/cells ENGINELOG=$PWD/out/engine.log NPROC=1 MD=10 CHUNK=${CHUNK:-25000}
CAP_EPOCH=${CAP_EPOCH:-$(date -u -d '2026-10-18 03:48:58' +%s)}
for c in "25 19 10 3" "26 22 11 3" "27 25 12 3"; do
  set -- $c; f=out/cells/cell_$1_$2_$3_D$4.txt
  [ -e $f ] && continue
  left=$(( CAP_EPOCH - $(date +%s) )); [ $left -lt 60 ] && { echo CAP reached before $c; break; }
  echo "$(date -u +%T) START $c timeout $left free $(df -BG --output=avail . | tail -1)"
  nice -n 19 timeout $left python3 run_one2.py $c > out/run_$1_$2_$3_D$4.log 2>&1
  rc=$?; echo "$(date -u +%T) END $c rc $rc"
  [ $rc -ne 0 ] && { printf '(%s,%s,%s,%s)\tINTERRUPTED_rc%d_at_%s (resumable: out/chunks)\t-\t-\t-\t-\t-\n' $1 $2 $3 $4 $rc $(date -u +%T) >> progress.tsv; break; }
done
echo HEAVY DONE
