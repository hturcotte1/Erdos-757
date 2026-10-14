#!/usr/bin/env bash
# Resumable chain: census n=12 (if not finished), then n=14 (T=8,m=12), then n=15 (T=9,m=13); 2 h limit each for 14/15.
# Relaunch: bash scripts/start_job.sh experiments/20261014-0610-extremal-census 6 bash experiments/20261014-0610-extremal-census/run_chain.sh
cd "$(dirname "$0")/../.."
export PYTHONPATH=.
D=experiments/20261014-0610-extremal-census
while pgrep -f "[c]ensus.py 12 7 10" > /dev/null; do sleep 20; done   # wait for a directly launched n=12 run
python3 $D/census.py 12 7 10 3600
python3 $D/census.py 14 8 12 7200
python3 $D/census.py 15 9 13 7200
