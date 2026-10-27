#!/bin/bash
# usage: run_all.sh "n list" : runs bin/redfree on all out/cls_n_m.txt
for n in $1; do for f in out/cls_${n}_*.txt; do m=${f##*_}; m=${m%.txt}; [ -s $f ] && nice -n 5 bin/redfree $n < $f > out/red_${n}_${m}.tsv; done; done
echo done > out/red_done_$(echo $1 | tr ' ' _)
