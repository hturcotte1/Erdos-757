"""Restrict a hit file (new vertex = NG) to the hits whose input part (edges avoiding NG) is one of the graphs of a sample file;
compare with another hit file as sets of edge sets.  Usage: restrict_hits.py NG SAMPLE PROVERHITS MYHITS"""
import re, sys
NG = int(sys.argv[1])
def es(l): return frozenset(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l))
S = set(es(l) for l in open(sys.argv[2]) if '(' in l)
P = set()
for l in open(sys.argv[3]):
    if not l.startswith('HIT'): continue
    e = es(l); inp = frozenset(x for x in e if NG not in x)
    if inp in S: P.add(e)
M = set(es(l) for l in open(sys.argv[4]) if l.startswith('HIT') or l.startswith('CHIT'))
print('sample inputs %d | prover hits on sample %d | referee hits %d | identical: %s' % (len(S), len(P), len(M), P == M))
