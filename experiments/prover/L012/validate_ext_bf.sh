#!/bin/bash
# (L012) brute-force validation of ext_d (d = 2, 3, 4; constrained and free modes; inputs with an isolated vertex) against bf_ext.py
cd /home/user/Erdos-757/experiments/prover/L012
L11=../L011/out; ENUM=./bin/enum_conn
toedges() { python3 -c "
import sys,re
for l in sys.stdin:
    es=re.findall(r'\((\d+),(\d+),(\d+)\)',l); print(len(es),' '.join(' '.join(e) for e in es))"; }
grep '^SURVIVOR' $L11/filt_8_5_3.txt | head -40 | toedges > out/v_8_5_3.txt
grep '^SURVIVOR' $L11/filt_10_7_4.txt | head -30 | toedges > out/v_10_7_4.txt
python3 combine.py out/v_ap853.txt AP $L11/filt_8_5_3.txt:SURVIVOR > /dev/null
python3 combine.py out/v_apap853.txt AP AP $L11/filt_8_5_3.txt:SURVIVOR > /dev/null; head -5 out/v_apap853.txt > out/v_apap853_s5.txt
python3 combine.py out/v_iso1074.txt ISO $L11/filt_10_7_4.txt:SURVIVOR > /dev/null; head -40 out/v_iso1074.txt > out/v_iso1074s.txt
for c in "10 5 3" "11 5 3"; do set -- $c; $ENUM $1 $2 $3 2 1 | grep FOUND | toedges > out/v_d2_$1_$2_$3.txt; done
for spec in "v_8_5_3 8 3 4 4 3" "v_8_5_3 8 3 4 2 1" "v_8_5_3 8 3 3 4 2" "v_10_7_4 10 4 5 4 3" "v_10_7_4 10 4 4 2 2" "v_8_5_3 8 3 3 2 2" \
            "v_ap853 11 4 5 4 3" "v_ap853 11 4 5 3 2" "v_apap853_s5 14 5 6 4 3" "v_iso1074s 11 4 5 4 3" "v_iso1074s 11 4 5 3 2" \
            "v_d2_10_5_3 10 3 4 2 1" "v_d2_11_5_3 11 3 4 2 1" "v_d2_10_5_3 10 3 4 2 2" "v_d2_11_5_3 11 3 4 3 2"; do
  set -- $spec; ./bin/ext_d $2 $3 $4 $5 $6 noprune < out/$1.txt > out/t_bfA.txt; python3 bf_ext.py $2 $4 $5 $6 < out/$1.txt > out/t_bfB.txt
  echo "$spec: ext_d $(tail -n1 out/t_bfA.txt | grep -o 'hits_all=[0-9]*') bf $(tail -n1 out/t_bfB.txt) | $(python3 compare_hits.py out/t_bfA.txt out/t_bfB.txt | grep -o 'identical sets: [A-Za-z]*')"
done
