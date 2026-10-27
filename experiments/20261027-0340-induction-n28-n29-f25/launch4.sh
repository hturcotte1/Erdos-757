#!/bin/bash
# waits for (26,18,10,3), then runs (27,21,11,3), (28,24,12,3), (29,27,13,3) in sequence (run_list3.sh: disk guard 3 GB)
cd "$(dirname "$0")"
until grep -q "^(26,18,10,3)" progress.tsv; do sleep 10; done
sleep 20
NPROC=2 bash run_list3.sh fin 27,21,11,3 28,24,12,3 29,27,13,3
