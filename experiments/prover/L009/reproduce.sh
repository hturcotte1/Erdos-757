#!/bin/bash
# Reproduction of every computation cited in results/proofs/L009-f18-equals-11.md (run from this directory).
# F = falsifier folder (its C sources are recompiled here for cross-checks).  L007/L008 computations: their own reproduce.sh.
set -e
F=/home/user/Erdos-757/experiments/20261017-0615-n17-n18-via-i11
mkdir -p bin rerun
cd indep; gcc -O2 -Wall -o enum_conn enum_conn.c; gcc -O2 -Wall -o enum_conn_slice enum_conn_slice.c; gcc -O2 -Wall -o ext_indep2 ext_indep2.c
gcc -O2 -Wall -o ext_indep3 ext_indep3.c; gcc -O2 -o filter_hits filter_hits.c; cd ..
gcc -O2 -o bin/ext_vertex2 $F/ext_vertex2.c
# --- C1: cells and decompositions
python3 decomp18.py > decomp18_output.txt
# --- C2: enumerations (components, window cells), prover's enum_conn
(cd indep && ./run_small_cells.sh > run_small_cells.log)
for c in 6_3_2 8_5_3 10_7_4 10_8_4 13_9_5; do python3 compare_found.py indep/cell_$c.txt -- $F/K_$c.txt | tail -n 1; done
python3 compare_found.py indep/cell_16_10_6.txt -- $F/K_16_10_6.txt.gz | tail -n 1
# --- C3: n = 17
python3 combine.py rerun/in17_C10_2AP.txt indep/cell_10_7_4.txt AP AP; ./indep/ext_indep2 16 6 3 < rerun/in17_C10_2AP.txt > indep/hits17_C10_2AP.txt
./indep/filter_hits HIT < indep/hits17_C10_2AP.txt | tail -n 1
python3 combine.py rerun/in17_C10all_2AP.txt ../L007/indep/mine_10_7_4.txt AP AP; ./indep/ext_indep2 16 6 3 < rerun/in17_C10all_2AP.txt > indep/hits17_C10all_2AP.txt
./indep/filter_hits HIT < indep/hits17_C10all_2AP.txt | tail -n 1
python3 combine.py rerun/in17_C13_AP.txt indep/cell_13_8_5.txt AP; ./indep/ext_indep2 16 6 3 < rerun/in17_C13_AP.txt > indep/hits17_C13_AP.txt
./indep/filter_hits HIT < indep/hits17_C13_AP.txt | tail -n 1; ./indep/filter_hits FOUND < indep/cell_13_8_5.txt | tail -n 1
./indep/ext_indep2 16 6 3 < $F/G_C10_2AP.txt | tail -n 1
# --- C4: components restricted to the class C
for c in 6_3_2 8_5_3 10_7_4 10_8_4 13_9_5 16_10_6; do ./indep/filter_hits FOUND < indep/cell_$c.txt > rerun/filt_$c.txt; tail -n 1 rerun/filt_$c.txt; done
# --- C5: rebuild of the connected (14,12,6) graphs
python3 combine.py rerun/inT14_a.txt AP rerun/filt_10_8_4.txt:SURVIVOR; python3 combine.py rerun/inT14_b.txt rerun/filt_13_9_5.txt:SURVIVOR
cat rerun/inT14_a.txt rerun/inT14_b.txt > rerun/inT14.txt
./indep/ext_indep2 13 5 3 < rerun/inT14.txt > indep/hitsT14.txt; ./indep/filter_hits HIT < indep/hitsT14.txt > rerun/filtT14.txt; tail -n 1 rerun/filtT14.txt
python3 connected_filter.py rerun/filtT14.txt indep/T14_conn.txt; python3 classes_of.py indep/T14_conn.txt FOUND rerun/T14_classes.txt
python3 iso_match.py rerun/T14_classes.txt $F/C14_classes.json; python3 iso_match.py $F/C14_classes.json rerun/T14_classes.txt
python3 -c "
import gzip,json,collections
out=[]
for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz','rt'):
    es=[tuple(e) for e in json.loads(l)['edges']]; d=collections.Counter(v for e in es for v in e)
    if max(d.values())<=3: out.append(es)
open('rerun/census_maxdeg3.txt','w').write(''.join('FOUND: '+' '.join('(%d,%d,%d)'%e for e in es)+'\n' for es in out))"
python3 iso_match.py rerun/T14_classes.txt rerun/census_maxdeg3.txt
# --- C6: rebuild of the connected (17,13,7) graphs
python3 combine.py rerun/inT17_1.txt AP AP rerun/filt_10_8_4.txt:SURVIVOR; python3 combine.py rerun/inT17_2.txt AP rerun/filt_13_9_5.txt:SURVIVOR
python3 combine.py rerun/inT17_3.txt rerun/filt_10_7_4.txt:SURVIVOR rerun/filt_6_3_2.txt:SURVIVOR
python3 combine.py rerun/inT17_4.txt rerun/filt_8_5_3.txt:SURVIVOR rerun/filt_8_5_3.txt:SURVIVOR; python3 combine.py rerun/inT17_5.txt rerun/filt_16_10_6.txt:SURVIVOR
cat rerun/inT17_[1-5].txt > rerun/inT17.txt
./indep/ext_indep2 16 6 3 < rerun/inT17.txt > indep/hitsT17.txt; ./indep/filter_hits HIT < indep/hitsT17.txt > rerun/filtT17.txt; tail -n 1 rerun/filtT17.txt
python3 connected_filter.py rerun/filtT17.txt indep/T17_conn.txt; python3 classes_of.py indep/T17_conn.txt FOUND rerun/T17_classes.txt   # about 7 min
python3 iso_match.py rerun/T17_classes.txt $F/G17_classes.json; python3 iso_match.py $F/G17_classes.json rerun/T17_classes.txt
# --- C7: final extension step for (18,16,8)
python3 combine.py rerun/inH18_T17.txt indep/T17_conn.txt; python3 combine.py rerun/inH18_T14AP.txt indep/T14_conn.txt AP
cat rerun/inH18_T17.txt rerun/inH18_T14AP.txt > rerun/inH18.txt
./indep/ext_indep3 17 7 3 < rerun/inH18.txt > indep/hitsH18.txt; tail -n 1 indep/hitsH18.txt
./bin/ext_vertex2 17 8 3 < rerun/inH18.txt > rerun/hitsH18_full_ext_vertex2.txt; tail -n 1 rerun/hitsH18_full_ext_vertex2.txt     # about 1 h
python3 control18.py; ./indep/filter_hits HIT < control18_hits.txt | tail -n 1
# --- C8: heuristic validations (random slices of direct searches; partial direct (14,12,6) run)
python3 slice_sample.py 17 13 7 21698 6 1500 7 rerun/slices6_17_13_7.txt
./indep/filter_hits FOUND < rerun/slices6_17_13_7.txt > rerun/slices6_filt.txt; python3 connected_filter.py rerun/slices6_filt.txt rerun/slices6_C.txt
python3 iso_match.py rerun/T17_classes.txt rerun/slices6_C.txt
# --- C9: witness for f(18) <= 11
python3 witness_18.py
