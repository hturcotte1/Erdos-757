#!/usr/bin/env python3
"""(Red') check: for the maximizer Z* of value (cols 11,12), no vertex y outside Z* has all its edges meeting Z*, unless Z* + y = V.
Usage: check_closure.py out/red_n_m.tsv ... ; prints violations count."""
import sys
bad = tot = 0
for f in sys.argv[1:]:
    for l in open(f):
        t = l.rstrip('\n').split('\t'); n = int(t[0]); Z = int(t[10], 16)
        E = [tuple(map(int, x.split('.'))) for x in t[-1].split()[1:]]
        tot += 1
        EZ = [e for e in E if any(Z >> v & 1 for v in e)]
        for y in range(n):
            if Z >> y & 1: continue
            ey = [e for e in E if y in e]
            if all(e in EZ for e in ey) and (Z | 1 << y) != (1 << n) - 1:
                bad += 1; break
print('graphs', tot, 'with a free vertex y outside the maximizer Z*:', bad)
