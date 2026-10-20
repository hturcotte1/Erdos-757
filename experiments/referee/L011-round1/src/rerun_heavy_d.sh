#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L011-round1/out/rerun
for p in 00 01 02; do s=$(date +%s); ./bin/ext_indep5 21 8 3 < out/in22_16_part$p > out/hits22_16_part$p.txt; echo "C8 part$p: $(tail -n 1 out/hits22_16_part$p.txt) [$(( $(date +%s) - s )) s]"
  s=$(date +%s); ./bin/filter_hits2 HIT notau < out/hits22_16_part$p.txt > out/filt22_16_part$p.txt; echo "C8 part$p filter: $(tail -n 1 out/filt22_16_part$p.txt) [$(( $(date +%s) - s )) s]"; done
