#!/usr/bin/env bash
# HY-assisted runs, n=13..16 (F7-free, with Henning-Yeo m-bound), then solver-only runs.
cd "$(dirname "$0")/../.."
export PYTHONPATH=.
D=experiments/20261013-2257-chyp-table
for n in 13 14 15 16; do python3 $D/run_n.py $n 1 3000 4 1; done
