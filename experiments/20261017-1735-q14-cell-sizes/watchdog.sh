#!/bin/bash
# kills this experiment's jobs if free disk on / drops below 700 MB (shared machine; protects other agents)
while true; do
  free=$(df --output=avail -m / | tail -1)
  if [ "$free" -lt 700 ]; then
    echo "$(date -u) free=${free}MB: killing" >> out/watchdog.log
    ps aux | grep -E "q14-cell-sizes" | grep -v grep | grep -v watchdog | awk '{print $2}' | xargs -r kill
  fi
  sleep 5
done
