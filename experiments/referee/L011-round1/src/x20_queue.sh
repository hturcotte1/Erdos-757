#!/bin/bash
# Referee L011: worker for the direct (20,14,>=8) Delta<=3 search in C-relaxation (linear, F7-free), genbg -X-5, 400 parts.
# Parts are taken from the shared queue out/x20_queue.txt under flock; results appended to logs/x20_split_q.txt.
cd /home/user/Erdos-757/experiments/referee/L011-round1
W=$1
while true; do
  p=$( ( flock 9; p=$(head -n 1 out/x20_queue.txt); [ -n "$p" ] && sed -i 1d out/x20_queue.txt; echo "$p" ) 9> out/x20_queue.lock )
  [ -z "$p" ] && break
  TAU0=8 CMODE=1 ./bin/rgenbg -q -c -Z1 -d1:3 -D3:3 -X-5 20 14 42:42 $p/400 > out/gC_20_14_8_part_$p.txt 2> out/x20split_$p.err
  ( flock 9; echo "part $p $(cat out/x20split_$p.err) lines=$(grep -c '^G' out/gC_20_14_8_part_$p.txt)" >> logs/x20_split_q.txt ) 9> out/x20_log.lock
done
echo "WORKER $W DONE" >> logs/x20_split_q.txt
