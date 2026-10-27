"""Referee #3 (round 2): checks of Lemma A+ (case split) and of the W2 statement of 7.3.
Part A (exhaustive, local): for every piece F of L* and every set of three pairwise disjoint nonempty traces
  Q1,Q2,Q3 (sizes 1 or 2; a 2-trace not inside an edge of F (linearity); d_F(u)+[u in a trace] <= 3), the
  H-degrees on F are d_H(u) = d_F(u) + [u in a trace] (4.1). Z = {u: d_H(u)=3}. Classify alpha/beta/gamma/delta.
  Claims tested: gamma never occurs; alpha only for F = E1 (then all traces singletons, all H-degrees 2);
  beta/delta only for |V(F)| >= 8.
Part B (random, structural): random connected linear 3-graphs H with Delta <= 3 built as an apex v over a
  component F of H-v met by all three edges, with extra components D attached through outer co-vertices.
  For each v of degree 3 and each component F of H-v met by all three edges at v: test (4.1), (4.2) and, in
  cases beta/delta, the W2 statements V(H) = V(F) u V(K_w) [u V(K_w')], E(H) = E(F) u E(K_w) [u E(K_w')],
  where K_w is the component of H-w containing v (in L024, F_w = K_w by Lemma A(a)), E(K) = edges of H-w inside V(K).
Run: timeout 1200 nice -n 10 python3 -B check_r2.py > check_r2_output.txt"""
import sys, itertools, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L024-round2-opus')
from rlib2 import *

def classify(Q, Z):
    covs = set().union(*Q)
    if not Z: return 'alpha'
    if any(u not in covs for u in Z): return 'beta'
    hit = [j for j in range(3) if Z & Q[j]]
    return 'gamma' if len(hit) == 1 else 'delta'

def part_a():
    pieces = load_pieces()
    stats = {}
    bad = 0
    for P in pieces:
        n, E = P['n'], P['edges']
        d = degrees(n, E)
        inedge = set()
        for e in E:
            for p in itertools.combinations(e, 2): inedge.add(frozenset(p))
        traces = [frozenset([x]) for x in range(n) if d[x] <= 2]
        traces += [frozenset(p) for p in itertools.combinations(range(n), 2)
                   if frozenset(p) not in inedge and d[p[0]] <= 2 and d[p[1]] <= 2]
        cnt = {'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0}
        for Q in itertools.combinations(traces, 3):
            if Q[0] & Q[1] or Q[0] & Q[2] or Q[1] & Q[2]: continue
            covs = Q[0] | Q[1] | Q[2]
            dH = [d[u] + (1 if u in covs else 0) for u in range(n)]
            if max(dH) > 3: continue
            Z = set(u for u in range(n) if dH[u] == 3)
            c = classify(Q, Z)
            cnt[c] += 1
            if c == 'gamma':
                bad += 1; print('GAMMA OCCURS', P['name'], [sorted(q) for q in Q])
            if c == 'alpha':
                if not (n == 3 and all(len(q) == 1 for q in Q) and all(x == 2 for x in dH)):
                    bad += 1; print('ALPHA NOT E1-HUB', P['name'], [sorted(q) for q in Q], dH)
            if c in ('beta', 'delta') and n < 8:
                bad += 1; print('BETA/DELTA WITH n<8', P['name'])
        stats[P['name']] = cnt
        print('A', P['name'], cnt, flush=True)
    tot = {k: sum(s[k] for s in stats.values()) for k in ('alpha', 'beta', 'gamma', 'delta')}
    print('PART A TOTAL', tot, 'BAD', bad, flush=True)
    return bad

def rand_linear_graph(rng, verts, nedges, E, deg, pairs, tries=200):
    """add up to nedges random edges on vertex list verts to E keeping linearity and Delta <= 3"""
    for _ in range(tries):
        if nedges == 0: break
        if len(verts) < 3: break
        e = tuple(sorted(rng.sample(verts, 3)))
        ps = [frozenset(p) for p in itertools.combinations(e, 2)]
        if any(p in pairs for p in ps) or any(deg[x] >= 3 for x in e): continue
        E.append(e)
        for p in ps: pairs.add(p)
        for x in e: deg[x] += 1
        nedges -= 1

def gen_apex(rng):
    nF = rng.randint(3, 17)
    E = []; deg = {}; pairs = set()
    F = list(range(nF))
    for x in F: deg[x] = 0
    # connected random F: spanning-ish chain of edges, then extras
    rand_linear_graph(rng, F, rng.randint(1, nF), E, deg, pairs)
    nxt = nF
    v = nxt; nxt += 1; deg[v] = 0
    # three edges at v: traces in F (sizes 1 or 2), outer co-vertices in new or shared D's
    Ds = []
    for j in range(3):
        cand = [x for x in F if deg[x] <= 2]
        if not cand: return None
        a = rng.choice(cand)
        if rng.random() < 0.35:
            cand2 = [x for x in F if deg[x] <= 2 and x != a and frozenset((a, x)) not in pairs]
            if not cand2: return None
            b = rng.choice(cand2)
        else:
            if Ds and rng.random() < 0.3:
                D = rng.choice(Ds); cand3 = [x for x in D if deg[x] <= 2 and frozenset((a, x)) not in pairs]
                if not cand3: return None
                b = rng.choice(cand3)
            else:
                size = rng.choice([1, 1, 3, 4, 5, 7])
                D = list(range(nxt, nxt + size)); nxt += size
                for x in D: deg[x] = 0
                rand_linear_graph(rng, D, rng.randint(0, size), E, deg, pairs)
                Ds.append(D); b = rng.choice(D)
        e = tuple(sorted((v, a, b)))
        ps = [frozenset(p) for p in itertools.combinations(e, 2)]
        if any(p in pairs for p in ps) or any(deg[x] >= 3 for x in e): return None
        E.append(e)
        for p in ps: pairs.add(p)
        for x in e: deg[x] += 1
    # extra edges inside F and inside each D to raise degrees
    rand_linear_graph(rng, F, rng.randint(0, nF), E, deg, pairs)
    for D in Ds: rand_linear_graph(rng, D, rng.randint(0, 3), E, deg, pairs)
    n = nxt
    if not is_linear(E) or max(degrees(n, E)) > 3: return None
    if len(components(range(n), E)) != 1: return None
    return n, E

def part_b(trials, seed):
    rng = random.Random(seed)
    st = {'graphs': 0, 'apex_cases': 0, 'alpha': 0, 'beta': 0, 'gamma': 0, 'delta': 0, 'beta_nontrivial': 0, 'delta_nontrivial': 0}
    bad = 0
    for _ in range(trials):
        g = gen_apex(rng)
        if g is None: continue
        n, E = g; st['graphs'] += 1
        d = degrees(n, E)
        for v in range(n):
            if d[v] != 3: continue
            ev = [e for e in E if v in e]
            rest = [x for x in range(n) if x != v]
            for Fset in components(rest, E):
                Q = [frozenset(x for x in e if x in Fset) for e in ev]
                if not all(Q): continue
                st['apex_cases'] += 1
                EF = induced_edges(Fset, E)
                dF = degrees(n, EF)
                cov = set()
                for e in ev: cov |= set(x for x in e if x != v)
                # (4.1)
                for u in Fset:
                    if d[u] != dF[u] + (1 if u in cov else 0):
                        bad += 1; print('4.1 FAILS', n, E, v, u)
                Z = set(u for u in Fset if d[u] == 3)
                c = classify(Q, Z); st[c] += 1
                if c not in ('beta', 'delta'): continue
                def K_of(w):
                    for K in components([x for x in range(n) if x != w], E):
                        if v in K: return K
                Ds = [D for D in components(rest, E) if D != Fset]
                if c == 'beta':
                    w = next(u for u in Z if u not in cov)
                    Ks = [K_of(w)]; ws = [w]
                else:
                    js = [j for j in range(3) if Z & Q[j]]
                    w = next(iter(Z & Q[js[0]])); w2 = next(iter(Z & Q[js[1]]))
                    Ks = [K_of(w), K_of(w2)]; ws = [w, w2]
                # (4.2): every edge at v avoiding w lies inside K_w, and every D containing its outer co-vertex too
                for w, K in zip(ws, Ks):
                    for e in ev:
                        if w in e: continue
                        if not set(e) <= K:
                            bad += 1; print('4.2 edge FAILS', n, E, v, w)
                        for D in Ds:
                            if set(e) & D and not D <= K:
                                bad += 1; print('4.2 D FAILS', n, E, v, w)
                Vcov = set(Fset)
                Ecov = set(EF)
                for w, K in zip(ws, Ks):
                    Vcov |= K
                    Ecov |= set(e for e in E if w not in e and set(e) <= K)
                if Vcov != set(range(n)):
                    bad += 1; print('W2 VERTEX COVER FAILS', c, n, E, v, ws)
                if Ecov != set(E):
                    bad += 1; print('W2 EDGE COVER FAILS', c, n, E, v, ws, sorted(set(E) - Ecov))
                if Ds: st[c + '_nontrivial'] += 1
    print('PART B', st, 'BAD', bad, flush=True)
    return bad

if __name__ == '__main__':
    ba = part_a()
    bb = part_b(int(sys.argv[1]) if len(sys.argv) > 1 else 20000, 1)
    print('ALL BAD', ba + bb)
