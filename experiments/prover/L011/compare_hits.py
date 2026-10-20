"""Compare two HIT files as sets of edge sets."""
import re, sys
def P(f):
    return [frozenset(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)) for l in open(f) if l.startswith('HIT:')]
A, B = P(sys.argv[1]), P(sys.argv[2])
print(sys.argv[1], len(A), 'distinct', len(set(A)), '|', sys.argv[2], len(B), 'distinct', len(set(B)), '| identical sets:', set(A) == set(B))
