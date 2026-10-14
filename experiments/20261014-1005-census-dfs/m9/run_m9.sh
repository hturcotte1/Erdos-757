#!/usr/bin/env bash
# (12, m=9, alpha<=7) enumeration in class O (F7-free), then filter (K30/K31/cores)
set -e
cd /home/user/Erdos-757/experiments/20261014-1005-census-dfs
mkdir -p m9
e757_bin=../../e757/c/ordered_dfs
$e757_bin n=12 T=7 m_min=9 m_exact=9 f7=1 mode=enum progress=0 | gzip > m9/n12_m9_all.raw.gz
zcat m9/n12_m9_all.raw.gz | tail -1 > m9/dfs_done.txt || true
zcat m9/n12_m9_all.raw.gz | ./filter cores.txt 2> m9/filter.stderr | gzip > m9/n12_m9_filtered.txt.gz
echo finished
