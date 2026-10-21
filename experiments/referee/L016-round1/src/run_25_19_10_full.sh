#!/bin/bash
# Referee L016 round 1: full one-level recomputation of cell(25,19,10,3) with my own program from the lower lists
# (my decompositions; lists: seeds of L013/L014, the prover's cell(24,16,9,3) (re-derived by me, run_24_16_9.sh)).
R=/home/user/Erdos-757/experiments/referee/L016-round1; cd $R
F=$(python3 -c "print('a'*25)")
nice -n 10 timeout 1200 python3 src/build_inputs.py 24 16 9 3 out/in_25_19_10_full.txt 2> out/build_25_19_10_full.log
tail -1 out/build_25_19_10_full.log
nice -n 10 timeout 6000 ./bin/myext 24 9 3 2 3 < out/in_25_19_10_full.txt | grep -E '^X:|^MYSUMMARY' > out/my_25_19_10_full.out
echo "d=3: $(tail -1 out/my_25_19_10_full.out)"
grep '^X:' out/my_25_19_10_full.out | python3 src/canon_lines.py 25 | ./bin/labelg -q -f$F 2>/dev/null | LC_ALL=C sort -u > out/mine_25_19_10.g6
echo "classes mine=$(wc -l < out/mine_25_19_10.g6) prover=$(wc -l < out/prov_25_19_10.g6) $(cmp -s out/mine_25_19_10.g6 out/prov_25_19_10.g6 && echo EQUAL || echo DIFFERENT)"
zcat /home/user/Erdos-757/experiments/20261017-2150-i11-n27/cell_25_19_10_D3.txt.gz | grep '^FOUND' | python3 src/canon_lines.py 25 | ./bin/labelg -q -f$F 2>/dev/null | LC_ALL=C sort -u | cmp -s - out/prov_25_19_10.g6 && echo "worker list EQUAL to prover list"
rm -f out/in_25_19_10_full.txt out/my_25_19_10_full.out
