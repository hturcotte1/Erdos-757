#!/bin/bash
# Referee L011: re-run of the prover's pipeline C1-C5, C7 (and C4) from COPIES of the prover's programs in out/rerun/.
# Nothing in the prover's folder is written.  Usage: rerun_prover.sh  (run from the referee folder)
set -e
R=/home/user/Erdos-757/experiments/referee/L011-round1; P=/home/user/Erdos-757/experiments/prover/L011
F=/home/user/Erdos-757/experiments/20261017-0825-n21-n22-via-i11
L8=/home/user/Erdos-757/experiments/prover/L008/indep; L9=/home/user/Erdos-757/experiments/prover/L009/indep
W=$R/out/rerun; mkdir -p $W/bin $W/out
cp $P/indep/{enum_conn,ext_indep5,filter_hits,filter_hits2}.c $W/bin/; cp $F/ext_vertex2.c $W/bin/
cp $P/{decomp22,combine,connected_filter,connected_filter2,connected_hits,hit_types,compare_hits,compare_found}.py $W/
cd $W/bin && gcc -O2 -Wall -o enum_conn enum_conn.c && gcc -O2 -Wall -o ext_indep5 ext_indep5.c && gcc -O2 -o filter_hits filter_hits.c && gcc -O2 -o filter_hits2 filter_hits2.c && gcc -O2 -o ext_vertex2 ext_vertex2.c
cd $W
t() { local s=$(date +%s); "$@"; echo "   [$(( $(date +%s) - s )) s]"; }
echo "== C1"; python3 decomp22.py > decomp22_output.txt; cmp decomp22_output.txt $P/decomp22_output.txt && echo "decomp22 output identical to prover's"
echo "== C2 small cells"
for c in "6 3 2" "8 5 3" "8 6 3" "9 4 3" "10 7 4" "10 8 4" "11 6 4" "11 7 4" "13 8 5" "13 9 5" "14 7 5" "14 8 5" "16 9 6" "17 8 6" "17 9 6" "19 10 7" "20 10 7" "16 10 6"; do
  set -- $c; ./bin/enum_conn $1 $2 $3 3 1 > out/cell_$1_$2_$3.txt; echo "$c: $(tail -n 1 out/cell_$1_$2_$3.txt)"; done
for c in "21 11 8" "21 12 8"; do set -- $c; echo "$c D2: $(./bin/enum_conn $1 $2 $3 2 0)"; done
echo "== C3 components in C"
zcat $L8/mine_12_10_5_deg3.txt.gz > out/cell_12_10_5.txt; zcat $L8/mine_15_11_6_deg3.txt.gz > out/cell_15_11_6.txt
cp $L9/T14_conn.txt out/T14_conn.txt; zcat $L9/T17_conn.txt.gz > out/T17_conn.txt
for c in 6_3_2 8_5_3 8_6_3 9_4_3 10_7_4 10_8_4 11_7_4 13_8_5 13_9_5 14_8_5 16_10_6 12_10_5 15_11_6; do ./bin/filter_hits FOUND < out/cell_$c.txt > out/filt_$c.txt; echo "$c: $(tail -n 1 out/filt_$c.txt | cut -c1-150)"; done
for x in T14 T17; do ./bin/filter_hits FOUND < out/${x}_conn.txt > out/filt_$x.txt; echo "$x: $(tail -n 1 out/filt_$x.txt | cut -c1-150)"; done
echo "== C4"
python3 combine.py out/in21_12.txt AP AP AP AP out/filt_8_5_3.txt:SURVIVOR
./bin/ext_indep5 20 7 3 < out/in21_12.txt > out/hits21_12.txt; tail -n 1 out/hits21_12.txt; ./bin/filter_hits HIT < out/hits21_12.txt | tail -n 1 | cut -c1-200
cmp out/hits21_12.txt $P/out/hits21_12.txt && echo "C4 hits byte-identical to prover's file"
echo "== C5 (X20)"
python3 combine.py out/inX20_1.txt AP AP AP out/filt_10_8_4.txt:SURVIVOR; python3 combine.py out/inX20_2.txt AP AP out/filt_13_9_5.txt:SURVIVOR
python3 combine.py out/inX20_3.txt AP out/filt_6_3_2.txt:SURVIVOR out/filt_10_7_4.txt:SURVIVOR; python3 combine.py out/inX20_4.txt AP out/filt_8_5_3.txt:SURVIVOR out/filt_8_5_3.txt:SURVIVOR
python3 combine.py out/inX20_5.txt AP out/filt_16_10_6.txt:SURVIVOR; python3 combine.py out/inX20_8.txt out/filt_9_4_3.txt:SURVIVOR out/filt_10_7_4.txt:SURVIVOR
cat out/inX20_1.txt out/inX20_2.txt out/inX20_3.txt out/inX20_4.txt out/inX20_5.txt out/inX20_8.txt > out/inX20_all.txt
t ./bin/ext_indep5 19 7 3 < out/inX20_all.txt > out/hitsX20.txt; tail -n 1 out/hitsX20.txt
echo "hitsX20 sha256 $(sha256sum < out/hitsX20.txt | cut -c1-64)"
t ./bin/filter_hits2 HIT notau < out/hitsX20.txt > out/filtX20.txt; tail -n 1 out/filtX20.txt | cut -c1-200
python3 connected_filter2.py out/filtX20.txt out/X20_conn.txt 20
python3 connected_hits.py out/hitsX20.txt out/hitsX20_conn.txt 20; ./bin/filter_hits2 HIT notau < out/hitsX20_conn.txt | tail -n 1 | cut -c1-200
echo "== C7 (X21)"
python3 combine.py out/inX21_1.txt ISO AP AP AP out/filt_10_7_4.txt:SURVIVOR; python3 combine.py out/inX21_5.txt AP AP AP AP out/filt_8_6_3.txt:SURVIVOR
python3 combine.py out/inX21_6.txt AP AP AP out/filt_11_7_4.txt:SURVIVOR; python3 combine.py out/inX21_7.txt AP AP out/filt_6_3_2.txt:SURVIVOR out/filt_8_5_3.txt:SURVIVOR
python3 combine.py out/inX21_8.txt AP AP out/filt_14_8_5.txt:SURVIVOR; python3 combine.py out/inX21_10.txt AP out/filt_8_5_3.txt:SURVIVOR out/filt_9_4_3.txt:SURVIVOR
cat out/inX21_1.txt out/inX21_5.txt out/inX21_6.txt out/inX21_7.txt out/inX21_8.txt out/inX21_10.txt > out/inX21_all.txt
t ./bin/ext_indep5 20 7 3 < out/inX21_all.txt > out/hitsX21.txt; tail -n 1 out/hitsX21.txt
echo "hitsX21 sha256 $(sha256sum < out/hitsX21.txt | cut -c1-64)"
t ./bin/filter_hits2 HIT notau < out/hitsX21.txt > out/filtX21.txt; tail -n 1 out/filtX21.txt | cut -c1-200
python3 connected_filter2.py out/filtX21.txt out/X21_conn.txt 21; python3 connected_hits.py out/hitsX21.txt out/hitsX21_conn.txt 21
echo "== inputs for C6, C8 (counts only here)"
python3 combine.py out/in21_17_a.txt AP AP out/filt_T14.txt:SURVIVOR; python3 combine.py out/in21_17_b.txt AP out/filt_T17.txt:SURVIVOR
python3 combine.py out/in21_17_c.txt out/filt_10_7_4.txt:SURVIVOR out/filt_10_7_4.txt:SURVIVOR
cat out/in21_17_a.txt out/in21_17_b.txt out/in21_17_c.txt > out/in21_17_all.txt
python3 combine.py out/in22_16_a.txt AP AP AP out/filt_12_10_5.txt:SURVIVOR; python3 combine.py out/in22_16_b.txt AP AP out/filt_15_11_6.txt:SURVIVOR
python3 combine.py out/in22_16_c.txt AP out/filt_8_5_3.txt:SURVIVOR out/filt_10_7_4.txt:SURVIVOR
cat out/in22_16_a.txt out/in22_16_b.txt out/in22_16_c.txt > out/in22_16_all.txt
for f in in21_17_all in22_16_all; do echo "$f: $(wc -l < out/$f.txt) lines; sha256 $(sha256sum < out/$f.txt | cut -c1-64); prover gz: $(zcat $P/out/$f.txt.gz | sha256sum | cut -c1-64)"; done
echo "RERUN DONE"
