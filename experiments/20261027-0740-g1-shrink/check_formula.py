"""Numerical check of the sub-extension identity (L022 Step 2.0):
 s(H[V(F)+v+Q]) = s_F + 3(|Q|+1) + 2(k+k') - 11 t,   t = tau(B) - tau(F),
with tau(B) computed by BRUTE FORCE (smallest vertex set meeting all edges, enumerating subsets by size).
Instances: stored (D1) patterns of E1, (8,5,3)#0, (10,7,4)#1, (15,11,6)#0 (all Q' subsets); also with an extra edge g inside Q'.
Also checks the coverage rule  t = 0  iff some minimum transversal of F meets all traces of the included edges."""
import itertools, json, sys
from g1lib import *
from d1 import parts_of, build

def tau_brute(n, em):
    for r in range(n + 1):
        for T in itertools.combinations(range(n), r):
            tm = 0
            for x in T: tm |= 1 << x
            if all(e & tm for e in em): return r

PI = {P.name: P for P in load_pieces()}
d = json.load(open('d1_results.json'))
out = []; bad = 0
for name, maxp in (('(3,1,1)#0', 4), ('(8,5,3)#0', 6), ('(10,7,4)#1', 4), ('(15,11,6)#0', 2)):
    P = PI[name]; sF = slack(P.n, P.m, P.tau)
    minT = min_transversals(masks(P.edges), P.tau)
    for r in d['survivors'][name][:maxp]:
        traces = [tuple(q) for q in r['traces']]; k = r['k']
        n, edges, ved, outer = build(P, traces, k)
        for rr in range(len(outer) + 1):
            for Qp in itertools.combinations(outer, rr):
                Qs = set(Qp)
                inc = [(q, o, e) for (q, o, e) in ved if set(o) <= Qs]
                Uv = list(range(P.n + 1)) + list(Qp)
                nn, ee = induced(n, edges, Uv)
                assert len(ee) == P.m + len(inc)
                tauB = tau_brute(nn, masks(ee))
                # formula
                tms = [sum(1 << x for x in q) for (q, o, e) in inc]
                t = 0 if (not inc or (all(tms) and any(all(T & tm for tm in tms) for T in minT))) else 1
                sform = sF + 3 * (len(Qp) + 1) + 2 * len(inc) - 11 * t
                sact = slack(nn, len(ee), tauB)
                ok = (tauB == P.tau + t) and (sform == sact)
                bad += (not ok)
                out.append((name, traces, list(Qp), nn, len(ee), tauB, P.tau + t, sact, sform, ok))
        print(name, traces, 'checked all Q subsets; running bad =', bad, flush=True)
# extra edge variant: E1 pattern (1,1,1) with g = the three outer vertices
P = PI['(3,1,1)#0']
n, edges, ved, outer = build(P, [(0,), (1,), (2,)], 3)
Uv = list(range(P.n + 1)) + outer; nn, ee = induced(n, edges, Uv); ee2 = ee + [tuple(Uv.index(x) for x in outer)]
tb = tau_brute(nn, masks(ee2)); sf = slack(P.n, P.m, P.tau) + 3 * 4 + 2 * (3 + 1) - 11 * (tb - P.tau)
print('E1 + 3 edges + extra edge g on the 3 outer vertices: n', nn, 'm', len(ee2), 'tau(brute)', tb, 'slack', slack(nn, len(ee2), tb), 'formula', sf)
bad += (slack(nn, len(ee2), tb) != sf)
json.dump(dict(rows=out, bad=bad, n_checked=len(out)), open('check_formula_results.json', 'w'))
print('TOTAL checked', len(out), 'mismatches', bad)
