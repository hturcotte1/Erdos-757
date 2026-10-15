#!/usr/bin/env bash
D=/home/user/Erdos-757/experiments/referee/L004
S=/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad
bash $D/run_sat_batches.sh cubes_cheap.txt 100 $S/sat_cheap
bash $D/run_sat_batches.sh cubes_sample.txt 10 $S/sat_sample
