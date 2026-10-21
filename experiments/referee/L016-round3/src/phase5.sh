#!/bin/bash
# after phase4: random sample of the d=3 branch of (24,16,9,3) (23-vertex inputs) with the own extension program; survivors must be in the prover's list
cd /home/user/Erdos-757/experiments/referee/L016-round3; export LC_ALL=C
CANON=/home/user/Erdos-757/experiments/prover/L012/bin/canon
echo "START phase5 $(date -u +%H:%M:%S)"
python3 src/sample.py out/in_24_16_9_3_d3.txt 4000 2024 > out/sample_24_16_9_3_d3.txt
grep '^FOUND' out/cells_L016/cells_new/runF/cell_24_16_9_D3.txt | $CANON 24 | sort -u > out/prover_24_16_9_3_classes.txt
nice -n 10 timeout 1500 ./bin/refext 23 8 9 3 2 3 < out/sample_24_16_9_3_d3.txt > out/refext_sample_24_16_9_3.txt; echo "rc=$?"; tail -1 out/refext_sample_24_16_9_3.txt
grep '^FOUND' out/refext_sample_24_16_9_3.txt | $CANON 24 | sort -u > out/sample_24_classes.txt
echo "d=3 sample: 4000 inputs; connected survivors $(grep -c '^FOUND' out/refext_sample_24_16_9_3.txt); classes $(wc -l < out/sample_24_classes.txt); not in prover's list: $(comm -23 out/sample_24_classes.txt out/prover_24_16_9_3_classes.txt | wc -l)"
nice -n 10 timeout 600 ./bin/refext 23 8 9 2 1 2 < out/in_24_16_9_3_d2.txt > out/refext_24_16_9_3_d2.txt; echo "d=2 branch (all 1511 inputs) rc=$?"; tail -1 out/refext_24_16_9_3_d2.txt
grep '^FOUND' out/refext_24_16_9_3_d2.txt | $CANON 24 | sort -u > out/d2_24_classes.txt
echo "d=2 branch: connected survivors $(grep -c '^FOUND' out/refext_24_16_9_3_d2.txt); classes $(wc -l < out/d2_24_classes.txt); not in prover's list: $(comm -23 out/d2_24_classes.txt out/prover_24_16_9_3_classes.txt | wc -l)"
echo "ALL DONE phase5 $(date -u +%H:%M:%S)"
