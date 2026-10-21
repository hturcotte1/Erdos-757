#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L016-round3; export LC_ALL=C
CANON=/home/user/Erdos-757/experiments/prover/L012/bin/canon
echo "START phase4 (own full recomputation of cell(25,19,10,3)) $(date -u +%H:%M:%S)"
nice -n 10 timeout 4200 ./bin/refext 24 9 10 3 2 3 < out/in_25_19_10_3.txt > out/refext_25_19_10_3_full.txt; echo "refext rc=$? $(date -u +%H:%M:%S)"
tail -1 out/refext_25_19_10_3_full.txt
grep '^FOUND' out/refext_25_19_10_3_full.txt | $CANON 25 | sort -u > out/own_25_19_10_3_classes.txt
echo "own connected survivors: $(grep -c '^FOUND' out/refext_25_19_10_3_full.txt); own classes: $(wc -l < out/own_25_19_10_3_classes.txt); prover classes: $(wc -l < out/prover_25_19_10_3_classes.txt); identical sets: $(cmp -s out/own_25_19_10_3_classes.txt out/prover_25_19_10_3_classes.txt && echo YES || echo NO); own-not-prover: $(comm -23 out/own_25_19_10_3_classes.txt out/prover_25_19_10_3_classes.txt | wc -l); prover-not-own: $(comm -13 out/own_25_19_10_3_classes.txt out/prover_25_19_10_3_classes.txt | wc -l)"
echo "ALL DONE phase4 $(date -u +%H:%M:%S)"
