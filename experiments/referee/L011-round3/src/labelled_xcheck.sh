#!/bin/bash
# Referee round 3: ext3 vs the prover's ext_indep5 (copy) on random labelled inputs from the prover's input files; hit sets compared
# as sets of sorted edge lists.  Usage: labelled_xcheck.sh NAME NG TG FILE(.gz ok) NSAMPLE SEED
cd /home/user/Erdos-757/experiments/referee/L011-round3
name=$1; NG=$2; TG=$3; f=$4; ns=$5; seed=$6
case "$f" in *.gz) zcat $f;; *) cat $f;; esac | shuf -n $ns --random-source=<(yes $seed) > out/xs_$name.txt
nice -n 5 ./bin/ext3 $NG $TG 3 1 < out/xs_$name.txt > out/xs_${name}_mine.txt
nice -n 5 ./out/prover_copy/ext_indep5 $NG $TG 3 < out/xs_$name.txt > out/xs_${name}_prov.txt
python3 -I - "$name" <<'PY'
import re, sys
name = sys.argv[1]
def hits(fn):
    S = set()
    for l in open(fn):
        if l.startswith('HIT:'): S.add(tuple(sorted(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l.split('|')[0]))))
    return S
a, b = hits('out/xs_%s_mine.txt' % name), hits('out/xs_%s_prov.txt' % name)
print('labelled cross-check %s: mine %d hits, ext_indep5 %d hits, identical sets: %s' % (name, len(a), len(b), a == b))
PY
tail -n 1 out/xs_${name}_mine.txt; tail -n 1 out/xs_${name}_prov.txt
