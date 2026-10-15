#!/usr/bin/env bash
D=/home/user/Erdos-757/experiments/referee/L004
S=/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad
cd $D
echo "== engine reruns $(date -u +%H:%M:%S)"
nice -n 10 python3 $D/rerun_engine.py 20 60 31415 > $D/rerun_engine.log 2>&1; tail -1 $D/rerun_engine.log
echo "== random sampler $(date -u +%H:%M:%S)"
nice -n 10 python3 $D/sample14.py $S/sample_seed7.gz 1800 7
echo "== SAT sample rest $(date -u +%H:%M:%S)"
bash $D/run_sat_batches.sh cubes_sample_rest_shuffled.txt 5 $S/sat_sample_rest
