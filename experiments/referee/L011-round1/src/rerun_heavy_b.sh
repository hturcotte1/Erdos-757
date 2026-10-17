#!/bin/bash
# Referee L011: re-run (copies of the prover's programs) of C8 part03 (+ F7/P3 filter).
cd /home/user/Erdos-757/experiments/referee/L011-round1/out/rerun
s=$(date +%s); ./bin/ext_indep5 21 8 3 < out/in22_16_part03 > out/hits22_16_part03.txt; echo "C8 part03: $(tail -n 1 out/hits22_16_part03.txt) [$(( $(date +%s) - s )) s]"
s=$(date +%s); ./bin/filter_hits2 HIT notau < out/hits22_16_part03.txt > out/filt22_16_part03.txt; echo "C8 part03 filter: $(tail -n 1 out/filt22_16_part03.txt) [$(( $(date +%s) - s )) s]"
