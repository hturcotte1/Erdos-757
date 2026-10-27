#!/bin/bash
cd /home/user/Erdos-757/experiments/falsify/kt-star-e1hub
for r in 1 2 3 4 5; do
  n=$(grep -l '"type": "cell"' main_25_15_9.part*.jsonl 2>/dev/null | wc -l)
  [ "$n" -ge 12 ] && break
  ./run_parts.sh
done
