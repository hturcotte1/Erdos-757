#!/usr/bin/env python3
"""Referee L016 round 1 (own code): closure test of a stored list cell(n,m,t,D).
For every class X and EVERY vertex w of maximum degree d: tau(X) = t (own), tau(X - w) = t - 1 (own; components' taus add
up), every component K of X - w (isolated vertices included) has slack >= 0, and its type multiset is one of my
decompositions of (n-1, m-d, t-1); every non-trivial component (in canonical form via labelg on the incidence graph) must
occur in the stored list cell(n_K, m_K, tau_K, d) (seeds of L013/L014 or the prover's new lists).
Usage: closure.py n m t D cellfile workdir"""
import sys, os, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_inputs as BI
from mydecomp import decomps

R = '/home/user/Erdos-757/experiments/referee/L016-round1'
LABELG = R + '/bin/labelg'; MYTAU = R + '/bin/mytau'

def taus(graphs):
    """graphs: list of (n, edges) -> list of tau (own C program)."""
    inp = ''.join('%d %s\n' % (len(es), ' '.join('%d %d %d' % e for e in es)) for (n, es) in graphs)
    out = subprocess.run([MYTAU], input=inp.encode(), capture_output=True, check=True).stdout.split()
    return [int(x) for x in out]

def g6_incidence(n, es):
    es = sorted(tuple(sorted(e)) for e in es)
    N = n + len(es); nb = N * (N - 1) // 2; arr = bytearray((nb + 5) // 6)
    for j, e in enumerate(es):
        jj = n + j; base = jj * (jj - 1) // 2
        for v in e:
            p = base + v; arr[p // 6] |= 1 << (5 - p % 6)
    return chr(N + 63) + ''.join(chr(b + 63) for b in arr)

def canon(n, graphs):
    """graphs: list of edge lists on 0..n-1 -> list of labelg canonical strings (incidence graph, vertex cell first)."""
    lines = [g6_incidence(n, es) for es in graphs]
    out = subprocess.run([LABELG, '-q', '-f' + 'a' * n], input=('\n'.join(lines) + '\n').encode(), capture_output=True, check=True).stdout.decode().split()
    assert len(out) == len(graphs)
    return out

def components(nv, es):
    par = list(range(nv))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for (a, b, c) in es:
        par[f(a)] = f(b); par[f(c)] = f(b)
    groups = collections.defaultdict(list)
    for v in range(nv):
        groups[f(v)].append(v)
    comps = []
    for r, vs in groups.items():
        idx = {v: i for i, v in enumerate(sorted(vs))}
        ce = [tuple(sorted(idx[x] for x in e)) for e in es if f(e[0]) == r]
        comps.append((len(vs), ce))
    return comps

def main():
    n, m, t, D = map(int, sys.argv[1:5]); cellfile = sys.argv[5]
    X = [BI.parse_found(l) for l in open(cellfile) if l.startswith('FOUND:')]
    tX = taus([(n, es) for es in X])
    problems = 0
    if any(x != t for x in tX):
        problems += sum(1 for x in tX if x != t); print('tau(X) != t for', sum(1 for x in tX if x != t), 'classes')
    pairs = 0; bytype = collections.defaultdict(list); typecount = collections.Counter(); decset = {}
    recs = []
    for xi, es in enumerate(X):
        deg = [0] * n
        for e in es:
            for v in e:
                deg[v] += 1
        dmax = max(deg)
        for w in range(n):
            if deg[w] != dmax:
                continue
            pairs += 1
            rest = [e for e in es if w not in e]
            relabel = {v: i for i, v in enumerate([u for u in range(n) if u != w])}
            rest = [tuple(relabel[v] for v in e) for e in rest]
            comps = components(n - 1, rest)
            recs.append((xi, w, dmax, comps))
    # taus of all non-trivial components
    flat = [(c[0], c[1]) for r in recs for c in r[3] if c[0] > 1]
    ft = taus(flat)
    k = 0; typed = []
    for (xi, w, dmax, comps) in recs:
        tl = []
        for (nc, ce) in comps:
            if nc == 1:
                tl.append(((1, 0, 0), None))
            else:
                tc = ft[k]; k += 1
                tl.append(((nc, len(ce), tc), ce))
        typed.append((xi, w, dmax, tl))
    for (xi, w, dmax, tl) in typed:
        tsum = sum(ty[2] for ty, _ in tl)
        ms = tuple(sorted(ty for ty, _ in tl))
        key = (n - 1, m - dmax, tsum)
        if key not in decset:
            decset[key] = set(tuple(sorted(d)) for d in decomps(*key))
        if tsum != t - 1:
            problems += 1; print('tau(X-w) != t-1', xi, w, tsum)
        if any(3 * ty[0] + 2 * ty[1] - 11 * ty[2] < 0 for ty, _ in tl):
            problems += 1; print('negative component slack', xi, w, ms)
        if ms not in decset[key]:
            problems += 1; print('type multiset not a decomposition', xi, w, ms)
        typecount[ms] += 1
        for ty, ce in tl:
            if ce is not None:
                bytype[ty].append((ce, xi, w, dmax))
    found_missing = 0
    for ty, items in sorted(bytype.items()):
        dset = sorted(set(it[3] for it in items))
        for d in dset:
            its = [it for it in items if it[3] == d]
            lst = BI.load(ty[0], ty[1], ty[2], d)
            if lst is None:
                problems += len(its); print('NO LIST for type', ty, 'D', d, len(its)); continue
            lcan = set(canon(ty[0], lst))
            assert len(lcan) == len(lst), 'duplicate classes in list %s' % (ty,)
            ccan = canon(ty[0], [it[0] for it in its])
            miss = sum(1 for c in ccan if c not in lcan)
            found_missing += miss; problems += miss
            print('type %s D=%d: %d components, list %d classes, missing %d' % (ty, d, len(its), len(lst), miss))
    print('CLOSURE n=%d m=%d t=%d D=%d classes=%d (class,vertex) pairs=%d problems=%d' % (n, m, t, D, len(X), pairs, problems))
    for ms, c in typecount.most_common():
        print('   X-w type', ms, c)

if __name__ == '__main__':
    main()
