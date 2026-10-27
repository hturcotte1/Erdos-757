#!/bin/bash
cd /home/user/Erdos-757/experiments/falsify/i11-structure-lemmas
nice -n 10 python3 src/part1d_newtight.py > part1d.log 2>&1
nice -n 10 python3 src/part1c_control.py > part1c.log 2>&1
nice -n 10 python3 src/part1b_glue.py > part1b.log 2>&1
# positive control for the local search: do we find known tight / slack-1 cells?
for nm in "10 7" "14 12" "17 13" "12 10" "15 11" "19 16" "22 17"; do
  for ps in 0.0 0.6; do
    echo "n,m=$nm pseed=$ps: $(nice -n 10 timeout 300 src/lsearch $nm 20000 300 11 0.5 $ps seeds.txt | tail -1 | cut -c1-160)" >> poscontrol3b.log
  done
done
echo MISCDONE >> poscontrol3b.log
