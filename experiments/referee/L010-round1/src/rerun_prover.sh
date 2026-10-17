#!/bin/bash
# Referee L010 r1: re-run of the prover's computations C2-C6 with copies of the prover's/falsifier's programs (compiled in
# out/rerun/bin), all outputs in out/rerun (the prover's folder is not touched).  Inputs from L008/L009 as in reproduce.sh.
set -e
R=/home/user/Erdos-757/experiments/referee/L010-round1/out/rerun; cd $R
L8=/home/user/Erdos-757/experiments/prover/L008/indep; L9=/home/user/Erdos-757/experiments/prover/L009/indep
B=$R/bin
t() { local s=$(date +%s); "$@"; echo "   [$(( $(date +%s)-s )) s]"; }
echo "== C2 enumerations"
for c in "8 6 3 3" "9 4 3 3" "11 6 4 3" "11 7 4 3" "14 8 5 3" "17 9 6 3" "16 9 6 3"; do set -- $c; t $B/enum_conn $1 $2 $3 $4 1 > cell_$1_$2_$3.txt; tail -n1 cell_$1_$2_$3.txt; done
for c in "19 9 7 1000" "19 10 7 3" "20 12 8 2" "18 12 7 2" "20 13 8 2"; do set -- $c; t $B/enum_conn $1 $2 $3 $4 0 | tail -n1; done
echo "== C3 filters"
for c in 6_3_2 8_5_3 10_7_4 13_8_5; do $B/filter_hits FOUND < $L9/cell_$c.txt > filt_$c.txt; tail -n1 filt_$c.txt; done
zcat $L8/mine_12_10_5_deg3.txt.gz > cell_12_10_5.txt; zcat $L8/mine_15_11_6_deg3.txt.gz > cell_15_11_6.txt
for c in 8_6_3 9_4_3 11_7_4 14_8_5 12_10_5 15_11_6; do $B/filter_hits FOUND < cell_$c.txt > filt_$c.txt; tail -n1 filt_$c.txt; done
echo "== C4 rebuild"
python3 -I combine.py inX_3.txt filt_8_5_3.txt:SURVIVOR filt_9_4_3.txt:SURVIVOR
python3 -I combine.py inX_5.txt AP filt_14_8_5.txt:SURVIVOR
python3 -I combine.py inX_7.txt AP filt_6_3_2.txt:SURVIVOR filt_8_5_3.txt:SURVIVOR
python3 -I combine.py inX_8.txt AP AP filt_11_7_4.txt:SURVIVOR
python3 -I combine.py inX_9.txt AP AP filt_10_7_4.txt:SURVIVOR ISO
python3 -I combine.py inX_10.txt AP AP AP filt_8_6_3.txt:SURVIVOR
cat inX_3.txt inX_5.txt inX_7.txt inX_8.txt inX_10.txt inX_9.txt > inX_all.txt
t $B/ext_indep4 17 6 3 < inX_all.txt > hitsX.txt; tail -n1 hitsX.txt
t $B/filter_hits HIT < hitsX.txt > filtX.txt; tail -n1 filtX.txt; python3 -I connected_filter.py filtX.txt X_conn.txt
echo "== C5 final step (19,15,8)"
python3 -I combine.py inH19_a.txt AP AP filt_12_10_5.txt:SURVIVOR; python3 -I combine.py inH19_b.txt AP filt_15_11_6.txt:SURVIVOR
python3 -I combine.py inH19_c.txt filt_10_7_4.txt:SURVIVOR filt_8_5_3.txt:SURVIVOR; cat inH19_a.txt inH19_b.txt inH19_c.txt > inH19.txt
t $B/ext_indep4 18 7 3 < inH19.txt > hitsH19.txt; tail -n1 hitsH19.txt
t $B/filter_hits2 HIT notau < hitsH19.txt > filtH19.txt; tail -n1 filtH19.txt
echo "== C6 (20,13,8)"
python3 -I combine.py inH20.txt AP AP AP filt_10_7_4.txt:SURVIVOR; t $B/ext_indep4 19 7 3 < inH20.txt > hitsH20.txt; tail -n1 hitsH20.txt
$B/filter_hits HIT < hitsH20.txt | tail -n1
t $B/ext_vertex2 19 8 3 < inH20.txt > hitsH20_ev2.txt; tail -n1 hitsH20_ev2.txt; python3 -I compare_hits.py hitsH20_ev2.txt hitsH20.txt
echo "== C4 cross-check on the isolated-vertex type with ext_vertex2"
t $B/ext_vertex2 17 7 3 < inX_9.txt > hitsX9_ev2.txt; tail -n1 hitsX9_ev2.txt; $B/ext_indep4 17 6 3 < inX_9.txt > hitsX9_mine.txt; python3 -I compare_hits.py hitsX9_ev2.txt hitsX9_mine.txt
echo "== done"
