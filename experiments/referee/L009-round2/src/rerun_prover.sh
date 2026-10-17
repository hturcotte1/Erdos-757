#!/bin/bash
# Referee L009 round 2: re-run of the prover's load-bearing pipeline C2-C7 from the prover's sources, in a fresh directory
# (out/pr), with outputs compared by SHA-256 to experiments/prover/L009/checksums_large_outputs.txt and to the gz files kept there.
set -e
P=/home/user/Erdos-757/experiments/prover/L009; R=/home/user/Erdos-757/experiments/referee/L009-round2; W=$R/out/pr
cd $W; mkdir -p indep rerun
for p in enum_conn ext_indep2 ext_indep3 filter_hits; do gcc -O2 -o indep/$p $P/indep/$p.c; done
cp $P/combine.py $P/connected_filter.py .
T() { s=$(date +%s); "$@"; e=$(date +%s); echo "   [$((e-s)) s]"; }
echo "== C2 component and window cells (enum_conn)"
cd indep
for c in "6 3 2 3 1" "8 5 3 3 1" "10 7 4 3 1" "10 8 4 3 1" "13 8 5 3 1" "13 9 5 3 1" "16 10 6 3 1"; do set -- $c
  nice -n 5 ./enum_conn $c > cell_$1_$2_$3.txt; tail -n 1 cell_$1_$2_$3.txt; done
for c in "16 9 6 3 0" "16 9 6 1000 0" "18 10 7 1000 0" "18 11 7 3 0"; do nice -n 5 ./enum_conn $c | tail -n 1; done
cd ..
echo "== C3 (17,12,7) case (iii) and (ii)"
python3 combine.py rerun/in17_C10_2AP.txt indep/cell_10_7_4.txt AP AP
nice -n 5 ./indep/ext_indep2 16 6 3 < rerun/in17_C10_2AP.txt > indep/hits17_C10_2AP.txt; tail -n 1 indep/hits17_C10_2AP.txt
./indep/filter_hits HIT < indep/hits17_C10_2AP.txt | tail -n 1
./indep/filter_hits FOUND < indep/cell_13_8_5.txt | tail -n 1
echo "== C4 components in C"
for c in 6_3_2 8_5_3 10_7_4 10_8_4 13_9_5 16_10_6; do nice -n 5 ./indep/filter_hits FOUND < indep/cell_$c.txt > rerun/filt_$c.txt; tail -n 1 rerun/filt_$c.txt; done
echo "== C5 rebuild (14,12,6)"
python3 combine.py rerun/inT14_a.txt AP rerun/filt_10_8_4.txt:SURVIVOR; python3 combine.py rerun/inT14_b.txt rerun/filt_13_9_5.txt:SURVIVOR
cat rerun/inT14_a.txt rerun/inT14_b.txt > rerun/inT14.txt
nice -n 5 ./indep/ext_indep2 13 5 3 < rerun/inT14.txt > indep/hitsT14.txt; tail -n 1 indep/hitsT14.txt
nice -n 5 ./indep/filter_hits HIT < indep/hitsT14.txt > rerun/filtT14.txt; tail -n 1 rerun/filtT14.txt
python3 connected_filter.py rerun/filtT14.txt indep/T14_conn.txt
echo "== C6 rebuild (17,13,7)"
python3 combine.py rerun/inT17_1.txt AP AP rerun/filt_10_8_4.txt:SURVIVOR; python3 combine.py rerun/inT17_2.txt AP rerun/filt_13_9_5.txt:SURVIVOR
python3 combine.py rerun/inT17_3.txt rerun/filt_10_7_4.txt:SURVIVOR rerun/filt_6_3_2.txt:SURVIVOR
python3 combine.py rerun/inT17_4.txt rerun/filt_8_5_3.txt:SURVIVOR rerun/filt_8_5_3.txt:SURVIVOR; python3 combine.py rerun/inT17_5.txt rerun/filt_16_10_6.txt:SURVIVOR
cat rerun/inT17_[1-5].txt > rerun/inT17.txt
nice -n 5 ./indep/ext_indep2 16 6 3 < rerun/inT17.txt > indep/hitsT17.txt; tail -n 1 indep/hitsT17.txt
nice -n 5 ./indep/filter_hits HIT < indep/hitsT17.txt > rerun/filtT17.txt; tail -n 1 rerun/filtT17.txt
python3 connected_filter.py rerun/filtT17.txt indep/T17_conn.txt
echo "== C7 final step"
python3 combine.py rerun/inH18_T17.txt indep/T17_conn.txt; python3 combine.py rerun/inH18_T14AP.txt indep/T14_conn.txt AP
cat rerun/inH18_T17.txt rerun/inH18_T14AP.txt > rerun/inH18.txt
nice -n 5 ./indep/ext_indep3 17 7 3 < rerun/inH18.txt > indep/hitsH18.txt; tail -n 1 indep/hitsH18.txt
echo "== SHA-256 comparison with the prover's recorded sums"
cd $W
( cd $P && cat checksums_large_outputs.txt ) | while read h f; do
  if [ -f "$f" ]; then h2=$(sha256sum "$f" | cut -d' ' -f1); [ "$h" = "$h2" ] && echo "same  $f" || echo "DIFF  $f"; else echo "absent $f (not regenerated here)"; fi; done
for f in indep/T14_conn.txt indep/cell_6_3_2.txt indep/cell_8_5_3.txt indep/cell_10_7_4.txt indep/cell_13_8_5.txt; do cmp -s $f $P/$f && echo "same as stored $f" || echo "DIFF stored $f"; done
for f in indep/T17_conn.txt indep/cell_10_8_4.txt indep/cell_13_9_5.txt indep/cell_16_10_6.txt indep/hitsT14.txt; do zcat $P/$f.gz | cmp -s - $f && echo "same as stored $f.gz" || echo "DIFF stored $f.gz"; done
