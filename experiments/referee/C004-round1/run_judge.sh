#!/bin/bash
# Runs the frozen judge (read-only use) on the C004 claim; output goes to this scratch folder only.
D=/home/user/Erdos-757/experiments/referee/C004-round1
cd /home/user/Erdos-757 || exit 1
LOG="$D/judge_run.log"
echo "start $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$LOG"
timeout 1800 nice -n 10 python3 judge/judge.py results/claims/C004-lemmaE-SK5-E1.json >> "$LOG" 2>&1
echo "exit=$?" >> "$LOG"
echo "end $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
