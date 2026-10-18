#!/bin/bash
# (L014) resource monitor: every 30 s, the total RSS of all run_cells.py processes and of all processes of this folder's binaries,
# the largest single RSS, the size of out/ and the free disk; appended to out/resmon.tsv (stops after 3 hours).
cd /home/user/Erdos-757/experiments/prover/L014
end=$(( $(date +%s) + 10800 ))
while [ $(date +%s) -lt $end ]; do
  py=$(ps -eo rss,args | grep "python3 run_cells.py" | grep -v grep | awk '{s+=$1; if ($1>m) m=$1} END {print s+0, m+0}')
  bins=$(ps -eo rss,args | grep -E "L014/bin/|sort -u|awk !s" | grep -v grep | awk '{s+=$1} END {print s+0}')
  du=$(du -sm out 2>/dev/null | cut -f1); fr=$(df -m . | tail -1 | awk '{print $4}')
  echo -e "$(date -u +%T)\t$py\t$bins\t$du\t$fr" >> out/resmon.tsv
  sleep 30
done
