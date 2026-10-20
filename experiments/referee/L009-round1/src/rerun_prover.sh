#!/bin/bash
# Referee L009: re-run the prover's labelled pipeline (C2-C7) with the prover's own programs (recompiled into ../bin) and
# scripts, writing every output under out/pr (nothing is written into the prover's folder).  One process at a time, nice 5.
set -e
R=/home/user/Erdos-757/experiments/referee/L009-round1; P=/home/user/Erdos-757/experiments/prover/L009; O=$R/out/pr
cd $O
EC=$R/bin/enum_conn_prover; X2=$R/bin/ext_indep2_prover; X3=$R/bin/ext_indep3_prover; FH=$R/bin/filter_hits_prover
t() { local s=$(date +%s); "$@"; echo "   [$(( $(date +%s) - s )) s]" >&2; }
echo "== C2"
for c in "6 3 2" "8 5 3" "10 7 4" "10 8 4" "13 8 5" "13 9 5" "16 10 6"; do set -- $c
  t nice -n 5 $EC $1 $2 $3 3 1 > cell_$1_$2_$3.txt; tail -n 1 cell_$1_$2_$3.txt; done
for c in "16 9 6 3" "16 9 6 1000" "18 10 7 1000" "18 11 7 3"; do set -- $c; t nice -n 5 $EC $1 $2 $3 $4 0 | tail -n 1; done
echo "== C3"
python3 $P/combine.py in17_C10_2AP.txt cell_10_7_4.txt AP AP
t nice -n 5 $X2 16 6 3 < in17_C10_2AP.txt > hits17_C10_2AP.txt; tail -n 1 hits17_C10_2AP.txt
$FH HIT < hits17_C10_2AP.txt | tail -n 1
python3 $P/combine.py in17_C13_AP.txt cell_13_8_5.txt AP
t nice -n 5 $X2 16 6 3 < in17_C13_AP.txt > hits17_C13_AP.txt; tail -n 1 hits17_C13_AP.txt; $FH HIT < hits17_C13_AP.txt | tail -n 1
$FH FOUND < cell_13_8_5.txt | tail -n 1
echo "== C4"
for c in 6_3_2 8_5_3 10_7_4 10_8_4 13_9_5 16_10_6; do $FH FOUND < cell_$c.txt > filt_$c.txt; tail -n 1 filt_$c.txt; done
echo "== C5"
python3 $P/combine.py inT14_a.txt AP filt_10_8_4.txt:SURVIVOR; python3 $P/combine.py inT14_b.txt filt_13_9_5.txt:SURVIVOR
cat inT14_a.txt inT14_b.txt > inT14.txt
t nice -n 5 $X2 13 5 3 < inT14.txt > hitsT14.txt; tail -n 1 hitsT14.txt
t nice -n 5 $FH HIT < hitsT14.txt > filtT14.txt; tail -n 1 filtT14.txt
python3 $P/connected_filter.py filtT14.txt T14_conn.txt
echo "== C6"
python3 $P/combine.py inT17_1.txt AP AP filt_10_8_4.txt:SURVIVOR; python3 $P/combine.py inT17_2.txt AP filt_13_9_5.txt:SURVIVOR
python3 $P/combine.py inT17_3.txt filt_10_7_4.txt:SURVIVOR filt_6_3_2.txt:SURVIVOR
python3 $P/combine.py inT17_4.txt filt_8_5_3.txt:SURVIVOR filt_8_5_3.txt:SURVIVOR; python3 $P/combine.py inT17_5.txt filt_16_10_6.txt:SURVIVOR
cat inT17_[1-5].txt > inT17.txt
t nice -n 5 $X2 16 6 3 < inT17.txt > hitsT17.txt; tail -n 1 hitsT17.txt
t nice -n 5 $FH HIT < hitsT17.txt > filtT17.txt; tail -n 1 filtT17.txt
python3 $P/connected_filter.py filtT17.txt T17_conn.txt
echo "== C7"
python3 $P/combine.py inH18_T17.txt T17_conn.txt; python3 $P/combine.py inH18_T14AP.txt T14_conn.txt AP
cat inH18_T17.txt inH18_T14AP.txt > inH18.txt
t nice -n 5 $X3 17 7 3 < inH18.txt > hitsH18.txt; tail -n 1 hitsH18.txt
echo "== sha256"
sha256sum T14_conn.txt T17_conn.txt cell_10_8_4.txt cell_13_9_5.txt cell_16_10_6.txt hits17_C10_2AP.txt hitsT14.txt hitsT17.txt filtT14.txt filtT17.txt filt_10_8_4.txt filt_13_9_5.txt filt_16_10_6.txt inH18.txt inT14.txt inT17.txt
