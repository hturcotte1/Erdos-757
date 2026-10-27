"""Referee (L022, round 1, referee #2): independent exact realizability checker.
No import of e757, judge, rexact or any L0xx code. Exact Fractions throughout.

A 3-graph on vertices 0..n-1 is "sub-realizable" if some (4,5)-set A has H as a sub-hypergraph of H(A)
(by L022 Theorem 1(a),(c) this is the same as exact realizability).  Method: for every injective midpoint
labelling, compute the solution space of the AP equations over Q (RREF), express the generic point as rows
R[v] in Q^k, and test the relations forced on the whole space: equal coordinates, weak-Sidon violation,
two forced APs sharing two vertices.  A labelling survives iff none is forced; then a generic point realizes.
"""
import sys, json, itertools, random, time
from fractions import Fraction as Fr

def generic_point(labelled, n):
    """labelled: list of (a, mid, c). returns (R rows over free params, rank)."""
    M = []
    for (a, b, c) in labelled:
        row = [Fr(0)] * n
        row[a] += 1; row[c] += 1; row[b] -= 2
        M.append(row)
    piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M):
            break
    free = [c for c in range(n) if c not in piv]
    k = len(free); fidx = {f: i for i, f in enumerate(free)}
    R = [None] * n
    for f in free:
        t = [Fr(0)] * k; t[fidx[f]] = Fr(1); R[f] = tuple(t)
    for i, c in enumerate(piv):
        R[c] = tuple(-M[i][f] for f in free)
    return R, r

def forced(R):
    """returns (kind or None, forced APs as (a,b,c) with b midpoint)."""
    n = len(R)
    seen = set()
    for v in range(n):
        if R[v] in seen:
            return 'EQ', None
        seen.add(R[v])
    sums = {}
    for a in range(n):
        for c in range(a + 1, n):
            s = tuple(x + y for x, y in zip(R[a], R[c]))
            if s in sums:
                return 'SIDON', None
            sums[s] = (a, c)
    F = []
    for b in range(n):
        s = tuple(2 * x for x in R[b])
        if s in sums:
            a, c = sums[s]; F.append((a, b, c))
    for e1, e2 in itertools.combinations(F, 2):
        if len(set(e1) & set(e2)) >= 2:
            return 'NONLIN', None
    return None, F

def surviving_labellings_bruteforce(E, n):
    """all injective midpoint labellings with no forced coincidence (brute force over 3^m)."""
    out = []
    for choice in itertools.product(range(3), repeat=len(E)):
        mids = [E[i][choice[i]] for i in range(len(E))]
        if len(set(mids)) < len(mids):
            continue
        lab = []
        for e, mi in zip(E, choice):
            a, c = [x for j, x in enumerate(e) if j != mi]
            lab.append((a, e[mi], c))
        R, rk = generic_point(lab, n)
        kind, F = forced(R)
        if kind is None:
            out.append((lab, F, R))
    return out

def dfs_realizable(E, n, tlimit=600.0):
    """DFS over labellings with sound pruning (relations forced on a space are forced on its subspaces).
    returns (labelling or None, timed_out, nodes)."""
    t0 = time.time(); m = len(E)
    # order edges: maximise overlap with already placed vertices
    order = []; rem = list(range(m)); cov = set()
    while rem:
        best = max(rem, key=lambda i: (len(cov & set(E[i])), -i))
        order.append(best); rem.remove(best); cov |= set(E[best])
    lab = [None] * m; used = set(); st = {'nodes': 0, 'to': False}
    def rec(k):
        if time.time() - t0 > tlimit:
            st['to'] = True; return None
        if k == m:
            return list(lab)
        e = E[order[k]]
        for mi in range(3):
            mid = e[mi]
            if mid in used:
                continue
            a, c = [x for j, x in enumerate(e) if j != mi]
            lab[order[k]] = (a, mid, c); used.add(mid)
            st['nodes'] += 1
            R, rk = generic_point([l for l in lab if l is not None], n)
            kind, F = forced(R)
            if kind is None:
                res = rec(k + 1)
                if res is not None or st['to']:
                    return res
            used.discard(mid); lab[order[k]] = None
        return None
    res = rec(0)
    return res, st['to'], st['nodes']

def explicit_integer_point(R, n, rnd, tries=100, bound=10 ** 6):
    k = len(R[0])
    from math import lcm
    for _ in range(tries):
        p = [rnd.randint(-bound, bound) for _ in range(k)]
        vals = [sum(x * y for x, y in zip(R[v], p)) for v in range(n)]
        den = 1
        for x in vals:
            den = lcm(den, x.denominator)
        iv = [int(x * den) for x in vals]
        if len(set(iv)) < n:
            continue
        return iv
    return None

def is45(A):
    """every 4-subset determines >= 5 distinct positive differences (brute force)."""
    A = list(A)
    if len(set(A)) < len(A):
        return False
    for B in itertools.combinations(A, 4):
        ds = set()
        for x, y in itertools.combinations(B, 2):
            ds.add(abs(x - y))
        if len(ds) < 5:
            return False
    return True

def aps_by_label(vals):
    """3-APs of the point list vals, as frozensets of indices (labels), midpoint anywhere."""
    pos = {}
    for i, x in enumerate(vals):
        pos[x] = i
    out = set()
    for a, c in itertools.combinations(range(len(vals)), 2):
        s = vals[a] + vals[c]
        if s % 2 == 0 and s // 2 in pos:
            out.add(frozenset((a, pos[s // 2], c)))
    return out

def exact_realization_check(iv, E):
    """iv indexed by the class's vertex labels; E edge list on those labels."""
    return is45(iv) and aps_by_label(iv) == {frozenset(e) for e in E}

if __name__ == '__main__':
    rnd = random.Random(2026)
    Q10 = [(0, 1, 2), (0, 3, 4), (1, 5, 7), (2, 6, 8), (3, 7, 9), (4, 8, 9), (5, 6, 9)]
    print('== Q10 exhaustive over all 3^7 labellings')
    tot = 0; inj = 0
    for choice in itertools.product(range(3), repeat=7):
        tot += 1
        mids = [Q10[i][choice[i]] for i in range(7)]
        if len(set(mids)) == 7:
            inj += 1
    surv = surviving_labellings_bruteforce(Q10, 10)
    print('labellings', tot, 'injective', inj, 'surviving (no forced coincidence)', len(surv))
    print('Q10 NOT sub-realizable' if not surv else 'Q10 REALIZABLE ?!')
    print('== Q10 six-edge subsets: realizable with explicit exact integer (4,5)-set')
    allok = True
    for sub in itertools.combinations(Q10, 6):
        vs = sorted({x for e in sub for x in e}); mp = {v: i for i, v in enumerate(vs)}
        Es = [tuple(mp[x] for x in e) for e in sub]
        surv = surviving_labellings_bruteforce(Es, len(vs))
        found = False
        for lab, F, R in surv:
            if {frozenset(f) for f in F} != {frozenset(e) for e in Es}:
                continue  # want exactly these APs forced
            for _ in range(20):
                iv = explicit_integer_point(R, len(vs), rnd)
                if iv and exact_realization_check(iv, Es):
                    found = True; break
            if found:
                break
        removed = [e for e in Q10 if e not in sub][0]
        print('  minus', removed, 'vertices', len(vs), 'surviving labellings', len(surv), 'exact realization', 'OK' if found else 'FAILED', iv if found else '')
        allok &= found
    print('all six-edge subsets exactly realizable:', allok)

    print('== stored explicit realizations (experiments/prover/L022/out/realize_*.jsonl): own (4,5) + exact AP check')
    INP = '/home/user/Erdos-757/experiments/20261027-0300-transversal-richness/inputs/cell_%s.txt'
    tot = dict(records=0, explicit=0, ok=0, bad=0, nonreal=0)
    nonreal_list = []
    for c in ['3_1_1', '10_7_4', '14_12_6', '17_13_7', '8_5_3', '12_10_5', '15_11_6', '19_16_8', '22_17_9', '26_22_11']:
        lines = [l.split() for l in open(INP % c) if l.strip()]
        for l in open('/home/user/Erdos-757/experiments/prover/L022/out/realize_%s.jsonl' % c):
            r = json.loads(l); tot['records'] += 1
            t = lines[r['cls']]; n, m = int(t[0]), int(t[1]); xs = list(map(int, t[3:]))
            E = [tuple(xs[3 * i:3 * i + 3]) for i in range(m)]
            assert n == r['n'] and m == r['m']
            if r.get('explicit'):
                tot['explicit'] += 1
                if exact_realization_check(r['explicit'], E):
                    tot['ok'] += 1
                else:
                    tot['bad'] += 1; print('  BAD explicit', c, r['cls'])
            elif 'realizable' in r and not r['realizable']:
                tot['nonreal'] += 1; nonreal_list.append((c, r['cls']))
    print(tot)
    print('non-realizable (stored verdicts):', nonreal_list)

    print('== independent DFS decision on the 13 tight Delta<=3 classes')
    for c in ['3_1_1', '10_7_4', '14_12_6', '17_13_7']:
        lines = [l.split() for l in open(INP % c) if l.strip()]
        for ci, t in enumerate(lines):
            n, m = int(t[0]), int(t[1]); xs = list(map(int, t[3:]))
            E = [tuple(xs[3 * i:3 * i + 3]) for i in range(m)]
            deg = [0] * n
            for e in E:
                for x in e: deg[x] += 1
            if max(deg) > 3:
                print('  ', c, ci, 'Delta =', max(deg), 'skipped'); continue
            lab, to, nodes = dfs_realizable(E, n, tlimit=900)
            verdict = 'TIMEOUT' if to else ('REALIZABLE' if lab else 'NOT realizable')
            extra = ''
            if lab:
                R, rk = generic_point(lab, n)
                kind, F = forced(R)
                iv = None
                for _ in range(30):
                    iv = explicit_integer_point(R, n, rnd)
                    if iv and exact_realization_check(iv, E): break
                    iv = None
                extra = 'explicit exact integer set OK' if iv else 'explicit point FAILED'
            print('  ', c, 'class', ci, 'degrees', ''.join(str(d) for d in sorted(deg)), verdict, 'nodes', nodes, extra, flush=True)

    print('== obstructions.json: maximum degree of each stored obstruction')
    obs = json.load(open('/home/user/Erdos-757/experiments/20261027-0400-realize-21-18-9/obstructions.json'))
    mds = []
    for o in obs:
        deg = {}
        for e in o['subedges']:
            for x in e: deg[x] = deg.get(x, 0) + 1
        mds.append(max(deg.values()))
    print('max degrees', mds, 'all >= 4:', all(d >= 4 for d in mds))
