#!/bin/bash
# second slot: (1) class sets of the prover's labelled hit files; (2) labelled cross-checks ext3 vs ext_indep5; (3) re-run of the
# prover's C4, C5, C7 from copies with SHA-256 comparison.
cd /home/user/Erdos-757/experiments/referee/L011-round3
P=/home/user/Erdos-757/experiments/prover/L011/out; L=logs/queue3b.txt
t0=$(date +%s)
zcat $P/hitsX20.txt.gz | grep '^HIT' | nice -n 5 ./bin/canon3 20 | cut -d' ' -f1 | sort -u > out/hc_prov_x20.cls; echo "prover hitsX20 classes: $(wc -l < out/hc_prov_x20.cls) [$(( $(date +%s)-t0 )) s]" >> $L
zcat $P/hitsX21.txt.gz | grep '^HIT' | nice -n 5 ./bin/canon3 21 | cut -d' ' -f1 | sort -u > out/hc_prov_x21.cls; echo "prover hitsX21 classes: $(wc -l < out/hc_prov_x21.cls) [$(( $(date +%s)-t0 )) s]" >> $L
zcat $P/hits21_17.txt.gz | grep '^HIT' | nice -n 5 ./bin/canon3 21 | cut -d' ' -f1 | sort -u > out/hc_prov_c6.cls; echo "prover hits21_17 classes: $(wc -l < out/hc_prov_c6.cls) [$(( $(date +%s)-t0 )) s]" >> $L
zcat $P/hits22_16.txt.gz | grep '^HIT' | nice -n 5 ./bin/canon3 22 | cut -d' ' -f1 | sort -u > out/hc_prov_c8.cls; echo "prover hits22_16 classes: $(wc -l < out/hc_prov_c8.cls) [$(( $(date +%s)-t0 )) s]" >> $L
# labelled cross-checks on random prover inputs
./src/labelled_xcheck.sh c4 20 7 $P/in21_12.txt 6 11 >> $L 2>&1
./src/labelled_xcheck.sh x20 19 7 $P/inX20_all.txt 40 12 >> $L 2>&1
./src/labelled_xcheck.sh x21iso 20 7 $P/inX21_1.txt 20 13 >> $L 2>&1
./src/labelled_xcheck.sh x21 20 7 $P/inX21_all.txt 30 14 >> $L 2>&1
./src/labelled_xcheck.sh c6 20 8 $P/in21_17_all.txt.gz 30 15 >> $L 2>&1
./src/labelled_xcheck.sh c8 21 8 $P/in22_16_all.txt.gz 30 16 >> $L 2>&1
echo "XCHECK-DONE [$(( $(date +%s)-t0 )) s]" >> $L
# re-run of the prover's pipeline from copies: C4, C5, C7 (each under 20 minutes)
mkdir -p out/rerun; cd out/rerun; PC=../prover_copy
nice -n 5 $PC/ext_indep5 20 7 3 < $P/in21_12.txt > hits21_12.txt; echo "C4 rerun: $(tail -n 1 hits21_12.txt) sha=$(sha256sum hits21_12.txt | cut -c1-16) prover=$(sha256sum $P/hits21_12.txt | cut -c1-16)" >> ../../$L
nice -n 5 $PC/filter_hits HIT < hits21_12.txt | tail -n 1 >> ../../$L
nice -n 5 $PC/ext_indep5 19 7 3 < $P/inX20_all.txt > hitsX20.txt; echo "C5 rerun: $(tail -n 1 hitsX20.txt) sha=$(sha256sum hitsX20.txt | cut -c1-16) recorded=5d68533cd1b79038 [$(( $(date +%s)-t0 )) s]" >> ../../$L
nice -n 5 $PC/filter_hits2 HIT notau < hitsX20.txt > filtX20.txt; echo "C5 filter: $(tail -n 1 filtX20.txt)" >> ../../$L
grep '^SURVIVOR' filtX20.txt | ../../bin/filt3 20 notau quiet >> ../../$L
nice -n 5 $PC/ext_indep5 20 7 3 < $P/inX21_all.txt > hitsX21.txt; echo "C7 rerun: $(tail -n 1 hitsX21.txt) sha=$(sha256sum hitsX21.txt | cut -c1-16) recorded=9f499ac0ea96d013 [$(( $(date +%s)-t0 )) s]" >> ../../$L
nice -n 5 $PC/filter_hits2 HIT notau < hitsX21.txt > filtX21.txt; echo "C7 filter: $(tail -n 1 filtX21.txt)" >> ../../$L
grep '^SURVIVOR' filtX21.txt | ../../bin/filt3 21 notau quiet >> ../../$L
rm -f hitsX20.txt hitsX21.txt filtX20.txt filtX21.txt
echo "RERUN-DONE [$(( $(date +%s)-t0 )) s]" >> ../../$L
