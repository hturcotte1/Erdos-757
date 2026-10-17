#!/bin/bash
cd /home/user/Erdos-757
export PYTHONPATH=.
D=experiments/20261017-0105-probe-n15-cells
python3 $D/probe.py 15 9 9 40 120 3 > $D/log_m9.txt 2>&1
python3 $D/probe.py 15 9 10 40 120 3 > $D/log_m10.txt 2>&1
python3 $D/probe.py 15 9 11 10 60 3 > $D/log_m11.txt 2>&1
python3 $D/probe.py 15 9 12 10 60 3 > $D/log_m12.txt 2>&1
