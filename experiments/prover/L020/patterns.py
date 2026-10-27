"""L020 sanity check of Theorem B4 (the degree-3 vertex lemma for a graph K with slack <= 1) on every stored connected
class-C graph K with Delta(K) <= 3 and slack 0 or 1 (all have <= 26 vertices, so I11 holds for every member of C with
<= n(K) vertices by L016, and the hypotheses of B4 hold).  Exact integer arithmetic.
For every vertex v of degree 3: G = K - v; checks tau(G) = tau(K) - 1, the number of isolated vertices, the number r of
non-trivial components, the distribution pattern of the three co-vertex pairs, and that the pattern is one of those
allowed by B4 ((a), (b), (e), (f) without isolated vertex; (i-..) with one), and evaluates the equivalent conditions.
Usage: python3 patterns.py <cellfile> ...   (formats as in roles.py)"""
import sys, os, itertools, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017')
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp
from roles import read_any, in_C

def comp_data(K_edges, vs):
    """component on vertex list vs: relabelled edges, tau, min transversals (as sets of original labels)."""
    S = set(vs); es = hyp.induced(K_edges, S)
    n, res, idx = hyp.relabel(vs, es)
    Ts, t = hyp.all_min_transversals(hyp.masks(res))
    inv = {i: v for v, i in idx.items()}
    Tsets = [frozenset(inv[i] for i in range(n) if (T >> i) & 1) for T in Ts]
    return dict(vs=vs, edges=es, n=n, m=len(es), tau=t, slack=3*n+2*len(es)-11*t, Ts=Tsets)

def main(paths):
    tally = collections.Counter(); fails = []
    for path in paths:
        for (n, es) in read_any(path):
            deg = hyp.degrees(n, es)
            if max(deg) > 3: continue
            tK = hyp.tau(n, es); sK = 3*n + 2*len(es) - 11*tK
            if sK > 1: continue
            tally['K'] += 1
            for v in range(n):
                if deg[v] != 3: continue
                tally['v'] += 1
                ev = [e for e in es if v in e]
                P = [tuple(x for x in e if x != v) for e in ev]
                rest = [x for x in range(n) if x != v]
                Ges = [e for e in es if v not in e]
                tG = hyp.tau_masks(hyp.masks(Ges))
                if tG != tK - 1: fails.append(('tauG', path, v)); continue
                comps = hyp.components(rest, Ges)
                iso = [c[0] for c in comps if len(c) == 1]
                big = [c for c in comps if len(c) > 1]
                if len(iso) > 1 or (iso and sK != 1): fails.append(('iso', path, v)); continue
                cd = [comp_data(es, c) for c in big]
                if iso and any(c['slack'] != 0 for c in cd): fails.append(('iso-slack', path, v)); continue
                where = {}
                for i, c in enumerate(cd):
                    for x in c['vs']: where[x] = i
                # live parts
                L = [[x for x in p if x in where] for p in P]
                r = len(cd)
                full_in = collections.Counter(where[p[0]] for p, l in zip(P, L) if len(l) == 2 and where[p[0]] == where[p[1]])
                key = None
                if r == 1:
                    key = 'a' if not iso else 'iso-r1'
                elif not iso:
                    types = []
                    for p in P:
                        types.append('s' if where[p[0]] != where[p[1]] else 'in%d' % where[p[0]])
                    ins = [t for t in types if t != 's']
                    if r == 2:
                        if len(set(ins)) < len(ins): key = 'two-pairs-in-one(c)'
                        elif len(ins) == 0: key = 'b'
                        elif len(ins) == 2: key = 'e'
                        elif len(ins) == 1: key = 'f'
                    else:
                        key = 'r%d-noiso' % r
                else:
                    key = 'iso-r%d' % r
                    if any(v2 >= 2 for v2 in full_in.values()): key += '-two-full-pairs-in-one'
                tally['pattern ' + key] += 1
                # record slacks / cells of components for the pattern
                tally['cells %s %s' % (key, sorted((c['n'], c['m'], c['tau'], c['slack']) for c in cd))] += 1
                if key in ('two-pairs-in-one(c)',) or key.startswith('r3-noiso') or key.endswith('two-full-pairs-in-one'):
                    fails.append(('forbidden pattern ' + key, path, v))
                # pattern conditions
                def cotr(c, X):
                    return any(set(X) <= T for T in c['Ts'])
                if key == 'b':
                    for c in cd:
                        att = [x for p in P for x in p if where[x] == cd.index(c)]
                        ok = all(not cotr(c, (x, y)) for x, y in itertools.combinations(att, 2))
                        if not ok: fails.append(('b-cond', path, v))
                    tally['b: components slacks %s' % sorted(c['slack'] for c in cd)] += 1
                if key == 'f':
                    # the pair inside a component
                    pin = [p for p in P if where[p[0]] == where[p[1]]][0]
                    i1 = where[pin[0]]; c1 = cd[i1]; c2 = cd[1 - i1]
                    others = [p for p in P if p != pin]
                    ce = [x for p in others for x in p if where[x] == i1]
                    df = [x for p in others for x in p if where[x] != i1]
                    cond1 = not any((T & set(pin)) and (T & set(ce)) for T in c1['Ts'])
                    cond2 = not cotr(c2, df)
                    if not (cond1 and cond2): fails.append(('f-cond', path, v))
                    nn = c1['n']; idx = {x: i for i, x in enumerate(c1['vs'])}
                    es2 = [tuple(idx[x] for x in e) for e in c1['edges']] + [(nn, idx[pin[0]], idx[pin[1]]), (nn, idx[ce[0]], idx[ce[1]])]
                    if in_C(nn + 1, es2): fails.append(('f-T2', path, v))
                    tally['f: slack F1 %d, F2 cell %s' % (c1['slack'], (c2['n'], c2['m'], c2['tau'], c2['slack']))] += 1
                if key == 'e':
                    tally['e: components %s' % sorted((c['n'], c['m'], c['tau'], c['slack']) for c in cd)] += 1
        print(os.path.basename(path), 'done', dict(K=tally['K'], v=tally['v']), 'fails so far', len(fails), flush=True)
    for k in sorted(tally): print('  ', k, tally[k])
    print('FAILS', len(fails), fails[:20])

if __name__ == '__main__':
    main(sys.argv[1:])
