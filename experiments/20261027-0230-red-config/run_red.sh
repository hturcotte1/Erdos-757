#!/bin/bash
# usage: run_red.sh n m  -> out/red_n_m.tsv
n=$1; m=$2
nice -n 5 bin/redfree $n < out/cls_${n}_${m}.txt > out/red_${n}_${m}.tsv
