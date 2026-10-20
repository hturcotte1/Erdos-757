#!/bin/bash
# direct genbg enumeration, connected linear (17,13,tau>=7), Delta<=3, tau prune only (no F7 prune), single process
cd /home/user/Erdos-757/experiments/referee/L009-round2
TAU0=7 nice -n 5 out/bin/genbg_r2 -q -c -Z1 -d1:3 -D3:3 17 13 39:39 > out/direct/d17_tauonly.txt 2> out/direct/d17_tauonly.err
echo "exit $?" >> out/direct/d17_tauonly.err
