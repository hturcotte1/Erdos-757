"""Synthetic two-sided test of the equivalences of L020 Theorem 3 (iv)(b),(e),(f) and (v)(i2-1)..(i2-4),(i3):
G = disjoint union of stored graphs (all with free choice) [+ isolated y]; random attachments of the given
shape (G-degree <= 2, pairs not inside an edge, pairwise disjoint); (*) computed DIRECTLY as
tau(G + w(P1,P2,P3)) == tau(G) + 1 and compared with the stated condition on NC pairs."""
import sys, random, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from roles_check import read_cell
I = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/'
pool = []
for c in ['3_1_1', '6_3_2', '8_5_3', '10_7_4', '9_4_3', '10_8_4', '12_10_5', '13_9_5']:
    L = read_cell(I + 'cell_%s.txt' % c)
    for n, m, t, es in L[:25]:
        pool.append((n, es))
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
N_PER = int(sys.argv[2]) if len(sys.argv) > 2 else 400


def union(parts, iso=0):
    off = 0
    es = []
    vs_of = []
    for n, e in parts:
        es += [tuple(x + off for x in ed) for ed in e]
        vs_of.append(list(range(off, off + n)))
        off += n
    ys = list(range(off, off + iso))
    return off + iso, es, vs_of, ys


def prep(n, es):
    t = hg.tau_bb(es)
    TL = hg.all_min_transversals(es, t)
    B = [0] * n
    for k, T in enumerate(TL):
        for x in hg.bits(T):
            B[x] |= 1 << k
    d = hg.degrees(n, es)
    share = set()
    for e in es:
        for p in itertools.combinations(sorted(e), 2):
            share.add(p)
    return t, B, d, share


def star(n, es, P):
    t = hg.tau_bb(es)
    w = n
    es2 = es + [tuple(sorted((w,) + tuple(p))) for p in P]
    return hg.tau_bb(es2) == t + 1


res = {}
def record(pat, lhs, rhs):
    k = res.setdefault(pat, [0, 0, 0])  # agree-true, agree-false, disagree
    if lhs == rhs:
        k[0 if lhs else 1] += 1
    else:
        k[2] += 1
        print('DISAGREE', pat)


def pick(lst, k):
    return random.sample(lst, k) if len(lst) >= k else None


trials = 0
while min([sum(v) for v in res.values()] + [0]) < N_PER or len(res) < 9:
    trials += 1
    if trials > 200000:
        break
    pat = random.choice(['b', 'e', 'f', 'i2-1', 'i2-2', 'i2-3', 'i2-4', 'i3'])
    if pat in res and sum(res[pat]) >= N_PER:
        continue
    r = 3 if pat == 'i3' else 2
    iso = 1 if pat.startswith('i') else 0
    parts = [random.choice(pool) for _ in range(r)]
    n, es, vs_of, ys = union(parts, iso)
    t, B, d, share = prep(n, es)
    def fc_ok():
        return all(B[x] for vs in vs_of for x in vs)
    if not fc_ok():
        continue
    low = [[x for x in vs if d[x] <= 2] for vs in vs_of]
    def nc(x, y):
        return d[x] <= 2 and d[y] <= 2 and (B[x] & B[y]) == 0
    def inside_ok(p):
        return tuple(sorted(p)) not in share
    P = None
    if pat == 'b':
        X = pick(low[0], 3); Y = pick(low[1], 3)
        if not X or not Y: continue
        P = [(X[i], Y[i]) for i in range(3)]
        cond = all(nc(a, b) for a, b in itertools.combinations(X, 2)) and all(nc(a, b) for a, b in itertools.combinations(Y, 2))
    elif pat == 'e':
        A = pick(low[0], 3); C = pick(low[1], 3)
        if not A or not C: continue
        a, b, e = A; c, dd, f = C
        if not inside_ok((a, b)) or not inside_ok((c, dd)): continue
        P = [(a, b), (c, dd), (e, f)]
        cond = nc(e, a) and nc(e, b) and nc(f, c) and nc(f, dd)
    elif pat == 'f':
        A = pick(low[0], 4); D = pick(low[1], 2)
        if not A or not D: continue
        a, b, c, e = A; dd, f = D
        if not inside_ok((a, b)): continue
        P = [(a, b), (c, dd), (e, f)]
        cond = nc(a, c) and nc(a, e) and nc(b, c) and nc(b, e) and nc(dd, f)
    else:
        y = ys[0]
        if pat == 'i2-1':
            A = pick(low[0], 3); C = pick(low[1], 2)
            if not A or not C: continue
            a, b, f = A; c, dd = C
            if not inside_ok((a, b)) or not inside_ok((c, dd)): continue
            P = [(a, b), (c, dd), (y, f)]
            cond = nc(a, f) and nc(b, f)
        elif pat == 'i2-2':
            A = pick(low[0], 4); D = pick(low[1], 1)
            if not A or not D: continue
            a, b, c, f = A; dd = D[0]
            if not inside_ok((a, b)): continue
            P = [(a, b), (c, dd), (y, f)]
            cond = nc(a, f) and nc(b, f)
        elif pat == 'i2-3':
            A = pick(low[0], 3); D = pick(low[1], 2)
            if not A or not D: continue
            a, b, c = A; dd, f = D
            if not inside_ok((a, b)): continue
            P = [(a, b), (c, dd), (y, f)]
            cond = nc(a, c) and nc(b, c) and nc(dd, f)
        elif pat == 'i2-4':
            A = pick(low[0], 3); D = pick(low[1], 2)
            if not A or not D: continue
            a, c, f = A; b, dd = D
            P = [(a, b), (c, dd), (y, f)]
            cond = nc(f, a) and nc(f, c) and nc(b, dd)
        elif pat == 'i3':
            A = pick(low[0], 3); C = pick(low[1], 1); D = pick(low[2], 1)
            if not A or not C or not D: continue
            a, b, f = A; c = C[0]; dd = D[0]
            if not inside_ok((a, b)): continue
            P = [(a, b), (c, dd), (y, f)]
            cond = nc(a, f) and nc(b, f)
    lhs = star(n, es, P)
    record(pat, lhs, cond)
print('pattern: [agree with (*) true, agree with (*) false, DISAGREE]')
for k in sorted(res):
    print(' ', k, res[k])
