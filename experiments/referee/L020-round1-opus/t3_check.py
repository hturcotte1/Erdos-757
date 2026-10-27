"""Theorem 3 of L020 checked with own code at every degree-3 vertex of given near-tight graphs.
Usage: python3 t3_check.py <file> [sample_size seed]   (file: cell list 'n m t edges' or the K29 json)"""
import sys, json, itertools, random, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
from roles_check import read_cell


class Comp:
    def __init__(self, vs, es):
        self.vs = vs
        self.n, self.es, self.idx = hg.relabel(vs, es)
        self.t = hg.tau_bb(self.es)
        self.m = len(self.es)
        self.s = hg.slack(self.n, self.m, self.t)
        self.TL = hg.all_min_transversals(self.es, self.t) if self.m else [0]
        self.B = {}
        for v in vs:
            b = 0
            li = self.idx[v]
            for k, T in enumerate(self.TL):
                if T >> li & 1:
                    b |= 1 << k
            self.B[v] = b
        self.deg = {v: 0 for v in vs}
        for e in es:
            for x in e:
                self.deg[x] += 1
        self.share = set()
        for e in es:
            for p in itertools.combinations(sorted(e), 2):
                self.share.add(p)

    def cot(self, *xs):  # co-transversal
        b = -1
        for x in xs:
            b &= self.B[x]
        return b != 0

    def nc(self, x, y):
        return self.deg[x] <= 2 and self.deg[y] <= 2 and not self.cot(x, y)

    def meets_both(self, Q1, Q2):
        return ((self.B[Q1[0]] | self.B[Q1[1]]) & (self.B[Q2[0]] | self.B[Q2[1]])) != 0


def check_vertex(n, es, tK, sK, v, stats, deep_pairs=False):
    fails = []
    P = [tuple(x for x in e if x != v) for e in es if v in e]
    assert len(P) == 3
    six = [x for p in P for x in p]
    if len(set(six)) != 6:
        fails.append('not distinct')
    dK = hg.degrees(n, es)
    rest = [x for x in range(n) if x != v]
    esG = [e for e in es if v not in e]
    dG = hg.degrees(n, esG)
    for u in six:
        if dG[u] != dK[u] - 1 or dG[u] not in (0, 1, 2):
            fails.append('deg')
    for p in P:
        if any(p[0] in e and p[1] in e for e in esG):
            fails.append('pair inside edge')
    comps = hg.components(rest, esG)
    Y = [vs[0] for vs, ce in comps if not ce]
    F = [Comp(vs, ce) for vs, ce in comps if ce]
    tG = sum(c.t for c in F)
    sG = sum(c.s for c in F) + 3 * len(Y)
    if tG != tK - 1:
        fails.append('tau(K-v) != tau(K)-1')
    if sG != sK + 2:
        fails.append('s(G) != s(K)+2')
    # (ii)
    if set(Y) != set(u for u in six if dK[u] == 1):
        fails.append('Y != co-vertices of degree 1')
    if len(Y) > 1:
        fails.append('|Y|>1')
    if Y and not (sK == 1 and all(c.s == 0 for c in F)):
        fails.append('Y nonempty but not (s=1, all tight)')
    for c in F:
        if not (0 <= c.s <= 3) or c.n > n - 1 or max(c.deg.values()) > 3 or not any(u in c.B for u in six):
            fails.append('component property')
        if not all(c.B[x] for x in c.vs):
            fails.append('free choice fails')
        # pair lemma on all NC pairs of the component
        low = [x for x in c.vs if c.deg[x] <= 2]
        for x, y in itertools.combinations(low, 2):
            if not c.cot(x, y):
                rv = [u for u in c.vs if u not in (x, y)]
                ce2 = [e for e in esG if e[0] in c.B and x not in e and y not in e]
                nn, cer, _ = hg.relabel(rv, ce2)
                t2 = hg.tau_bb(cer)
                dpart = sum(1 for e in esG if e[0] in c.B and (x in e or y in e))
                s2 = hg.slack(nn, len(cer), t2)
                if not (t2 == c.t - 1 and s2 == c.s + 5 - 2 * dpart and s2 >= 0):
                    fails.append('pair lemma')
        if deep_pairs:
            # pair richness: all disjoint 2-sets not inside an edge; uncovered ones must give F+w not in C
            prs = [p for p in itertools.combinations(c.vs, 2) if p not in c.share]
            for Q1, Q2 in itertools.combinations(prs, 2):
                if set(Q1) & set(Q2):
                    continue
                if not c.meets_both(Q1, Q2):
                    w = n + 1
                    ce = [e for e in esG if e[0] in c.B] + [tuple(sorted((w,) + Q1)), tuple(sorted((w,) + Q2))]
                    nn, cer, _ = hg.relabel(c.vs + [w], ce)
                    if hg.in_C(nn, cer):
                        fails.append('pair richness')
    # (*) : no min transversal of G meets the three pairs   <=> tau(K) = tau(G)+1 (checked above); also directly:
    comp_of = {}
    for i, c in enumerate(F):
        for x in c.vs:
            comp_of[x] = i
    r = len(F)
    # pattern classification
    if not Y:
        typ = []
        for p in P:
            ci = [comp_of[p[0]], comp_of[p[1]]]
            typ.append(('in', ci[0]) if ci[0] == ci[1] else ('split',))
        ins = [t[1] for t in typ if t[0] == 'in']
        if r >= 2 and len(ins) != len(set(ins)):
            fails.append('two pairs in one component with r>=2')
        if r > 2:
            fails.append('r>2 without isolated vertex')
        if r == 1:
            pat = 'a'
        else:
            nsplit = sum(1 for t in typ if t[0] == 'split')
            pat = {3: 'b', 1: 'e', 2: 'f'}.get(nsplit, '?')
            if pat == 'b':
                c1 = F[0]; c2 = F[1]
                xs = [p[0] if comp_of[p[0]] == 0 else p[1] for p in P]
                ys = [p[1] if comp_of[p[0]] == 0 else p[0] for p in P]
                ok = all(c1.nc(a, b) for a, b in itertools.combinations(xs, 2)) and \
                    all(c2.nc(a, b) for a, b in itertools.combinations(ys, 2))
                if not ok:
                    fails.append('(b) condition')
            elif pat == 'e':
                # P_i inside F1, P_j inside F2, the split pair {e,f}
                pin = [p for p, t in zip(P, typ) if t[0] == 'in']
                psp = [p for p, t in zip(P, typ) if t[0] == 'split'][0]
                ok = True
                for p in pin:
                    c = F[comp_of[p[0]]]
                    z = psp[0] if comp_of[psp[0]] == comp_of[p[0]] else psp[1]
                    ok &= c.nc(z, p[0]) and c.nc(z, p[1]) and (tuple(sorted(p)) not in c.share)
                if not ok:
                    fails.append('(e) condition')
            elif pat == 'f':
                pin = [p for p, t in zip(P, typ) if t[0] == 'in'][0]
                i1 = comp_of[pin[0]]
                c1 = F[i1]; c2 = F[1 - i1]
                sp = [p for p, t in zip(P, typ) if t[0] == 'split']
                ce_ = [p[0] if comp_of[p[0]] == i1 else p[1] for p in sp]
                df = [p[1] if comp_of[p[0]] == i1 else p[0] for p in sp]
                ok = all(c1.nc(x, y) for x in pin for y in ce_) and c2.nc(df[0], df[1])
                # moreover F1 + w(P1,{c,e}) not in C
                w = n + 1
                ce = [e for e in esG if e[0] in c1.B] + [tuple(sorted((w,) + tuple(pin))), tuple(sorted((w,) + tuple(ce_)))]
                nn, cer, _ = hg.relabel(c1.vs + [w], ce)
                if hg.in_C(nn, cer):
                    ok = False
                if not ok:
                    fails.append('(f) condition')
            else:
                fails.append('unknown pattern')
    else:
        y = Y[0]
        P3 = [p for p in P if y in p][0]
        f = P3[0] if P3[1] == y else P3[1]
        others = [p for p in P if y not in p]
        if dK[f] not in (2, 3):
            fails.append('d(f)')
        if r > 3:
            fails.append('r>3')
        if r == 1:
            pat = 'i1'
            c = F[0]
            # no min transversal of F1 meets P1, P2 and contains f
            b = c.B[f] & (c.B[others[0][0]] | c.B[others[0][1]]) & (c.B[others[1][0]] | c.B[others[1][1]])
            if b:
                fails.append('(i1) condition')
        else:
            typ = []
            for p in others:
                typ.append(('in', comp_of[p[0]]) if comp_of[p[0]] == comp_of[p[1]] else ('split',))
            ins = [t[1] for t in typ if t[0] == 'in']
            if len(ins) == 2 and ins[0] == ins[1]:
                fails.append('P1,P2 in one component with r>=2')
            pat = 'i%d' % r
            # generic check of the stated conditions via the targets P1, P2, {f}
            cf = F[comp_of[f]]
            if r == 2:
                if typ[0][0] == 'in' and typ[1][0] == 'in':  # (i2-1)
                    pa = [p for p, t in zip(others, typ) if t[1] == comp_of[f]][0]
                    ok = cf.nc(pa[0], f) and cf.nc(pa[1], f)
                    pat = 'i2-1'
                elif typ[0][0] == 'split' and typ[1][0] == 'split':  # (i2-4)
                    pa, pc = others
                    a = pa[0] if comp_of[pa[0]] == comp_of[f] else pa[1]; b = pa[1] if a == pa[0] else pa[0]
                    c = pc[0] if comp_of[pc[0]] == comp_of[f] else pc[1]; d = pc[1] if c == pc[0] else pc[0]
                    co = F[comp_of[b]]
                    ok = cf.nc(f, a) and cf.nc(f, c) and co.nc(b, d)
                    pat = 'i2-4'
                else:
                    pin = [p for p, t in zip(others, typ) if t[0] == 'in'][0]
                    psp = [p for p, t in zip(others, typ) if t[0] == 'split'][0]
                    c1 = F[comp_of[pin[0]]]
                    c = psp[0] if comp_of[psp[0]] == comp_of[pin[0]] else psp[1]
                    d = psp[1] if c == psp[0] else psp[0]
                    if comp_of[f] == comp_of[pin[0]]:  # (i2-2)
                        ok = c1.nc(pin[0], f) and c1.nc(pin[1], f)
                        pat = 'i2-2'
                    else:  # (i2-3)
                        c2 = F[comp_of[d]]
                        ok = c1.nc(pin[0], c) and c1.nc(pin[1], c) and c2.nc(d, f)
                        pat = 'i2-3'
                if not ok:
                    fails.append('(%s) condition' % pat)
            else:  # r == 3: (i3)
                pin = [p for p, t in zip(others, typ) if t[0] == 'in']
                if len(pin) != 1 or comp_of[pin[0][0]] != comp_of[f]:
                    fails.append('(i3) shape')
                else:
                    ok = cf.nc(pin[0][0], f) and cf.nc(pin[0][1], f)
                    if not ok:
                        fails.append('(i3) condition')
    stats[pat] = stats.get(pat, 0) + 1
    return fails, pat, [(c.n, c.m, c.t, c.s) for c in F], len(Y)


if __name__ == '__main__':
    path = sys.argv[1]
    deep = '--deep' in sys.argv
    args = [a for a in sys.argv[2:] if a != '--deep']
    if path.endswith('.json'):
        L = [(c['n'], c['m'], c['tau'], [tuple(e) for e in c['edges']]) for c in json.load(open(path))]
    else:
        L = [g for g in read_cell(path) if max(hg.degrees(g[0], g[3])) <= 3]
    if args:
        k, seed = int(args[0]), int(args[1])
        random.seed(seed)
        if k < len(L):
            L = random.sample(L, k)
    stats = {}
    nf = 0
    nv = 0
    t0 = time.time()
    combos = {}
    for n, m, t, es in L:
        tt = hg.tau_bb(es)
        assert tt == t
        s = hg.slack(n, m, t)
        d = hg.degrees(n, es)
        for v in range(n):
            if d[v] != 3:
                continue
            nv += 1
            fails, pat, cells, ny = check_vertex(n, es, t, s, v, stats, deep_pairs=deep)
            key = (pat, tuple(sorted(cells)), ny)
            combos[key] = combos.get(key, 0) + 1
            if fails:
                nf += 1
                print('FAIL', path, es, v, fails)
    print(path.split('/')[-1], 'graphs', len(L), 'degree-3 vertices', nv, 'patterns', dict(sorted(stats.items())),
          'failures', nf, f'{time.time()-t0:.1f}s')
    for k_, c in sorted(combos.items(), key=lambda z: -z[1])[:12]:
        print('   ', k_, c)
