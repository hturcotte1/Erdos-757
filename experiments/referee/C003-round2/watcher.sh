#!/bin/bash
# wait (up to 110 min) until the frozen verifier log has an exit line and the CP-SAT json exists
for i in $(seq 1 660); do
  if grep -q "exit=" /home/user/Erdos-757/experiments/referee/C003-round2/frozen_verifier.log && [ -s /home/user/Erdos-757/experiments/referee/C003-round2/solve_cpsat.json ]; then
    echo "both done at $(date -u)"; exit 0
  fi
  sleep 10
done
echo "watcher timed out at $(date -u)"; exit 1
