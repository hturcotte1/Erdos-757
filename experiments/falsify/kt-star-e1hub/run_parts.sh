#!/bin/bash
# resumable chunked run of cell (25,15,9): 12 parts, each its own output file; a part is done when its jsonl contains a "cell" record
cd /home/user/Erdos-757/experiments/falsify/kt-star-e1hub
for i in $(seq 0 11); do
  f=main_25_15_9.part$i.jsonl
  if [ -f $f ] && grep -q '"type": "cell"' $f; then continue; fi
  rm -f $f
  PART=$i/12 nice -n 10 timeout 3000 python3 run_main.py $f 25,15,9 > main_25_15_9.part$i.log 2>&1
done
