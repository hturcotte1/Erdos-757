#!/usr/bin/env bash
# Lemma validation at N=12 (T=7, M=10): layered vs direct, plus record sets '12','12b','12c' present.
cd "$(dirname "$0")/../.."
export PYTHONPATH=.
D=experiments/20261014-0550-n16-layered
for mp in 5 6 7 8 9; do python3 $D/layer1.py 11 7 $mp 1500; done   # H' on 11 vertices, alpha<=7 (c_hyp(11)=7), HY: m'>=5
python3 $D/direct.py 12 7 10 1500
python3 $D/extend.py 12 7 10 0 1
python3 $D/finalize.py 12 10 1
