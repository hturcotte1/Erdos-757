#!/usr/bin/env bash
# Usage: run_layer1.sh NP T "MP list" TIME_S [PAR=3]   -- resumable (finished streams are skipped)
cd "$(dirname "$0")/../.."
export PYTHONPATH=.
NP=$1; T=$2; MPS=$3; TL=$4; PAR=${5:-3}
for mp in $MPS; do echo $mp; done | xargs -P $PAR -I{} python3 experiments/20261014-0550-n16-layered/layer1.py $NP $T {} $TL
