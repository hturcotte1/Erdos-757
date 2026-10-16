#!/bin/bash
# n=11 first-300 samples (census binary used only as a pattern source), decided by my realdec.py
D=/home/user/Erdos-757/experiments/referee/L003
cd $D
for m in 6 7 8; do
  nice -n 10 /home/user/Erdos-757/e757/c/ordered_dfs n=11 T=7 m_min=$m m_exact=$m f7=1 progress=0 mode=enum limit=300 \
    | awk '/^SOL/{printf "PAT"; for(i=2;i<=NF;i++) printf " %s", $i; printf "\n"} /^DONE/{print > "/dev/stderr"}' \
    | nice -n 10 python3 realdec.py 11 7 h
done
