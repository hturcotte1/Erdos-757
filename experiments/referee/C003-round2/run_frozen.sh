#!/bin/bash
# Wrapper: run the frozen verifier (judge/judge.py) on the claim; log to the referee scratch folder.
cd /home/user/Erdos-757
LOG=/home/user/Erdos-757/experiments/referee/C003-round2/frozen_verifier.log
{
  date -u
  sha256sum judge/judge.py
  nice -n 10 timeout 7200 python3 judge/judge.py results/claims/C003-reader-5-9-K6.json
  echo "exit=$?"
  date -u
} > "$LOG" 2>&1
