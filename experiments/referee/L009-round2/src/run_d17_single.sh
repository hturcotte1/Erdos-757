#!/bin/bash
# direct genbg enumeration, connected linear (17,13,tau>=7), Delta<=3, F7-free (F7 prune), single process (no res/mod split)
cd /home/user/Erdos-757/experiments/referee/L009-round2
TAU0=7 F7PRUNE=1 nice -n 5 out/bin/genbg_r2 -q -c -Z1 -d1:3 -D3:3 17 13 39:39 > out/direct/d17_single.txt 2> out/direct/d17_single.err
echo "exit $?" >> out/direct/d17_single.err
