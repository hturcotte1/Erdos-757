"""Per-class pattern profile of the 45 classes of L020 Theorem 1 (K29_classes.json read as data only),
to check the counts now written in the Theorem 1 statement: all 45 have a pattern-(e) vertex, three
Theta-vertices each, 27 have an (f)-vertex (10,7,4)+(18,13,7), 31 have a (b)-vertex E1+(25,19,10)."""
import json, re, sys
from collections import Counter
from hgr2 import HG, in_C
from patt import analyse

cert = open('/home/user/Erdos-757/results/proofs/L020-joint-induction-i11.md').read()
blk = cert[cert.index('$$K_{29}='):]
blk = blk[:blk.index('Each of the 45 graphs')]
K29 = sorted(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\\\{(\d+,\d+,\d+)\\\}', blk))
print('K29 from text: edges', len(K29))
data = json.load(open('/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'))
print('classes in json', len(data))
c0 = sorted(tuple(sorted(e)) for e in data[0]['edges'])
print('K29 text == class 0:', c0 == K29)
tot = Counter(); per = []
allfails = 0
for ci, d in enumerate(data):
    E = [tuple(sorted(e)) for e in d['edges']]
    V = sorted(set(u for e in E for u in e))
    K = HG(V, E)
    assert len(V) == 29 and len(E) == 23 and K.tau() == 12
    prof = Counter()
    for v in V:
        if K.deg(v) != 3: continue
        res = analyse(K, v)
        allfails += len(res['fails'])
        if res['fails']: print('class', ci, 'v', v, res)
        tot[res['pattern']] += 1
        if res['pattern'] == 'e' and res['cells'] == [(8,5,3),(20,15,8)]: prof['e853+20158'] += 1
        elif res['pattern'] == 'f' and res['detail'][1] == (6,3,2) and res['detail'][3] == (22,17,9): prof['theta'] += 1
        elif res['pattern'] == 'f' and res['detail'][1] == (18,13,7) and res['detail'][3] == (10,7,4): prof['f18137+1074'] += 1
        elif res['pattern'] == 'b' and res['cells'] == [(3,1,1),(25,19,10)]: prof['bE1+251910'] += 1
        else: prof['other:%s:%s' % (res['pattern'], res['cells'])] += 1
    per.append(prof)
print('pattern totals over all degree-3 vertices:', dict(tot), 'sum', sum(tot.values()))
print('fails', allfails)
keys = sorted(set(k for p in per for k in p))
for k in keys:
    vals = Counter(p.get(k, 0) for p in per)
    print('%-40s classes with >=1: %2d   distribution of counts per class: %s' % (k, sum(1 for p in per if p.get(k, 0) > 0), dict(sorted(vals.items()))))
