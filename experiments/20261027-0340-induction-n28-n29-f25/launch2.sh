#!/bin/bash
cd "$(dirname "$0")"
until grep -q "^(20,16,8,3)" progress.tsv; do sleep 10; done
NPROC=2 nohup bash run_list2.sh chain2 24,20,10,3 26,18,10,3 27,21,11,3 > out/nohup_chain2.log 2>&1 &
NPROC=2 nohup bash run_list2.sh chain3 21,19,9,3 21,19,9,4 > out/nohup_chain3.log 2>&1 &
wait
