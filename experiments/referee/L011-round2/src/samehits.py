"""Referee L011 r2: compare two HIT files as sets of labelled edge sets.  Usage: python3 -I samehits.py A B"""
import sys, re, gzip
def S(p):
    op = gzip.open if p.endswith('.gz') else open
    out = []
    for l in op(p, 'rt'):
        if l.startswith('HIT'):
            out.append(frozenset(frozenset(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', l)))
    return out
a, b = S(sys.argv[1]), S(sys.argv[2])
print('A lines %d distinct %d | B lines %d distinct %d | %s' % (len(a), len(set(a)), len(b), len(set(b)), 'EQUAL' if set(a) == set(b) else 'DIFFERENT'))
