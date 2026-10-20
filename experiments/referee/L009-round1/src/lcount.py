"""Referee L009: read 'canon' output lines '<canon> <line> <|Aut|>' and print: number of lines, number of distinct canonical
forms, and the number of labelled copies on [n] = sum over DISTINCT classes of n!/|Aut| (n taken from the canon prefix)."""
import sys, math
seen = {}; lines = 0
for l in sys.stdin:
    c, ln, aut = l.split(); lines += 1
    a = int(aut)
    if c in seen: assert seen[c] == a
    seen[c] = a
n = None; tot = 0
for c, a in seen.items():
    n = int(c.split('_')[0]); f = math.factorial(n); assert f % a == 0; tot += f // a
print('lines', lines, 'classes', len(seen), 'labelled_copies', tot)
