#!/bin/bash
# mode-all robustness runs (every Delta<=3 class as component, in C or not): X20 (230 inputs) and C8 (267 inputs)
cd /home/user/Erdos-757/experiments/referee/L011-round3
s=$(date +%s); nice -n 5 ./bin/ext3 19 7 3 1 < out/ain_x20_all.txt > out/ext_x20_all.txt; echo "x20 mode-all: $(tail -n 1 out/ext_x20_all.txt) [$(( $(date +%s)-s )) s]" >> logs/classlevel3.txt
s=$(date +%s); nice -n 5 ./bin/ext3 21 8 3 1 < out/ain_c8_all.txt > out/ext_c8_all.txt; echo "c8 mode-all: $(tail -n 1 out/ext_c8_all.txt) [$(( $(date +%s)-s )) s]" >> logs/classlevel3.txt
echo MODEALL-DONE >> logs/classlevel3.txt
