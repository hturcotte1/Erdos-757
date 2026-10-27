#!/bin/bash
# build: gcc -O2 -march=native -o i11 i11.c -lm ; gcc -O2 -march=native -o vext vext.c -lm ; gcc -O2 -march=native -o vext_mut vext_mut.c -lm
# self test:            ./i11 selftest
# pieces:               python3 pieces.py                       (-> pieces.json)
# random growth:        ./run_grow.sh ; ./run_grow2.sh           (-> out/grow_K*.txt)
# gluing:               python3 glue.py 11 700000 out/glue_main ; python3 glue_exh.py
# one-edge extension:   I11_DMAX=5 ./i11 extend < out/ext_in.txt
# beam (exact vext):    EXTRA=out/extra_pieces.txt MAXC=6 SMAX=3 MAXD=4 python3 beam5.py 5 600 40 12 d5i
# hub unions:           python3 hubunion.py 1 900 ; python3 hubunion2.py 2 700
# subset SA:            I11_CONN=1 python3 run_subsa.py 150000 1 conn
# realizable walks:     python3 real.py 5 600 out/real_main.json ; python3 realize_rand.py
# validation:           python3 validate_tau.py
# aggregate:            python3 classify_low.py ; python3 structure2.py ; python3 aggregate.py ; python3 make_report.py
