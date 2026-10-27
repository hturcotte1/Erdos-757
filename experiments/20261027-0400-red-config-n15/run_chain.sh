#!/bin/bash
# generate all connected Delta<=3 members of C on 15 vertices for m=7..13 and run the exact (Red) test (redmin) on each; progress.tsv
cd $(dirname $0); H=$PWD
guard() { a=$(df --output=avail -B1G /home/user | tail -1 | tr -d ' '); if [ "$a" -lt 8 ]; then echo "DISK GUARD: only ${a}G free, stopping" >> progress.tsv; exit 3; fi; }
log() { echo -e "$(date -u +%H:%M:%S)\t$*" >> progress.tsv; }
for m in 7 8 9 10 11 12; do
  guard
  if [ ! -s out/cls_15_$m.txt.gz ]; then log "gen 15 $m start"; nice -n 19 timeout 3h ./gen15.sh 15 $m out/cls_15_$m.txt.gz || { log "gen 15 $m FAILED"; exit 1; }; fi
  log "gen 15 $m done classes=$(zcat out/cls_15_$m.txt.gz | wc -l)"
  rm -f out/hits_15_$m.tsv
  nice -n 19 timeout 3h bash -c "zcat out/cls_15_$m.txt.gz | bin/redmin 15 out/hits_15_$m.tsv 6" > out/summary_15_$m.txt || { log "redmin 15 $m FAILED"; exit 1; }
  log "redmin 15 $m $(cut -c1-120 out/summary_15_$m.txt)"
done
guard
log "gen+redmin 15 13 start (streamed)"
rm -f out/hits_15_13.tsv
nice -n 19 timeout 4h bash -c "./gen15.sh 15 13 - | tee >(wc -l > out/count_15_13.txt) | bin/redmin 15 out/hits_15_13.tsv 6" > out/summary_15_13.txt || { log "15 13 FAILED"; exit 1; }
log "redmin 15 13 $(cut -c1-120 out/summary_15_13.txt) classes=$(cat out/count_15_13.txt)"
log "ALL DONE"
