#!/bin/bash
# direct genbg enumeration, connected linear (17,13,tau>=7), Delta<=3, F7-free (F7 prune), part $1 of 2
cd /home/user/Erdos-757/experiments/referee/L009-round2
TAU0=7 F7PRUNE=1 nice -n 5 out/bin/genbg_r2 -q -c -Z1 -d1:3 -D3:3 -X-3 17 13 39:39 $1/2 > out/direct/d17_p$1.txt 2> out/direct/d17_p$1.err
echo "exit $?" >> out/direct/d17_p$1.err
