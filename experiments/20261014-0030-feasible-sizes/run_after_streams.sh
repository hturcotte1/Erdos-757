#!/usr/bin/env bash
# Wait for the n=15 layer-1 streams to finish, then run the resumable sweep (1 h per size, 3 workers).
cd "$(dirname "$0")/../.."
while pgrep -f "layer1.py" >/dev/null; do sleep 60; done
export PYTHONPATH="$PWD"; exec python3 experiments/20261014-0030-feasible-sizes/run_sweep.py 3600 3
