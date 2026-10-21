#!/bin/bash
# (L016) unpruned re-validation (L014's ext_validate.py, pyverify) of the final steps of the four sparse n = 27 top cells (run A's lists)
cd /home/user/Erdos-757/experiments/prover/L016
for k in "27 13 10 2" "27 14 10 3" "27 18 11 2" "27 19 11 3"; do
  CELLDIR=$PWD/out/cells ENGINELOG=/dev/null nice -n 10 timeout 1200 python3 ext_validate.py $k out/extval 2000 > out/extval_$(echo $k | tr ' ' '_').txt 2>&1
done
