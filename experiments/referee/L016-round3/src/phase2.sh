#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L016-round3; export LC_ALL=C
CANON=/home/user/Erdos-757/experiments/prover/L012/bin/canon; G30=/home/user/Erdos-757/experiments/referee/L013-round3/bin/genbg30
echo "START $(date -u +%H:%M:%S)"
# 1. own filters on all 51 new lists
for f in out/cells_L016/cells_new/runF/*.txt out/cells_L016/cells_new/runB2/*.txt out/cells_L016/cells_new/runA/*.txt; do b=$(basename $f .txt); set -- $(echo $b | sed 's/cell_//; s/_D/ /; s/_/ /g'); echo -n "$(dirname $f | xargs basename) "; nice -n 10 timeout 1200 ./bin/refcheck $1 $2 $3 $4 < $f; done > logs/refcheck_all.txt 2>&1
echo "refcheck done $(date -u +%H:%M:%S): $(grep -c ALL-OK logs/refcheck_all.txt) ALL-OK, $(grep -c FAILURES logs/refcheck_all.txt) FAILURES"
# 2. own inputs
python3 src/mkinputs.py 26 22 11 3 out/cells_all > out/in_26_22_11_3.txt 2> out/in_26_22_11_3.log
python3 src/mkinputs.py 25 19 10 3 out/cells_all > out/in_25_19_10_3.txt 2> out/in_25_19_10_3.log
python3 src/mkinputs.py 24 16 9 3 out/cells_all 3 8 > out/in_24_16_9_3_d3.txt 2> out/in_24_16_9_3_d3.log; python3 src/mkinputs.py 24 16 9 3 out/cells_all 2 8 > out/in_24_16_9_3_d2.txt 2> out/in_24_16_9_3_d2.log
python3 src/mkinputs.py 23 21 10 3 out/cells_all > out/in_23_21_10_3.txt 2> out/in_23_21_10_3.log
python3 src/mkinputs.py 27 19 11 3 out/cells_all > out/in_27_19_11_3.txt 2> out/in_27_19_11_3.log; python3 src/mkinputs.py 27 18 11 2 out/cells_all > out/in_27_18_11_2.txt 2> out/in_27_18_11_2.log
python3 src/mkinputs.py 27 14 10 3 out/cells_all 2 9 > out/in_27_14_10_3_d2.txt 2> out/in_27_14_10_3_d2.log; python3 src/mkinputs.py 27 14 10 3 out/cells_all 3 9 > out/in_27_14_10_3_d3.txt 2> out/in_27_14_10_3_d3.log
python3 src/mkinputs.py 27 13 10 2 out/cells_all > out/in_27_13_10_2.txt 2> out/in_27_13_10_2.log
python3 src/mkinputs.py 26 16 10 3 out/cells_all 2 9 > out/in_26_16_10_3_d2.txt 2> out/in_26_16_10_3_d2.log; python3 src/mkinputs.py 26 16 10 3 out/cells_all 3 9 > out/in_26_16_10_3_d3.txt 2> out/in_26_16_10_3_d3.log
for f in out/in_*.log; do echo "$f: $(tail -1 $f)"; done > logs/inputs.txt; echo "inputs done $(date -u +%H:%M:%S)"
# 3. sparse top cells' final steps with own program (all extensions with the required tau, connectivity reported)
{ echo "(27,13,10,2) d=2:"; ./bin/refext 26 9 10 2 1 2 gosper all < out/in_27_13_10_2.txt | tail -3
  echo "(27,14,10,3) d=2:"; ./bin/refext 26 9 10 2 2 3 gosper all < out/in_27_14_10_3_d2.txt | tail -3
  echo "(27,14,10,3) d=3:"; ./bin/refext 26 9 10 3 2 3 gosper all < out/in_27_14_10_3_d3.txt > out/refext_27_14_d3_all.txt; tail -1 out/refext_27_14_d3_all.txt; echo "extensions tau>=10: $(grep -c '^ALL' out/refext_27_14_d3_all.txt) connected: $(grep '^ALL' out/refext_27_14_d3_all.txt | grep -c 'conn=1')"
  echo "(27,18,11,2) d=2: inputs $(wc -l < out/in_27_18_11_2.txt)"
  echo "(27,19,11,3) d=3:"; ./bin/refext 26 10 11 3 2 3 gosper all < out/in_27_19_11_3.txt > out/refext_27_19_all.txt; tail -1 out/refext_27_19_all.txt; echo "extensions tau>=11: $(grep -c '^ALL' out/refext_27_19_all.txt) connected: $(grep '^ALL' out/refext_27_19_all.txt | grep -c 'conn=1')"; } > logs/sparse_final.txt 2>&1
echo "sparse final steps done $(date -u +%H:%M:%S)"
# 4. closure
nice -n 10 timeout 1200 python3 src/closure.py 26 22 11 3 out/cells_L016/cells_new/runF/cell_26_22_11_D3.txt out/cells_all $CANON > logs/closure_26_22_11_3.txt 2>&1; tail -1 logs/closure_26_22_11_3.txt
nice -n 10 timeout 2400 python3 src/closure.py 25 19 10 3 out/cells_L016/cells_new/runF/cell_25_19_10_D3.txt out/cells_all $CANON > logs/closure_25_19_10_3.txt 2>&1; tail -1 logs/closure_25_19_10_3.txt
echo "closure done $(date -u +%H:%M:%S)"
# 5. regression
bash src/regress.sh > logs/regress.txt 2>&1; echo "regress done $(date -u +%H:%M:%S)"
# 6. own full recomputation of cell(26,22,11,3)
nice -n 10 timeout 2400 ./bin/refext 25 10 11 3 2 3 < out/in_26_22_11_3.txt > out/refext_26_22_11_3.txt; echo "rc=$?" > logs/own_26_22_11_3.txt; tail -1 out/refext_26_22_11_3.txt >> logs/own_26_22_11_3.txt
grep '^FOUND' out/refext_26_22_11_3.txt | $CANON 26 | sort -u > out/own_26_22_11_3_classes.txt; grep '^FOUND' out/cells_L016/cells_new/runF/cell_26_22_11_D3.txt | $CANON 26 | sort -u > out/prover_26_22_11_3_classes.txt
echo "own connected survivors: $(grep -c '^FOUND' out/refext_26_22_11_3.txt); own classes: $(wc -l < out/own_26_22_11_3_classes.txt); prover classes: $(wc -l < out/prover_26_22_11_3_classes.txt); identical sets: $(cmp -s out/own_26_22_11_3_classes.txt out/prover_26_22_11_3_classes.txt && echo YES || echo NO)" >> logs/own_26_22_11_3.txt
cat logs/own_26_22_11_3.txt; echo "own (26,22,11,3) done $(date -u +%H:%M:%S)"
# 7. genbg sparse cells (count first, then filter)
for c in "27 13 10 2" "27 18 11 2" "27 14 10 3" "27 19 11 3"; do set -- $c; echo "== cell ($1,$2,$3,$4) genbg30 -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2))"; ( nice -n 10 timeout 900 $G30 -u -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) ) 2>&1 | tail -2; echo "count rc=$?"; done > logs/genbg_counts.txt 2>&1; echo "genbg counts done $(date -u +%H:%M:%S)"
for c in "27 13 10 2" "27 18 11 2" "27 14 10 3" "27 19 11 3"; do set -- $c; echo "== cell ($1,$2,$3,$4)"; nice -n 10 timeout 1500 $G30 -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) | ./bin/g6filt $1 $2 $3; echo "pipeline rc=${PIPESTATUS[0]},${PIPESTATUS[1]}"; done > logs/genbg_filter.txt 2>&1; echo "genbg filter done $(date -u +%H:%M:%S)"
# 8. six random chunks of cell(25,19,10,3) with own program
python3 - <<'PY'
import random
lines = open('out/in_25_19_10_3.txt').read().split('\n'); lines = [l for l in lines if l.strip()]
rnd = random.Random(757); idx = list(range(len(lines))); rnd.shuffle(idx)
for c in range(6):
    with open('out/chunk_%d.txt' % c, 'w') as f:
        for i in sorted(idx[c*25000:(c+1)*25000]): f.write(lines[i] + '\n')
print('inputs', len(lines))
PY
grep '^FOUND' out/cells_L016/cells_new/runF/cell_25_19_10_D3.txt | $CANON 25 | sort -u > out/prover_25_19_10_3_classes.txt
for c in 0 1 2 3 4 5; do nice -n 10 timeout 1500 ./bin/refext 24 9 10 3 2 3 < out/chunk_$c.txt > out/refext_chunk_$c.txt; rc=$?; grep '^FOUND' out/refext_chunk_$c.txt | $CANON 25 | sort -u > out/chunk_${c}_classes.txt; echo "chunk $c rc=$rc $(tail -1 out/refext_chunk_$c.txt) | classes $(wc -l < out/chunk_${c}_classes.txt) not-in-prover-list $(comm -23 out/chunk_${c}_classes.txt out/prover_25_19_10_3_classes.txt | wc -l)"; done > logs/chunks.txt 2>&1
echo "chunks done $(date -u +%H:%M:%S)"; echo "ALL DONE $(date -u +%H:%M:%S)"
