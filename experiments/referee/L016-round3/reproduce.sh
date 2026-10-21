#!/bin/bash
# Referee L016 round 3 -- every computation of the review (run from this directory; about 1.5 CPU-hours on one core; large files in out/, logs in logs/)
set -e; cd "$(dirname "$0")"; mkdir -p bin out logs out/reg
P=/home/user/Erdos-757/experiments/prover; CANON=$P/L012/bin/canon; G30=/home/user/Erdos-757/experiments/referee/L013-round3/bin/genbg30
gcc -O2 -Wall -o bin/refcheck src/refcheck.c; gcc -O2 -Wall -o bin/refext src/refext.c; gcc -O2 -Wall -o bin/g6filt src/g6filt.c
mkdir -p out/cells_L016 out/cells_L013 out/cells_L014; tar xzf $P/L016/cells_new.tar.gz -C out/cells_L016; tar xzf $P/L013/cells.tar.gz -C out/cells_L013; tar xzf $P/L014/cells.tar.gz -C out/cells_L014; cp $P/L014/cell_15_13_6_D3.txt.gz out/cells_L014/
# (the merge of the lists into out/cells_all with the common-key check is the inline Python of the session; see the review, check 5)
python3 src/arith.py > logs/arith.txt; python3 src/decomp.py > logs/decomp.txt; python3 src/c27.py > logs/c27.txt
python3 src/mkinputs.py 27 25 12 3 out/cells_all > out/in_27_25_12_3.txt; ./bin/refext 26 11 12 3 2 3 gosper all < out/in_27_25_12_3.txt > out/refext_27_25_12_3_all.txt
bash src/phase2.sh   # refcheck on all lists, all inputs, sparse final steps, closure tests, regression, own cell(26,22,11,3)  (stop it before the genbg counts)
bash src/phase3.sh   # genbg (27,13,10,2), six random chunks of (25,19,10,3)  (stopped after the chunks)
bash src/phase4.sh   # own full recomputation of cell(25,19,10,3)
bash src/phase5.sh   # sample of (24,16,9,3)
python3 src/closure.py 23 13 8 3 out/cells_L016/cells_new/runA/cell_23_13_8_D3.txt out/cells_all $CANON > logs/closure_23_13_8_3.txt
# (27,18,11,2) by cubic duals: geng -q -c -d3 -D3 18 > out/cubic18.g6, then the inline networkx matching script of the session
