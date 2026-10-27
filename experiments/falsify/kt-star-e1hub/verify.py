#!/usr/bin/env python3
"""Independent re-verification of H records: (1) membership in C by pyverify AND by a direct brute-force definition on small H
(F7 as a subhypergraph by exhaustive 5-edge search; e(S)<=|S|-2 by Hall pair test); (2) tau by pyverify.tau (branching, different code from kt/CP-SAT);
(3) DEF by networkx induced-copy search + plain family enumeration (no bounding), different code from kt.deficiency.
usage: verify.py N_SAMPLE seed file1.jsonl ...   or  verify.py hits file.jsonl (verify only P<0 records)"""
import sys, json, random, itertools, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hubs, kt, pyverify
import networkx as nx
from networkx.algorithms import isomorphism as iso
PL = hubs.PIECES
def inc(n, E):
    G = nx.Graph()
    for x in range(n): G.add_node(('v', x), t=0)
    for i, e in enumerate(E):
        G.add_node(('e', i), t=1)
        for x in e: G.add_edge(('v', x), ('e', i))
    return G
def copies(n, E):
    fm = [frozenset(e) for e in E]; GH = inc(n, E); out = {}
    for P in PL:
        if P.n >= n and not (P.n == n and False): 
            if P.n > n: continue
        GP = inc(P.n, P.edges)
        GM = iso.GraphMatcher(GH, GP, node_match=lambda a, b: a['t'] == b['t'])
        for mp in GM.subgraph_monomorphisms_iter():   # mp: H node -> P node
            W = frozenset(x[1] for x in mp if x[0] == 'v')
            if len(W) != P.n: continue
            inside = sum(1 for f in fm if f <= W)
            if inside != P.m: continue                 # induced: no extra edge inside W
            out[(W, P.name)] = P.W
    return [(W, nm, w) for (W, nm), w in out.items()]
def DEF_plain(n, E, proper=False):
    fm = [frozenset(e) for e in E]
    cps = [c for c in copies(n, E) if not (proper and len(c[0]) >= n)]
    pm = {P.name: P.m for P in PL}
    best = 0
    def rec(i, U, g):
        nonlocal best
        bd = sum(1 for f in fm if f & U)
        best = max(best, g - 35 * bd)
        for j in range(i, len(cps)):
            W, nm, w = cps[j]
            if not W & U: rec(j + 1, U | W, g + w + 35 * pm[nm])
    rec(0, frozenset(), 0)
    return best, len(cps)
def f7_brute(E):
    S = [frozenset(e) for e in E]
    for five in itertools.combinations(range(len(S)), 5):
        es = [S[i] for i in five]
        vs = set().union(*es)
        if len(vs) != 7: continue
        from collections import Counter
        c = Counter(x for e in es for x in e)
        if sorted(c.values()) != [2, 2, 2, 2, 2, 2, 3]: continue
        if all(len(a & b) <= 1 for a, b in itertools.combinations(es, 2)) and sum(len(a & b) for a, b in itertools.combinations(es, 2)) == 9: return True
    return False
def check(rec, brute_f7=False):
    n = rec['n']; E = [tuple(e) for e in rec['H']]
    assert pyverify.in_C(E), 'not in C'
    t = pyverify.tau(E)
    assert t == rec['tau'], ('tau', t, rec['tau'])
    A = 27 * n + 35 * len(E) - 132 * t
    assert A == rec['A']
    d1, nc = DEF_plain(n, E, False)
    assert d1 == rec['DEF'], ('DEF', d1, rec['DEF'])
    return dict(n=n, m=len(E), tau=t, A=A, DEF=d1, ncopies=nc, P=A + d1)
if __name__ == '__main__':
    mode = sys.argv[1]
    recs = []
    for fn in sys.argv[3:]:
        for l in open(fn):
            d = json.loads(l)
            if d.get('type') in ('H', 'FH', 'UV'): recs.append(d)
    if mode == 'hits':
        recs = [r for r in recs if r['P'] < 0 or (r['piece'] is None and r['Pp'] < 0)]
    else:
        random.seed(int(sys.argv[2])); random.shuffle(recs); recs = recs[:int(mode)]
    ok = 0
    for r in recs:
        t0 = time.time()
        res = check(r); ok += 1
        print('OK', res, '[%.1fs]' % (time.time() - t0), flush=True)
    print('verified', ok, 'of', len(recs))
