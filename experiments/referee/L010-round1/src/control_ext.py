"""Referee L010 r1 control: random admissible extensions (no tau requirement) of the class representatives, written as
'CTL:' lines for ref_filter (membership in C, tau range).  Usage: control_ext.py REPFILE NG PER_REP SEED"""
import re, sys, random, itertools
f, NG, K, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
random.seed(seed)
for l in open(f):
    if '(' not in l: continue
    E = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
    deg = [0] * NG
    for e in E:
        for v in e: deg[v] += 1
    inside = set(frozenset(p) for e in E for p in itertools.combinations(e, 2))
    pairs = [p for p in itertools.combinations(range(NG), 2) if deg[p[0]] <= 2 and deg[p[1]] <= 2 and frozenset(p) not in inside]
    trip = [t for t in itertools.combinations(pairs, 3) if len(set(t[0]) | set(t[1]) | set(t[2])) == 6]
    for t in random.sample(trip, min(K, len(trip))):
        H = E + [(a, b, NG) for a, b in t]
        print('CTL: ' + ' '.join('(%d,%d,%d)' % e for e in H))
