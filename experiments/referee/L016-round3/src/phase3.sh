#!/bin/bash
cd /home/user/Erdos-757/experiments/referee/L016-round3; export LC_ALL=C
CANON=/home/user/Erdos-757/experiments/prover/L012/bin/canon; G30=/home/user/Erdos-757/experiments/referee/L013-round3/bin/genbg30
echo "START phase3 $(date -u +%H:%M:%S)"
# A. genbg + own filter for the hypertree cell (27,13,10,2)
{ echo "== cell (27,13,10,2): genbg30 -q -c -Z1 -d1:3 -D2:3 27 13 39:39 | g6filt 27 13 10"; nice -n 10 timeout 600 $G30 -q -c -Z1 -d1:3 -D2:3 27 13 39:39 | ./bin/g6filt 27 13 10; echo "rc=${PIPESTATUS[0]},${PIPESTATUS[1]}"; } > logs/genbg_27_13_10_2.txt 2>&1; cat logs/genbg_27_13_10_2.txt
# B. six random chunks of cell(25,19,10,3) with the own extension program
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
for c in 0 1 2 3 4 5; do nice -n 10 timeout 900 ./bin/refext 24 9 10 3 2 3 < out/chunk_$c.txt > out/refext_chunk_$c.txt; rc=$?; grep '^FOUND' out/refext_chunk_$c.txt | $CANON 25 | sort -u > out/chunk_${c}_classes.txt; echo "chunk $c rc=$rc $(tail -1 out/refext_chunk_$c.txt) | connected survivors $(grep -c '^FOUND' out/refext_chunk_$c.txt) classes $(wc -l < out/chunk_${c}_classes.txt) not-in-prover-list $(comm -23 out/chunk_${c}_classes.txt out/prover_25_19_10_3_classes.txt | wc -l) $(date -u +%H:%M:%S)"; done > logs/chunks.txt 2>&1
echo "chunks done $(date -u +%H:%M:%S)"; cat logs/chunks.txt
# C. genbg for the other sparse cells, best effort with caps
for c in "27 18 11 2 600" "27 14 10 3 600" "27 19 11 3 600"; do set -- $c; { echo "== cell ($1,$2,$3,$4): genbg30 -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) | g6filt $1 $2 $3 (timeout $5 s)"; nice -n 10 timeout $5 $G30 -q -c -Z1 -d1:3 -D$4:3 $1 $2 $((3*$2)):$((3*$2)) | ./bin/g6filt $1 $2 $3; echo "rc=${PIPESTATUS[0]},${PIPESTATUS[1]} (124 = timeout: INCOMPLETE)"; } > logs/genbg_$1_$2_$3_$4.txt 2>&1; cat logs/genbg_$1_$2_$3_$4.txt; done
echo "ALL DONE phase3 $(date -u +%H:%M:%S)"
