#!/bin/bash
# noprune validation (L014/L016 C4 style) of the top cells with the ORIGINAL Gosper ext_d (L016 bin/ext_d, MAXP 640), pure-Python pyverify
cd "$(dirname "$0")"
export CELLDIR=$PWD/../out/cells ENGINELOG=$PWD/../out/engine_val.log
for k in 29,27,13,3 28,23,12,3 28,18,11,3 28,17,11,2 29,16,11,3 29,15,11,2 29,22,12,3 27,20,11,3 26,17,10,3; do
  echo "=== $k"; nice -n 5 timeout 1500 python3 ext_validate.py ${k//,/ } out_val 50 2>&1 | tail -6
done
