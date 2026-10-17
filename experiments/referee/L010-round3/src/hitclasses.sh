#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L010-round3; P=/home/user/Erdos-757/experiments/prover/L010/out
# C6 hits: my 72 rep hits vs the prover's 6,624 labelled hits (classes)
grep ^HIT out/rephits_H20_C.txt | ./bin/canon 20 | sort -u > out/cls_rephits_H20.txt; grep ^HIT $P/hitsH20.txt | ./bin/canon 20 | sort -u > out/cls_proverhits_H20.txt
echo "C6 hit classes: mine $(wc -l < out/cls_rephits_H20.txt), prover $(wc -l < out/cls_proverhits_H20.txt): $(cmp -s out/cls_rephits_H20.txt out/cls_proverhits_H20.txt && echo IDENTICAL || echo DIFFERENT)"
# C4 hits: my 4,628 rep hits vs the prover's 797,231 labelled hits (classes); survivors (in C) vs the C5 input classes
grep ^HIT out/rephits_X_C.txt | ./bin/canon 18 | sort -u > out/cls_rephits_X.txt; zcat $P/hitsX.txt.gz | grep ^HIT | ./bin/canon 18 | sort -u > out/cls_proverhits_X.txt
echo "C4 hit classes: mine $(wc -l < out/cls_rephits_X.txt), prover $(wc -l < out/cls_proverhits_X.txt): $(cmp -s out/cls_rephits_X.txt out/cls_proverhits_X.txt && echo IDENTICAL || echo DIFFERENT)"
grep ^SURVIVOR out/repfilt_X_C.txt | sed 's/.*| //' | ./bin/canon 18 | sort -u > out/cls_repsurv_X.txt
echo "C4 survivors (in C, all disconnected): $(wc -l < out/cls_repsurv_X.txt) classes; equal to the C5 input classes (176)? $(cmp -s out/cls_repsurv_X.txt out/cls_rep_H19.txt && echo YES || echo NO)"
grep "^REJECT.*conn=1" out/repfilt_X_C.txt | sed 's/.*| //' | ./bin/canon 18 | sort -u > out/cls_repconn_X.txt
grep ^FOUND out/g_18_12_7_d3.txt | ./bin/canon 18 | sort -u > out/cls_direct_18_12_7.txt
echo "C4 connected hits: $(wc -l < out/cls_repconn_X.txt) classes; direct genbg connected (18,12,>=7) Delta<=3: $(wc -l < out/cls_direct_18_12_7.txt) classes; rebuild-connected == direct? $(cmp -s out/cls_repconn_X.txt out/cls_direct_18_12_7.txt && echo YES || echo NO)"
# C4 connected hits from ALL component classes (not only in C)
grep "^REJECT.*conn=1" out/repfilt_X_all.txt | sed 's/.*| //' | ./bin/canon 18 | sort -u > out/cls_repconn_X_all.txt
echo "C4(all) connected hits: $(wc -l < out/cls_repconn_X_all.txt) classes; == direct? $(cmp -s out/cls_repconn_X_all.txt out/cls_direct_18_12_7.txt && echo YES || echo NO)"
echo HITCLASSESDONE
