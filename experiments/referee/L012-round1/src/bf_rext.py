"""Referee: brute-force validation of rext (every d-set of pairwise disjoint admissible pairs, exact tau of the extension)."""
import sys, itertools, subprocess, re, random
sys.path.insert(0, 'src')
from build_inputs import load, tau
def bf(E, n, d, ep):
    deg = [0] * n; inside = set()
    for e in E:
        for v in e: deg[v] += 1
        for a, b in itertools.combinations(sorted(e), 2): inside.add((a, b))
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if (a, b) not in inside and deg[a] <= ep and deg[b] <= ep]
    t = tau(E, n); out = set()
    def rec(start, chosen, used):
        if len(chosen) == d:
            H = E + [(a, b, n) for a, b in chosen]
            if tau(H, n + 1) == t + 1: out.add(tuple(chosen))
            return
        for i in range(start, len(pairs)):
            a, b = pairs[i]
            if a in used or b in used: continue
            rec(i + 1, chosen + [pairs[i]], used | {a, b})
    rec(0, [], frozenset())
    return out
def rext(E, n, d, ep):
    line = '%d ' % len(E) + ' '.join('%d %d %d' % e for e in E)
    o = subprocess.run(['./out/bin/rext', str(n), str(d), str(ep)], input=line + '\n', capture_output=True, text=True).stdout.splitlines()
    res = set()
    for l in o:
        if l.startswith('X:'):
            v = list(map(int, l.split()[2:])); res.add(tuple(sorted((v[2 * i], v[2 * i + 1]) for i in range(len(v) // 2))))
    return res
cases = []
for typ in [(8, 5, 3), (10, 7, 4)]:
    for E in load(*typ, 4): cases.append((typ, E, typ[0]))
ap = [(0, 1, 2)]
for E in load(8, 5, 3, 4): cases.append(('AP+(8,5,3)', ap + [tuple(v + 3 for v in e) for e in E], 11))
for E in load(10, 7, 4, 4)[:2]: cases.append(('I+(10,7,4)', [tuple(v + 1 for v in e) for e in E], 11))
for E in load(6, 3, 2, 3): cases.append(('(6,3,2)+I+I', E, 8))
tot = 0; bad = 0; ncase = 0
for name, E, n in cases:
    for d, ep in [(2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 2)]:
        if n >= 11 and d == 4 and ep == 3 and name == 'I+(10,7,4)': pass
        a, b = bf(E, n, d, ep), rext(E, n, d, ep)
        ncase += 1; tot += len(a)
        if a != b: bad += 1; print('MISMATCH', name, d, ep, len(a), len(b))
print('cases %d, brute-force hits total %d, mismatches %d' % (ncase, tot, bad))
