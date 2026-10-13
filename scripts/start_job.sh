#!/usr/bin/env bash
# Start a long computation in the background, detached from the Claude Code turn.
# Usage: bash scripts/start_job.sh experiments/<YYYYMMDD-HHMM>-<slug> <max_hours> <command...>
# Writes <dir>/run.log and <dir>/job.pid. Check on jobs with: bash scripts/jobs.sh
set -euo pipefail
cd "$(dirname "$0")/.."
[ $# -ge 3 ] || { echo "usage: bash scripts/start_job.sh <dir> <max_hours> <command...>"; exit 2; }
dir="$1"; hours="$2"; shift 2
mkdir -p "$dir"
if command -v timeout >/dev/null; then TO=(timeout "${hours}h")
elif command -v gtimeout >/dev/null; then TO=(gtimeout "${hours}h")
else TO=(); echo "warning: no timeout command; the job has no time limit"; fi
{
  echo "# started $(date -u +%Y-%m-%dT%H:%M:%SZ) max ${hours}h"
  echo "# command: $*"
} > "$dir/run.log"
nohup "${TO[@]}" "$@" >> "$dir/run.log" 2>&1 < /dev/null &
echo $! > "$dir/job.pid"
echo "started pid $(cat "$dir/job.pid"); log: $dir/run.log"
