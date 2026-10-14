"""Route C (referee round 4): recount every number the proof text quotes for the case split, with new code.
h is computed two ways, neither of them the judge's: (i) the criterion h(B)=h(A)+2 iff some maximum Sidon
subset S of A has S u {x,y} Sidon (definition-level), (ii) exact MaxSAT (pysat RC2) on all sum collisions."""
import itertools, json, sys, time, random
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round4')
from r4_lib import A_BASE, is45_full, is_sidon, sidon_subsets, h_maxsat

EXP = '/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/'
t0 = time.time()
A = [Fr(a) for a in A_BASE]
Aset = set(A)
out = {}


def aps(pts):
    s = set(pts)
    L = sorted(pts)
    return [(L[i], (L[i] + L[j]) / 2, L[j]) for i in range(len(L)) for j in range(i + 1, len(L)) if (L[i] + L[j]) / 2 in s]


# ---- A_base
assert len(Aset) == 14 and is45_full(A)
M = sidon_subsets(A, 8)
assert not sidon_subsets(A, 9)
hA, _ = h_maxsat(A)
apA = aps(A)
mids = sorted(m for _, m, _ in apA)
out['A_base'] = {'(4,5)': True, 'h_bruteforce': 8, 'n_max_sidon': len(M), 'h_maxsat': hA, 'n_3APs': len(apA),
                 'midpoints_are_interior_points': mids == sorted(A)[1:-1]}
print(out['A_base'], flush=True)
Msets = [set(S) for S in M]


def h_crit(base, new):
    """h(base u new) == 8 + len(new)  iff some S in M has S u new Sidon."""
    return any(is_sidon(list(S) + list(new)) for S in M)


# ---- P (the proof's P_x)
mid = {(a + b) / 2 for a, b in itertools.combinations(A, 2)}
end = {2 * b - a for a in A for b in A if a != b}
P_full = mid | end
P = sorted(P_full - Aset)
out['|P_full|'] = len(P_full)
out['|P_full n A|'] = len(P_full & Aset)
out['|P| = |P_full minus A|'] = len(P)
P_ok = [x for x in P if is45_full(A + [x])]
out['|P_ok|'] = len(P_ok)
h1 = {}
for x in P_ok:
    hc = 9 if h_crit(A, [x]) else 8
    hm, _ = h_maxsat(A + [x])
    assert hc == hm, (x, hc, hm)
    h1[str(x)] = hm
out['h(A u {x}) distribution over P_ok'] = {str(v): list(h1.values()).count(v) for v in set(h1.values())}
print(out, flush=True)

# ---- T1b
cand = set()
for x in P_ok:
    Ax = A + [x]
    Q = set()
    for u, v in itertools.combinations(Ax, 2):
        Q |= {(u + v) / 2, 2 * u - v, 2 * v - u}
    Q -= set(Ax)
    for y in Q:
        cand.add(frozenset((x, y)))
out['T1b candidate unordered pairs'] = len(cand)
ok45 = set()
hdist = {}
for c in cand:
    x, y = sorted(c)
    if is45_full(A + [x, y]):
        ok45.add(c)
        hc = 10 if h_crit(A, [x, y]) else None
        hm, _ = h_maxsat(A + [x, y])
        assert hc == hm == 10, (x, y, hc, hm)
        hdist[hm] = hdist.get(hm, 0) + 1
out['T1b (4,5) pairs'] = len(ok45)
out['T1b h distribution'] = {str(k): v for k, v in hdist.items()}
out['T1b (4,5) pairs with both points in P'] = sum(1 for c in ok45 if all(v in set(P) for v in c))
print('T1b done', round(time.time() - t0, 1), out['T1b candidate unordered pairs'], out['T1b (4,5) pairs'], flush=True)

# ---- compare with stored data (exact Fraction keys)
R = json.load(open(EXP + 'results.json'))
stored = {frozenset((Fr(a), Fr(b))) for a, b, h in R['stored']}
out['stored rows / distinct keys'] = [len(R['stored']), len(stored)]
out['stored h values'] = sorted({h for _, _, h in R['stored']})
out['stored symmetric difference with my T1b (4,5) set'] = len(stored ^ ok45)
out['results.json summary fields'] = {k: R[k] for k in R if k not in ('stored', 'type2_lines', 'hdist')}
out['results.json type2_lines alphas'] = sorted({l[2] for l in R['type2_lines']})
W = json.load(open(EXP + 'witnesses.json'))
bad = 0
wkeys = set()
for w in W['pairs']:
    x, y = Fr(w['x']), Fr(w['y'])
    S = [Fr(v) for v in w['S']]
    wkeys.add(frozenset((x, y)))
    if not (len(S) == 10 and len(set(S)) == 10 and set(S) <= Aset | {x, y} and is_sidon(S)):
        bad += 1
out['witnesses.json pairs: count / invalid (Sidon by definition) / key set == stored'] = [len(W['pairs']), bad, wkeys == stored]
bad9 = 0
for w in W['generic_y']:
    x = Fr(w['x'])
    S = [Fr(v) for v in w['S9']]
    if not (len(S) == 9 and len(set(S)) == 9 and set(S) <= Aset | {x} and is_sidon(S)):
        bad9 += 1
out['witnesses.json generic_y: count / invalid / x-set == P_ok'] = [len(W['generic_y']), bad9,
                                                                    {Fr(w['x']) for w in W['generic_y']} == set(P_ok)]
print(out, flush=True)

# ---- T2
lines = []
for a in A:
    lines.append(('x_mid', a, Fr(2), -a))       # 2x = a + y
    lines.append(('y_mid', a, Fr(1, 2), a / 2))  # 2y = a + x
    lines.append(('a_mid', a, Fr(-1), 2 * a))    # x + y = 2a
assert len({(m, c) for _, _, m, c in lines}) == 42
pts = set()
npar = 0
for (r1, a1, m1, c1), (r2, a2, m2, c2) in itertools.combinations(lines, 2):
    if m1 == m2:
        npar += 1
        continue
    x = (c2 - c1) / (m1 - m2)
    pts.add((x, m1 * x + c1))
filt = [(x, y) for x, y in pts if x != y and x not in Aset and y not in Aset]
n45 = sum(1 for x, y in filt if is45_full(A + [x, y]))


def ncross(x, y):
    return sum(1 for a in A if 2 * a == x + y) + sum(1 for a in A if 2 * x == a + y) + sum(1 for a in A if 2 * y == a + x)


out['T2'] = {'lines': len(lines), 'parallel pairs': npar, 'nonparallel pairs': 861 - npar,
             'distinct intersection points': len(pts), 'after filter (x!=y, x,y not in A)': len(filt),
             '(4,5) among them': n45, 'min cross APs at filtered points': min(ncross(*p) for p in filt),
             'points with a coordinate in P': sum(1 for x, y in filt if x in set(P) or y in set(P)),
             'every a avoided by some max Sidon set': all(any(a not in S for S in Msets) for a in A)}
# random points on each line (generic with probability 1; checked: exactly 13 APs)
rng = random.Random(7)
line_stats = {}
for role, a, m, c in lines:
    res = []
    for _ in range(4):
        x = Fr(rng.randrange(-10**6, 10**6), 1000003)
        y = m * x + c
        B = A + [x, y]
        nap = len(aps(B))
        if is45_full(B):
            hm, _ = h_maxsat(B)
            res.append((nap, hm))
        else:
            res.append((nap, None))
    line_stats[role + ':' + str(a)] = res
out['T2 random points: all have exactly 13 APs'] = all(r[0] == 13 for v in line_stats.values() for r in v)
out['T2 random points: h values at (4,5) points'] = sorted({r[1] for v in line_stats.values() for r in v if r[1] is not None})
out['T2 lines with (4,5) random points'] = sum(1 for v in line_stats.values() if any(r[1] is not None for r in v))
out['seconds'] = round(time.time() - t0, 1)
print(json.dumps(out, indent=1, default=str), flush=True)
json.dump(out, open('/home/user/Erdos-757/experiments/referee/L001-round4/r4_cases_out.json', 'w'), indent=1, default=str)
