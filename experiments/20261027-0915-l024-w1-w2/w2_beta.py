"""W2 case (beta): H = {v} u F_v u F_w, F_v = P1 (v not in it), w in F_v with d_{P1}(w) = 3 not a co-vertex of v, F_w = P2 containing v
(d_{P2}(v) = 3, all three edges at v inside P2), S = V(F_v) n V(F_w) = union of components of P1 - w and of P2 - v (isomorphic as
induced sub-hypergraphs), H = P1 glued to P2 along S, every edge at v meets S.  P1, P2 range over ALL pieces of L* with >= 8 vertices
(rich ones included; |F_w| >= |F_v| not imposed); n <= 31 and n >= 25 are NOT imposed (counts by n are reported)."""
import sys, itertools, json, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2')
from w2lib import *
t0 = time.time()
pieces = load_pieces()
big = [P for P in pieces if P['n'] >= 8]
stats = dict(pairs=0, glue_candidates=0, trace_ok=0, struct_ok=0, n_le_31=0, n_ge_25_le_31=0, inC3=0, A_nonneg=0, A_neg=0, Pneg=0,
             inC3_n_ge_25=0, A_neg_n_ge_25=0)
byn = {}
out = []
for P1 in big:
    for w in range(P1['n']):
        if P1['deg'][w] != 3: continue
        C1 = comps_minus(P1['n'], P1['edges'], w)
        for P2 in big:
            for v in range(P2['n']):
                if P2['deg'][v] != 3: continue
                stats['pairs'] += 1
                C2 = comps_minus(P2['n'], P2['edges'], v)
                e_v = [e for e in P2['edges'] if v in e]
                for r2 in range(1, len(C2) + 1):
                    for I2 in itertools.combinations(range(len(C2)), r2):
                        S2 = frozenset().union(*[C2[i] for i in I2])
                        if not all(any(x in S2 for x in e if x != v) for e in e_v): continue   # traces nonempty
                        for r1 in range(1, len(C1) + 1):
                            for I1 in itertools.combinations(range(len(C1)), r1):
                                S1 = frozenset().union(*[C1[i] for i in I1])
                                if len(S1) != len(S2): continue
                                if len(inner_edges(P1['edges'], S1)) != len(inner_edges(P2['edges'], S2)): continue
                                for phi in isos(P2['edges'], S2, P1['edges'], S1):
                                    stats['glue_candidates'] += 1
                                    stats['trace_ok'] += 1
                                    # build H: P1 vertices 0..n1-1, other P2 vertices new
                                    mp = dict(phi); nxt = P1['n']
                                    for x in range(P2['n']):
                                        if x not in mp: mp[x] = nxt; nxt += 1
                                    n = nxt
                                    Eset = set(tuple(sorted(e)) for e in P1['edges'])
                                    Eset |= set(tuple(sorted(mp[y] for y in e)) for e in P2['edges'])
                                    E = sorted(Eset)
                                    V1 = set(range(P1['n'])); V2 = set(mp.values())
                                    vv = mp[v]
                                    ok = (len(inner_edges(E, V1)) == P1['m'] and len(inner_edges(E, V2)) == P2['m'])
                                    cv = comps_of(n, E, {vv}); cw = comps_of(n, E, {w})
                                    ok = ok and (frozenset(V1) in cv) and (frozenset(V2) in cw)
                                    ok = ok and not any(w in e for e in E if vv in e)    # w is not a co-vertex of v
                                    if not ok: continue
                                    stats['struct_ok'] += 1
                                    if n > 31: continue
                                    stats['n_le_31'] += 1
                                    byn[n] = byn.get(n, 0) + 1
                                    if n >= 25: stats['n_ge_25_le_31'] += 1
                                    rec = dict(P1=P1['name'], w=w, P2=P2['name'], v=v, S2=sorted(S2), phi=phi, edges=E)
                                    before = stats['inC3']; beforeA = stats['A_neg']
                                    p = evaluate(n, E, pieces, stats, 'beta', rec)
                                    if stats['inC3'] > before:
                                        if n >= 25: stats['inC3_n_ge_25'] += 1
                                        if stats['A_neg'] > beforeA and n >= 25: stats['A_neg_n_ge_25'] += 1
                                        out.append(rec)
                                        if p is not None and p < 0: print('NEGATIVE P', rec, flush=True)
    print(P1['name'], 'done', stats, f'{time.time()-t0:.0f}s', flush=True)
print('TOTAL', stats, 'by_n', dict(sorted(byn.items())), f'{time.time()-t0:.0f}s')
json.dump(dict(stats=stats, by_n=byn, configs=out), open('/home/user/Erdos-757/experiments/20261027-0915-l024-w1-w2/w2_beta_results.json', 'w'))
