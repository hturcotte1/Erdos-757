#!/bin/bash
# Referee L011: re-run (copies of the prover's programs) of C6 part00 (+ exact-tau filter) and the C2 long1 cell (19,11,7).
cd /home/user/Erdos-757/experiments/referee/L011-round1/out/rerun
s=$(date +%s); ./bin/ext_indep5 20 8 3 < out/in21_17_part00 > out/hits21_17_part00.txt; echo "C6 part00: $(tail -n 1 out/hits21_17_part00.txt) [$(( $(date +%s) - s )) s]"
s=$(date +%s); ./bin/filter_hits HIT < out/hits21_17_part00.txt > out/filt21_17_part00.txt; echo "C6 part00 filter: $(tail -n 1 out/filt21_17_part00.txt) [$(( $(date +%s) - s )) s]"
echo "C6 part00 hits sha256 $(sha256sum < out/hits21_17_part00.txt | cut -c1-64); prover gz $(zcat /home/user/Erdos-757/experiments/prover/L011/out/hits21_17.txt.gz | grep '^HIT' | sha256sum | cut -c1-64); mine HIT-only $(grep '^HIT' out/hits21_17_part00.txt | sha256sum | cut -c1-64)"
s=$(date +%s); ./bin/enum_conn 19 11 7 3 1 > out/cell_19_11_7.txt; echo "C2 long1: $(tail -n 1 out/cell_19_11_7.txt) [$(( $(date +%s) - s )) s]"
cmp out/cell_19_11_7.txt /home/user/Erdos-757/experiments/prover/L011/out/cell_19_11_7.txt && echo "cell_19_11_7 byte-identical to prover's"
