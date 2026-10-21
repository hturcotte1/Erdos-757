#!/bin/bash
# Referee L016 round 1: full one-level recomputation of cell(24,16,9,3) with my own program from the lower lists
# (seeds of L013/L014 and the run-A lists (23,13,8,3), (23,14,8,2), (22,14,8,2), (20,13,7,2), all re-verified independently).
R=/home/user/Erdos-757/experiments/referee/L016-round1; cd $R
F=$(python3 -c "print('a'*24)")
nice -n 10 timeout 3000 ./bin/myext 23 8 2 1 2 < out/in_24_16_9_d2.txt > out/my_24_16_9_d2.out
nice -n 10 timeout 5000 ./bin/myext 23 8 3 2 3 < out/in_24_16_9_d3.txt > out/my_24_16_9_d3.out
echo "d=2: $(tail -1 out/my_24_16_9_d2.out)"
echo "d=3: $(tail -1 out/my_24_16_9_d3.out)"
cat out/my_24_16_9_d2.out out/my_24_16_9_d3.out | grep '^X:' | python3 src/canon_lines.py 24 | ./bin/labelg -q -f$F 2>/dev/null | LC_ALL=C sort -u > out/mine_24_16_9.g6
grep '^FOUND' out/new/cells_new/runF/cell_24_16_9_D3.txt | python3 src/canon_lines.py 24 | ./bin/labelg -q -f$F 2>/dev/null | LC_ALL=C sort -u > out/prov_24_16_9.g6
echo "classes mine=$(wc -l < out/mine_24_16_9.g6) prover=$(wc -l < out/prov_24_16_9.g6) $(cmp -s out/mine_24_16_9.g6 out/prov_24_16_9.g6 && echo EQUAL || echo DIFFERENT)"
zcat /home/user/Erdos-757/experiments/20261017-2150-i11-n27/cell_24_16_9_D3.txt.gz | grep '^FOUND' | python3 src/canon_lines.py 24 | ./bin/labelg -q -f$F 2>/dev/null | LC_ALL=C sort -u | cmp -s - out/prov_24_16_9.g6 && echo "worker list EQUAL to prover list"
rm -f out/my_24_16_9_d3.out
