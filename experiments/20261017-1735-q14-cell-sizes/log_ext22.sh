#!/bin/bash
# logs input bytes consumed by the ext_d process of cell (22,18,9,3) (input file order = decomposition order), every 60 s
f=out/cells/tmp_22_18_9_D3_d3_tp8.in; echo "# input file bytes: $(stat -c %s $f), lines: $(wc -l < $f)" > ext22_progress.log
while true; do
  p=$(for q in $(pgrep -f "q14-cell-sizes/bin/ext_d 21 8 9 3 2"); do [ "$(cat /proc/$q/comm)" = ext_d ] && echo $q; done | tail -1); [ -z "$p" ] && break
  echo "$(date -u +%H:%M:%S) rchar=$(grep rchar /proc/$p/io | awk '{print $2}') cputime_ticks=$(awk '{print $14+$15}' /proc/$p/stat)" >> ext22_progress.log; sleep 60
done
