#!/bin/bash
# Referee round 2 (L008): validate "delete a degree-3 vertex, enumerate the rest, extend" against direct enumeration on small
# analogues.  Direct: all linear 3-graphs on [N] with M edges, tau >= T, Delta <= 3 (bfs_enum CONN=0), keep those with a
# vertex of degree 3.  Extension: all linear (N-1, M-3, tau >= T-1, Delta <= 3) graphs (CONN=0), extended by ext_r2 (and by
# the prover's ext_indep2 where it applies).  The two sets of isomorphism classes must coincide.
cd /home/user/Erdos-757/experiments/referee/L008-round2
for c in "12 10 5" "12 9 4" "13 10 5" "11 8 4" "13 11 5"; do
  set -- $c; N=$1; M=$2; T=$3; G=$((N-1)); MG=$((M-3)); TG=$((T-1))
  ./bin/bfs_enum $N $M $T 3 0 1 2>/dev/null | grep FOUND | sed 's/ AUT=.*$//' > out/val_direct_$N_$M_$T.txt
  python3 - out/val_direct_$N_$M_$T.txt > out/val_direct_deg3.txt << 'PY'
import re, sys
for l in open(sys.argv[1]):
    es = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
    deg = {}
    for e in es:
        for v in e: deg[v] = deg.get(v, 0) + 1
    if 3 in deg.values(): print(l.strip())
PY
  ./bin/canon_list FOUND $N < out/val_direct_deg3.txt | awk '{print $1}' | sort -u > out/val_k1.txt
  ./bin/bfs_enum $G $MG $TG 3 0 1 2>/dev/null | grep FOUND | sed 's/ AUT=.*$//' > out/val_G.txt
  ./bin/ext_r2 EXT $G $T 3 < out/val_G.txt | grep HIT | sed 's/ |.*$//' | ./bin/canon_list HIT $N | awk '{print $1}' | sort -u > out/val_k2.txt
  echo "N=$N M=$M T=$T: direct classes with a deg-3 vertex: $(wc -l < out/val_k1.txt); G classes: $(wc -l < out/val_G.txt); extension hit classes: $(wc -l < out/val_k2.txt); identical: $(cmp -s out/val_k1.txt out/val_k2.txt && echo YES || echo NO)"
done
