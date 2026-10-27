"""Check of Lemma R2 (edge-deletion closure of R) of L022 on stored sets: for a (4,5)-set A with AP set E (rank labels) and
a set D of APs, a generic point x of the solution space V' of the AP equations of E \\ D close to A is a (4,5)-set, in the
same order as A, whose AP hypergraph is exactly E \\ D.  We compute a rational basis of V' exactly, take x = A + eps*w for a
random integer combination w of the basis and a small eps, scale to integers and verify exactly (e757.core.is_45_set, AP set).
Also re-checks rank(E) = m (Lemma R1).  usage: python3 edge_delete_check.py seed trials_per_set"""
import sys, json, random, glob
from fractions import Fraction as Fr
from math import lcm
import lib22

def nullspace(rows, n):
    M = [list(map(Fr, r)) for r in rows]; piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; inv = 1 / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [Fr(0)] * n; v[fc] = Fr(1)
        for i, pc in enumerate(piv): v[pc] = -M[i][fc]
        basis.append(v)
    return basis, len(piv)

def rows_of(E, n):
    out = []
    for (i, j, k) in E:
        r = [0] * n; r[i] += 1; r[k] += 1; r[j] -= 2; out.append(r)
    return out

def try_delete(A, E, D, rnd):
    n = len(A); Ep = [e for e in E if e not in D]
    basis, rk = nullspace(rows_of(Ep, n), n)
    for attempt in range(20):
        coef = [rnd.randint(-50, 50) for _ in basis]
        w = [sum(cb * b[i] for cb, b in zip(coef, basis)) for i in range(n)]
        span = A[-1] - A[0]
        eps = Fr(1, 10 ** 4) * span / (max(abs(x) for x in w) or 1)
        x = [A[i] + eps * w[i] for i in range(n)]
        den = 1
        for t in x: den = lcm(den, t.denominator)
        xi = [int(t * den) for t in x]
        if sorted(xi) != xi: continue           # order preserved
        if not lib22.is_45(xi): continue
        if set(lib22.ap_triples(xi)) == set(Ep): return True
    return False

seed, T = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed)
sets = []
d = json.load(open('/home/user/Erdos-757/data/small_records.json'))
for k, v in d['sets'].items(): sets.append(('small_records:' + k, sorted(v['set'])))
for f in sorted(glob.glob('/home/user/Erdos-757/results/claims/C00[12]*.json')):
    sets.append(('claim:' + f.split('/')[-1][:4], sorted(json.load(open(f))['set'])))
for c in ['10_7_4', '15_11_6', '17_13_7', '22_17_9', '26_22_11']:
    got = 0
    for l in open('/home/user/Erdos-757/experiments/prover/L022/out/realize_%s.jsonl' % c):
        r = json.loads(l)
        if r.get('explicit') and got < 3:
            sets.append(('realized:%s#%d' % (r['cell'], r['cls']), sorted(r['explicit']))); got += 1
tot = dict(cases=0, ok=0, rank_full=0, sets=0)
for name, A in sets:
    E = lib22.ap_triples(A); n = len(A); tot['sets'] += 1
    _, rk = nullspace(rows_of(E, n), n)
    if rk == len(E): tot['rank_full'] += 1
    cases = [[e] for e in E] + [rnd.sample(E, rnd.randint(1, len(E))) for _ in range(T)]
    good = 0
    for D in cases:
        tot['cases'] += 1
        if try_delete(A, E, D, rnd): tot['ok'] += 1; good += 1
    print(name, 'n', n, 'm', len(E), 'rank', rk, 'deletions ok', good, '/', len(cases), flush=True)
print(tot)
