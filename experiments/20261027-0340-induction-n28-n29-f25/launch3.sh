#!/bin/bash
cd "$(dirname "$0")"
until grep -q "^(27,21,11,3)" progress.tsv; do sleep 10; done
NPROC=2 bash run_list2.sh fin 28,24,12,3 29,27,13,3
