#!/bin/bash
cd /home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2
timeout 4000 nice -n 10 python3 w1.py 4 0 1 25 nc > w1_k4_nc.log 2>&1
timeout 6000 nice -n 10 python3 w1.py 3 0 1 25 nc > w1_k3_nc.log 2>&1
timeout 3000 nice -n 10 python3 w1.py 2 0 1 25 nc > w1_k2_nc.log 2>&1
