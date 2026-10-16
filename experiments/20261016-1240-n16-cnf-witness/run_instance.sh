#!/usr/bin/env bash
# usage: run_instance.sh M TAG ; hard 12600 s limit (cadical is not interruptible through pysat)
cd "$(dirname "$0")"
M=$1; TAG=$2
timeout 12600 nice -n 5 python3 build_cnf.py solve 16 9 $M $TAG cadical195
rc=$?
if [ $rc -eq 124 ]; then
  python3 - <<PY
import json
r=json.load(open("result_$TAG.json")); r["status"]="TIMEOUT"; r["wall_s"]=12600; r["note"]="killed by timeout 12600 (cadical running, no answer)"
json.dump(r,open("result_$TAG.json","w"),indent=1)
PY
  echo "TIMEOUT $TAG"
fi
echo "exit $rc"
