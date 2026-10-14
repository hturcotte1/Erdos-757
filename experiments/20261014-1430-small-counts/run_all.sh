#!/bin/bash
# one process at a time, niced.  from repo root.
set -x
D=experiments/20261014-1430-small-counts
nice -n 10 python3 $D/counts.py 9 6 7
nice -n 10 python3 $D/counts.py 10 7 8
# n=11 saturated (m=9): prefix-split driver (P=1, no --refl) + postprocess pipeline of the L002 census
nice -n 10 python3 -m e757.ordered_dfs_split 11 7 9 2 1 $D/n11/results --nice 10
nice -n 10 python3 experiments/20261014-1005-census-dfs/postprocess.py 11 7 9 $D/n11/results n11_m9 1
# n=11 non-saturated: first 300 patterns in DFS order realized (sample), DFS counts are exact (dfscount.py)
nice -n 10 python3 $D/counts.py --sample 300 11 6 7 8
