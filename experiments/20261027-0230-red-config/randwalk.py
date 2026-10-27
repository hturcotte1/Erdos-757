#!/usr/bin/env python3
"""Heuristic [heuristic]: random members of C (max degree <= 3) of larger n, grown from random 12-point classes by uniformly random
one-edge extensions (bin/extend with nofilter), then exact (Red) statistics with bin/redfree.  Usage: randwalk.py SEED NWALKS NSTART N_END KMODE"""
import os, random, subprocess, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(HERE, 'bin', 'extend'); RF = os.path.join(HERE, 'bin', 'redfree')
seed, nw, nstart, nend = map(int, sys.argv[1:5]); random.seed(seed)
cell = {(11, 9): None, (12, 10): None, (13, 11): None, (12, 9): None, (13, 10): None}
def pick(n, m):
    L = [l for l in open(os.path.join(HERE, 'out', f'cls_{n}_{m}.txt'))]
    return L
base = pick(nstart, nstart - 2)
def to_edges(line):
    p = line.split(); return p[2:]
def children(line, np_, K):
    r = subprocess.run([EXT, str(np_), str(K), '3', 'nofilter'], input=line, capture_output=True, text=True).stdout.strip().split('\n')
    return [x for x in r if x.startswith('FOUND')]
def conv(found):   # "FOUND: (a,b,c) ..." -> "C m a.b.c ..."
    import re
    es = re.findall(r'\((\d+),(\d+),(\d+)\)', found); return 'C %d %s\n' % (len(es), ' '.join('%s.%s.%s' % e for e in es))
stats = collections.Counter(); out = []
for w in range(nw):
    line = random.choice(base); n = nstart; ok = True
    while n < nend:
        opts = []
        for K in (1, 2):
            opts += [(K, c) for c in children(line, n, K)]
        if not opts: ok = False; break
        # prefer dense: choose K=1 mostly (keeps deficiency), K=2 with prob 1/4 of picks
        K1 = [o for o in opts if o[0] == 1]; K2 = [o for o in opts if o[0] == 2]
        o = random.choice(K1) if (K1 and (not K2 or random.random() < 0.75)) else random.choice(K2)
        line = conv(o[1]); n += o[0]
    if ok: out.append((n, line))
bynn = collections.defaultdict(list)
for n, l in out: bynn[n].append(l)
for n, L in sorted(bynn.items()):
    r = subprocess.run([RF, str(n)], input=''.join(L), capture_output=True, text=True).stdout.strip().split('\n')
    c = collections.Counter(); slk = collections.defaultdict(list); rfree = 0
    for x in r:
        t = x.split('\t'); mz = int(t[13]); c[mz] += 1; rfree += int(t[5]); slk[mz].append(int(t[3]))
    print('n=%d graphs=%d redfree=%d min|Z| histogram %s' % (n, len(L), rfree, dict(sorted(c.items()))), 'm hist', dict(collections.Counter(int(x.split('\t')[1]) for x in r)))
