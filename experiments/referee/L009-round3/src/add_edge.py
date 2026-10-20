"""Append one disjoint edge (N1,N1+1,N1+2) to every 'G ...:' graph on vertices 0..N1-1 (for the case T14 + edge)."""
import sys, re
N1 = int(sys.argv[1])
for l in sys.stdin:
    if not l.startswith('G '): continue
    head, body = l.split(':', 1)
    es = re.findall(r'\([\d,]+\)', body)
    print('%s: %s (%d,%d,%d)' % (head, ' '.join(es), N1, N1 + 1, N1 + 2))
