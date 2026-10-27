# Referee round 2 (L017): check the two [unrefereed] observations added to Remark 13.1(ii) against the cited files.
import json, sys, itertools
from collections import Counter
f1 = 'experiments/falsify/i11-structure-lemmas/verified_tight_25_23_11_candidates.json'
d = json.load(open(f1))
gs = d['graphs']
print('(25,23,11) candidates file:', len(gs), 'graphs;', d['filt_summary'][:120])
def canon_invariant(edges):
    # cheap isomorphism invariant: sorted degree sequence + sorted multiset of (deg triple per edge) + 2-step neighbourhood degree profile
    V = sorted({v for e in edges for v in e}); deg = Counter(v for e in edges for v in e)
    inv1 = tuple(sorted(deg[v] for v in V))
    inv2 = tuple(sorted(tuple(sorted(deg[v] for v in e)) for e in edges))
    nb = {v: sorted(deg[u] for e in edges if v in e for u in e if u != v) for v in V}
    inv3 = tuple(sorted(tuple(nb[v]) for v in V))
    return (inv1, inv2, inv3)
def tau_bruteforce(edges, n):
    # exact transversal number by iterative deepening over subsets (n = 25 small enough with pruning by edge-cover branch)
    E = [frozenset(e) for e in edges]
    best = [None]
    def rec(E_left, chosen, k):
        if not E_left: return True
        if k == 0: return False
        e = min(E_left, key=len)
        for v in e:
            if rec([f for f in E_left if v not in f], chosen + [v], k - 1): return True
        return False
    for k in range(0, len(E) + 1):
        if rec(E, [], k): return k
def is_linear(edges):
    return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(edges, 2))
def P3_ok(edges, n):
    # e(S) <= |S| - 2 for all S with |S| >= 2: check via the standard sufficient route (all subsets infeasible at n=25); instead check
    # the necessary-and-cheap part: every union of k edges' vertex sets has size >= k + 2 for k <= 4 (small k only; a sample check)
    E = [set(e) for e in edges]
    for k in range(2, 5):
        for comb in itertools.combinations(E, k):
            S = set().union(*comb)
            if len(S) - 2 < k: return False
    return True
invs = []
for g in gs:
    ed = [tuple(e) for e in g['edges']]
    n = g['n']; m = len(ed)
    deg = Counter(v for e in ed for v in e)
    t = tau_bruteforce(ed, n)
    print('  n=%d m=%d maxdeg=%d linear=%s P3(k<=4)=%s tau=%d slack=%d (file: tau_cpsat=%s maxdeg=%s slack=%s)' % (
        n, m, max(deg.values()), is_linear(ed), P3_ok(ed, n), t, 3*n+2*m-11*t, g.get('tau_cpsat'), g.get('maxdeg'), g.get('slack')))
    invs.append(canon_invariant(ed))
print('  distinct cheap invariants among the %d graphs: %d' % (len(gs), len(set(invs))))
try:
    import networkx as nx
    from networkx.algorithms import isomorphism as iso
    def inc(edges):
        B = nx.Graph()
        for i, e in enumerate(edges):
            B.add_node(('e', i), kind=1)
            for v in e:
                B.add_node(('v', v), kind=0); B.add_edge(('e', i), ('v', v))
        return B
    Bs = [inc([tuple(e) for e in g['edges']]) for g in gs]
    nm = iso.categorical_node_match('kind', 0)
    classes = []
    for i, B in enumerate(Bs):
        for c in classes:
            if nx.is_isomorphic(B, Bs[c[0]], node_match=nm): c.append(i); break
        else: classes.append([i])
    print('  isomorphism classes (networkx VF2 on incidence graphs):', classes, '->', len(classes), 'classes')
except Exception as ex:
    print('  networkx isomorphism unavailable:', ex)
f2 = 'experiments/20261027-0400-realize-21-18-9/results_main_21_18_9.json'
r = json.load(open(f2))
print('(21,18,9) realizability file:', len(r), 'entries; realizable flags:', Counter(str(x.get('realizable')) for x in r),
      '; (n,m) set:', set((x['n'], x['m']) for x in r), '; labellings found:', sum(x.get('realizable_labellings', 0) for x in r))
