#!/usr/bin/env bash
# List background jobs started with scripts/start_job.sh and show the end of each log.
cd "$(dirname "$0")/.."
found=0
for pidf in $(find experiments -name job.pid 2>/dev/null | sort); do
  found=1
  d=$(dirname "$pidf"); pid=$(cat "$pidf")
  if kill -0 "$pid" 2>/dev/null; then state="RUNNING"; else state="finished"; fi
  echo "== $d  pid=$pid  $state"
  tail -n 3 "$d/run.log" 2>/dev/null | sed 's/^/   /'
done
[ $found -eq 1 ] || echo "no jobs"
