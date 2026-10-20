#!/bin/bash
# Referee L011: direct search (no rebuild) for connected linear F7-free (20,14,>=8) 3-graphs with Delta <= 3:
# genbg + rhooks (tau prune + F7 prune), split -X-5 into 400 parts; this script runs parts START, START+STEP, ... < 400.
cd /home/user/Erdos-757/experiments/referee/L011-round1
START=$1; STEP=$2
for ((p=START; p<400; p+=STEP)); do
  TAU0=8 CMODE=1 ./bin/rgenbg -q -c -Z1 -d1:3 -D3:3 -X-5 20 14 42:42 $p/400 >> out/gC_20_14_8_split_$START.txt 2> out/x20split_$p.err
  echo "part $p $(cat out/x20split_$p.err)" >> logs/x20_split_$START.txt
done
echo "STREAM $START DONE" >> logs/x20_split_$START.txt
