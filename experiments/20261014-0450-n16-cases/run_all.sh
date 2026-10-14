#!/usr/bin/env bash
# Resumable master: n=16 case split (4 parallel, workers=1 each), then the feasible-size sweep.
# Relaunch after a restart with:
#   bash scripts/start_job.sh experiments/20261014-0450-n16-cases 14 bash experiments/20261014-0450-n16-cases/run_all.sh
cd "$(dirname "$0")/../.."
export PYTHONPATH=.
python3 experiments/20261014-0450-n16-cases/driver.py 4 3000
python3 experiments/20261014-0030-feasible-sizes/run_sweep.py 3600 4
