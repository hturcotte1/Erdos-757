#!/bin/bash
# Referee L009 round 3: from-scratch re-run of the prover's load-bearing pipeline C1-C7 (sources copied to prover_copy/),
# outputs under prover_copy/{indep,rerun}; SHA-256 compared with the prover's checksums_large_outputs.txt.
set -e
cd /home/user/Erdos-757/experiments/referee/L009-round3/prover_copy
F=/home/user/Erdos-757/experiments/20261017-0615-n17-n18-via-i11
L7=/home/user/Erdos-757/experiments/prover/L007
mkdir -p bin rerun
(cd indep && gcc -O2 -o enum_conn enum_conn.c && gcc -O2 -o ext_indep2 ext_indep2.c && gcc -O2 -o ext_indep3 ext_indep3.c && gcc -O2 -o filter_hits filter_hits.c)
echo "== C1"; python3 decomp18.py > decomp18_output.txt; diff decomp18_output.txt /home/user/Erdos-757/experiments/prover/L009/decomp18_output.txt && echo "decomp18 output identical"
echo "== C2"
cd indep
run() { s=$(date +%s); ./enum_conn "$@" > "$OUT"; e=$(date +%s); echo "enum_conn $* -> $(tail -n 1 $OUT) [$((e-s)) s]"; }
OUT=cell_6_3_2.txt;   run 6 3 2 3 1
OUT=cell_8_5_3.txt;   run 8 5 3 3 1
OUT=cell_10_7_4.txt;  run 10 7 4 3 1
OUT=cell_10_8_4.txt;  run 10 8 4 3 1
OUT=cell_13_8_5.txt;  run 13 8 5 3 1
OUT=cell_13_9_5.txt;  run 13 9 5 3 1
OUT=cell_16_9_6_deg3.txt;  run 16 9 6 3 0
OUT=cell_16_9_6_anydeg.txt; run 16 9 6 1000 0
OUT=cell_18_10_7_anydeg.txt; run 18 10 7 1000 0
OUT=cell_16_10_6.txt; run 16 10 6 3 1
OUT=cell_18_11_7_deg3.txt; run 18 11 7 3 0
cd ..
for c in 6_3_2 8_5_3 10_7_4 10_8_4 13_9_5; do python3 compare_found.py indep/cell_$c.txt -- $F/K_$c.txt | tail -n 1; done
python3 compare_found.py indep/cell_16_10_6.txt -- $F/K_16_10_6.txt.gz | tail -n 1
echo "== C3"
python3 combine.py rerun/in17_C10_2AP.txt indep/cell_10_7_4.txt AP AP; ./indep/ext_indep2 16 6 3 < rerun/in17_C10_2AP.txt > indep/hits17_C10_2AP.txt
./indep/filter_hits HIT < indep/hits17_C10_2AP.txt | tail -n 1
python3 combine.py rerun/in17_C10all_2AP.txt $L7/indep/mine_10_7_4.txt AP AP; ./indep/ext_indep2 16 6 3 < rerun/in17_C10all_2AP.txt > indep/hits17_C10all_2AP.txt
./indep/filter_hits HIT < indep/hits17_C10all_2AP.txt | tail -n 1
python3 combine.py rerun/in17_C13_AP.txt indep/cell_13_8_5.txt AP; ./indep/ext_indep2 16 6 3 < rerun/in17_C13_AP.txt > indep/hits17_C13_AP.txt
./indep/filter_hits HIT < indep/hits17_C13_AP.txt | tail -n 1; ./indep/filter_hits FOUND < indep/cell_13_8_5.txt | tail -n 1
./indep/ext_indep2 16 6 3 < $F/G_C10_2AP.txt | tail -n 1
echo "== C4"
for c in 6_3_2 8_5_3 10_7_4 10_8_4 13_9_5 16_10_6; do ./indep/filter_hits FOUND < indep/cell_$c.txt > rerun/filt_$c.txt; tail -n 1 rerun/filt_$c.txt; done
echo "== C5"
python3 combine.py rerun/inT14_a.txt AP rerun/filt_10_8_4.txt:SURVIVOR; python3 combine.py rerun/inT14_b.txt rerun/filt_13_9_5.txt:SURVIVOR
cat rerun/inT14_a.txt rerun/inT14_b.txt > rerun/inT14.txt
./indep/ext_indep2 13 5 3 < rerun/inT14.txt > indep/hitsT14.txt; tail -n 1 indep/hitsT14.txt; ./indep/filter_hits HIT < indep/hitsT14.txt > rerun/filtT14.txt; tail -n 1 rerun/filtT14.txt
python3 connected_filter.py rerun/filtT14.txt indep/T14_conn.txt
echo "== C6"
python3 combine.py rerun/inT17_1.txt AP AP rerun/filt_10_8_4.txt:SURVIVOR; python3 combine.py rerun/inT17_2.txt AP rerun/filt_13_9_5.txt:SURVIVOR
python3 combine.py rerun/inT17_3.txt rerun/filt_10_7_4.txt:SURVIVOR rerun/filt_6_3_2.txt:SURVIVOR
python3 combine.py rerun/inT17_4.txt rerun/filt_8_5_3.txt:SURVIVOR rerun/filt_8_5_3.txt:SURVIVOR; python3 combine.py rerun/inT17_5.txt rerun/filt_16_10_6.txt:SURVIVOR
cat rerun/inT17_[1-5].txt > rerun/inT17.txt
./indep/ext_indep2 16 6 3 < rerun/inT17.txt > indep/hitsT17.txt; tail -n 1 indep/hitsT17.txt; ./indep/filter_hits HIT < indep/hitsT17.txt > rerun/filtT17.txt; tail -n 1 rerun/filtT17.txt
python3 connected_filter.py rerun/filtT17.txt indep/T17_conn.txt
echo "== C7"
python3 combine.py rerun/inH18_T17.txt indep/T17_conn.txt; python3 combine.py rerun/inH18_T14AP.txt indep/T14_conn.txt AP
cat rerun/inH18_T17.txt rerun/inH18_T14AP.txt > rerun/inH18.txt
./indep/ext_indep3 17 7 3 < rerun/inH18.txt > indep/hitsH18.txt; tail -n 1 indep/hitsH18.txt
python3 control18.py; ./indep/filter_hits HIT < control18_hits.txt | tail -n 1
echo "== checksums"
sha256sum ./indep/T14_conn.txt ./indep/T17_conn.txt ./indep/cell_10_8_4.txt ./indep/cell_13_9_5.txt ./indep/cell_16_10_6.txt ./indep/hits17_C10_2AP.txt ./indep/hits17_C10all_2AP.txt ./indep/hitsT14.txt ./indep/hitsT17.txt ./rerun/filtT14.txt ./rerun/filtT17.txt ./rerun/filt_10_8_4.txt ./rerun/filt_13_9_5.txt ./rerun/filt_16_10_6.txt ./rerun/inH18.txt ./rerun/inH18_T14AP.txt ./rerun/inH18_T17.txt ./rerun/inT14.txt ./rerun/inT14_a.txt ./rerun/inT14_b.txt ./rerun/inT17.txt ./rerun/inT17_1.txt ./rerun/inT17_2.txt ./rerun/inT17_4.txt > my_checksums.txt
python3 - <<'PY'
ref = {l.split()[1]: l.split()[0] for l in open('checksums_large_outputs.txt') if l.strip()}
mine = {l.split()[1]: l.split()[0] for l in open('my_checksums.txt') if l.strip()}
ok = bad = 0
for k, v in mine.items():
    if k in ref:
        if ref[k] == v: ok += 1
        else: bad += 1; print('MISMATCH', k)
    else: print('not in prover list', k)
print('checksum matches:', ok, 'mismatches:', bad)
PY
echo "== done"
