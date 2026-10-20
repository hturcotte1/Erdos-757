#!/bin/bash
# re-run of the prover's C7 (Lemma X21 labelled extension) from the copied sources, with SHA-256 comparison and filter counts
cd /home/user/Erdos-757/experiments/referee/L011-round3/out/rerun; P=/home/user/Erdos-757/experiments/prover/L011/out; PC=../prover_copy; L=../../logs/queue3b.txt
s=$(date +%s); nice -n 5 $PC/ext_indep5 20 7 3 < $P/inX21_all.txt > hitsX21.txt
echo "C7 rerun: $(tail -n 1 hitsX21.txt) sha=$(sha256sum hitsX21.txt | cut -c1-16) recorded=9f499ac0ea96d013 [$(( $(date +%s)-s )) s]" >> $L
nice -n 5 $PC/filter_hits2 HIT notau < hitsX21.txt > filtX21.txt; echo "C7 filter: $(tail -n 1 filtX21.txt)" >> $L
python3 -I /home/user/Erdos-757/experiments/prover/L011/connected_filter2.py filtX21.txt X21_conn.txt 21 >> $L 2>&1
rm -f hitsX21.txt filtX21.txt; echo "C7-RERUN-DONE" >> $L
