#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L016-round3
until grep -q "chunks done" logs/phase3.log; do sleep 5; done
pkill -f "bash src/phase3.sh"; sleep 1; pkill -x genbg30; pkill -x g6filt; sleep 1
echo "phase3 stopped after the chunks at $(date -u +%H:%M:%S)"
nohup bash src/phase4.sh > logs/phase4.log 2>&1 &
