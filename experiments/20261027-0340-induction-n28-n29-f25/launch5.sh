#!/bin/bash
# waits for (26,18,10,3), then (27,21,11,3) with NPROC=4 (time pressure), then (28,24,12,3), (29,27,13,3)
cd "$(dirname "$0")"
until grep -q "^(26,18,10,3)" progress.tsv; do sleep 10; done
sleep 15
NPROC=4 bash run_list3.sh fin 27,21,11,3
NPROC=2 bash run_list3.sh fin 28,24,12,3 29,27,13,3
