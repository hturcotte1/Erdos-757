# Referee data checks of L022 Theorem 4 (O1-O7) and Theorem 1(d) (gluing), independent code.
import json, glob, random
from fractions import Fraction
from itertools import combinations
from rlib import is_45_fast, rank
from check_thm1 import load_sets, aps_of, form

OUT = '/home/user/Erdos-757/experiments/prover/L022/out/'


def check_set(vals):
    n = len(vals)
    E = aps_of(vals)  # rank triples (a,b,c), b midpoint
    fails = []
    # O1
    for (a, b, c) in E:
        if b in (0, n - 1):
            fails.append('O1 midpoint extreme')
        if c == 0 or a == n - 1:
            fails.append('O1 order')
    # O2
    if any(c == 1 for (a, b, c) in E):
        fails.append('O2 x1 right endpoint')
    x1mid = any(b == 1 for (a, b, c) in E)
    if x1mid != ((2 * vals[1] - vals[0]) in set(vals)):
        fails.append('O2 x1 midpoint iff')
    if n >= 3 and any(a == n - 2 for (a, b, c) in E):
        fails.append('O2 x_{n-2} left endpoint')
    # O3 distinct steps; every positive difference at most twice, exactly the steps twice
    steps = [vals[b] - vals[a] for (a, b, c) in E]
    if len(set(steps)) != len(steps):
        fails.append('O3 steps')
    cnt = {}
    for i, j in combinations(range(n), 2):
        d = vals[j] - vals[i]
        cnt[d] = cnt.get(d, 0) + 1
    if max(cnt.values()) > 2 or set(d for d, k in cnt.items() if k == 2) != set(steps):
        fails.append('O3 differences')
    # O4 K30 at a vertex
    for v in range(n):
        L = sorted((c, b) for (a, b, c) in E if a == v)
        if any(L[i][1] >= L[i + 1][1] for i in range(len(L) - 1)):
            fails.append('O4 left')
        R = sorted((a, b) for (a, b, c) in E if c == v)
        if any(R[i][1] >= R[i + 1][1] for i in range(len(R) - 1)):
            fails.append('O4 right')
    # O5
    for (a, b, c) in E:
        if c == n - 1:
            if 2 * vals[b] < vals[0] + vals[n - 1] or ((2 * vals[b] == vals[0] + vals[n - 1]) != (a == 0)):
                fails.append('O5 max')
        if a == 0:
            if 2 * vals[b] > vals[0] + vals[n - 1] or ((2 * vals[b] == vals[0] + vals[n - 1]) != (c == n - 1)):
                fails.append('O5 min')
    if sum(1 for (a, b, c) in E if a == 0 and c == n - 1) > 1:
        fails.append('O5 count')
    # O6: midpoint of at most one AP; rank drop by 2 at degree-3 vertices
    rows = [form(n, *t) for t in E]
    rk = rank(rows, n)
    if rk != len(E):
        fails.append('rank')
    for v in range(n):
        at = [t for t in E if v in t]
        if sum(1 for t in at if t[1] == v) > 1:
            fails.append('O6 midpoint twice')
        if len(at) == 3:
            sub = [x for i, x in enumerate(vals) if i != v]
            E2 = aps_of(sub)
            if len(E2) != len(E) - 3:
                fails.append('O6 heredity')
            r2 = rank([form(n - 1, *t) for t in E2], n - 1) if E2 else 0
            if ((n - 1) - r2) - (n - rk) != 2:
                fails.append('O6 dim drop')
    # O7 (K31): no AP triangle with all three third vertices midpoints
    sets = [set(t) for t in E]
    for i, j, k in combinations(range(len(E)), 3):
        A, B, C = sets[i], sets[j], sets[k]
        ab, ac, bc = A & B, A & C, B & C
        if len(ab) == 1 and len(ac) == 1 and len(bc) == 1 and len(ab | ac | bc) == 3:
            th = [(A - ab - ac), (B - ab - bc), (C - ac - bc)]
            if all(len(s) == 1 for s in th):
                if all(list(s)[0] == E[idx][1] for s, idx in zip(th, (i, j, k))):
                    fails.append('O7 medial triangle')
    return fails


sets = dict(load_sets())
for f in sorted(glob.glob(OUT + 'realize_*.jsonl')):
    for line in open(f):
        r = json.loads(line)
        if r.get('realizable'):
            sets['%s#%d' % (r['cell'], r['cls'])] = sorted(Fraction(x) for x in r['explicit'])
tot = 0
bad = 0
for name, vals in sets.items():
    fl = check_set(vals)
    tot += 1
    if fl:
        bad += 1
        print('FAIL', name, fl[:5])
print('Theorem 4 O1-O7 (+rank=m): sets', tot, 'failures', bad)

# Theorem 1(d): generic gluing C = A u (qB + t)
rng = random.Random(9)
names = [k for k in sets if not k.startswith('C00')]
ok = 0
trials = 60
for _ in range(trials):
    a, b = rng.sample(names, 2)
    A, B = sets[a], sets[b]
    q = Fraction(rng.randint(1, 10**6), rng.randint(1, 10**6))
    t = Fraction(rng.randint(-10**9, 10**9))
    Cset = sorted(set(A) | set(q * x + t for x in B))
    if len(Cset) != len(A) + len(B):
        continue
    good = is_45_fast(Cset) and len(aps_of(Cset)) == len(aps_of(A)) + len(aps_of(B))
    ok += good
print('Theorem 1(d) gluing: %d/%d random generic gluings are (4,5)-sets with H(C) = H(A) + H(B)' % (ok, trials))
