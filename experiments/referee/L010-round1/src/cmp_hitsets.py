"""Compare two hit files as sets of labelled edge sets (any line containing '(' and a tag starting with HIT/CHIT)."""
import re, sys
def P(f):
    S = []
    for l in open(f):
        if not (l.startswith('HIT') or l.startswith('CHIT')): continue
        S.append(frozenset(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)))
    return S
A, B = P(sys.argv[1]), P(sys.argv[2])
print('%s: %d (distinct %d) | %s: %d (distinct %d) | identical sets: %s' % (sys.argv[1], len(A), len(set(A)), sys.argv[2], len(B), len(set(B)), set(A) == set(B)))
