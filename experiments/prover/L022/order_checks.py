"""Data checks of the order facts of L022 (Section 'What the order structure buys') on stored realizable sets.
Sets: data/small_records.json, results/claims/C001..C005, and the explicit exact realizations found by realize_lists.py
(out/realize_*.jsonl, field 'explicit').  All checks exact (integers / Fractions).
Checks per set A (sorted, ranks 0..n-1):
 O1 min and max are never midpoints, never right resp. left endpoints;   O2 x_1 never a right endpoint, M(x_1) = [2x_1-x_0 in A];
 O3 the m APs have pairwise distinct steps;   O4 K30;   O5 no medial triangle (K31);   O6 midpoints of APs at max lie in the right
 half [(min+max)/2, max) (equality iff the AP contains min), symmetrically for min;   O7 every degree-3 vertex is the midpoint of at
 most one of its APs and satisfies the two reflection relations;   O8 rank of the AP equation system over Q (= m means every AP is free).
Prints one summary line per set and the totals."""
import json, glob, itertools, sys
from fractions import Fraction as Fr
import lib22

def rank_Q(rows, n):
    rows = [list(map(Fr, r)) for r in rows]; rk = 0; col = 0
    piv_rows = []
    M = rows
    r = 0
    for c in range(n):
        p = None
        for i in range(r, len(M)):
            if M[i][c] != 0: p = i; break
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return r

def check(name, A):
    A = sorted(A); n = len(A); E = lib22.ap_triples(A); m = len(E)
    L, M, R = lib22.roles(n, E); d = lib22.deg(n, E)
    res = {}
    res['O1'] = M[0] == 0 and M[n - 1] == 0 and R[0] == 0 and L[n - 1] == 0
    res['O2'] = R[1] == 0 and M[1] == (1 if (2 * A[1] - A[0]) in set(A) else 0) and L[n - 2] == 0
    steps = [A[j] - A[i] for (i, j, k) in E]
    res['O3'] = len(set(steps)) == m
    res['O4'] = lib22.k30_ok(E)
    res['O5'] = not lib22.medial_triangle(E)
    ok6 = True
    for (i, j, k) in E:
        if k == n - 1:
            if not (2 * A[j] >= A[0] + A[n - 1] and ((2 * A[j] == A[0] + A[n - 1]) == (i == 0))): ok6 = False
        if i == 0:
            if not (2 * A[j] <= A[0] + A[n - 1] and ((2 * A[j] == A[0] + A[n - 1]) == (k == n - 1))): ok6 = False
    res['O6'] = ok6
    ok7 = True; prof = {}
    for v in range(n):
        if d[v] != 3: continue
        es = [e for e in E if v in e]
        mids = [e for e in es if e[1] == v]
        if len(mids) > 1: ok7 = False
        refl = set()
        for (i, j, k) in es:
            if j == v: refl.add(Fr(A[i] + A[k], 2))
            elif i == v: refl.add(Fr(2 * A[j] - A[k]))
            else: refl.add(Fr(2 * A[j] - A[i]))
        if refl != {Fr(A[v])}: ok7 = False
        key = (L[v], M[v], R[v]); prof[key] = prof.get(key, 0) + 1
    res['O7'] = ok7
    rows = []
    for (i, j, k) in E:
        r = [0] * n; r[i] += 1; r[k] += 1; r[j] -= 2; rows.append(r)
    rk = rank_Q(rows, n) if rows else 0
    res['O8_rank'] = rk; res['m'] = m; res['n'] = n
    res['deg_min'] = d[0]; res['deg_max'] = d[n - 1]
    res['deg3_profiles(L,M,R)'] = {str(k): v for k, v in sorted(prof.items())}
    return res

sets = []
d = json.load(open('/home/user/Erdos-757/data/small_records.json'))
for k, v in d['sets'].items(): sets.append(('small_records:' + k, v['set']))
for f in sorted(glob.glob('/home/user/Erdos-757/results/claims/C00*.json')):
    c = json.load(open(f)); sets.append(('claim:' + f.split('/')[-1][:4], c['set']))
for f in sorted(glob.glob('/home/user/Erdos-757/experiments/prover/L022/out/realize_*.jsonl')):
    for l in open(f):
        r = json.loads(l)
        if r.get('explicit'): sets.append(('realized:%s#%d' % (r['cell'], r['cls']), r['explicit']))
tot = dict(sets=0, fails=0, free_all=0)
for name, A in sets:
    assert lib22.is_45(A), name
    res = check(name, A); tot['sets'] += 1
    bad = [k for k in ('O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7') if not res[k]]
    if bad: tot['fails'] += 1
    if res['O8_rank'] == res['m']: tot['free_all'] += 1
    if not name.startswith('realized') or bad or res['O8_rank'] != res['m']:
        print(name, 'n', res['n'], 'm', res['m'], 'rank', res['O8_rank'], 'deg(min,max)', (res['deg_min'], res['deg_max']),
              'deg3 profiles', res['deg3_profiles(L,M,R)'], 'FAILED' if bad else 'ok', bad)
# aggregate over realized pieces
agg = {}; dm = {}
for name, A in sets:
    if not name.startswith('realized'): continue
    res = check(name, A)
    for k, v in res['deg3_profiles(L,M,R)'].items(): agg[k] = agg.get(k, 0) + v
    key = (res['deg_min'], res['deg_max']); dm[str(key)] = dm.get(str(key), 0) + 1
print('realized pieces: deg3 role profiles (L,M,R) totals', agg)
print('realized pieces: (deg min, deg max) histogram', dm)
print(tot)
