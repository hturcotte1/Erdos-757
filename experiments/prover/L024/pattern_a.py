"""L024 item (iii): the finite (D3) family of pattern (a).
In a minimal counterexample H to KT^{L*} with a degree-3 vertex v such that H - v is connected, (D3) holds and
H - v = F1 + F2 + F3 + g (three disjoint induced pieces of L*, g = {g1,g2,g3} with g_i in V(F_i)), every co-vertex of v
lies in V(F1) u V(F2) u V(F3), W1+W2+W3 >= 36, and (Claim B for X_v) no choice of minimum transversals T_i of F_i has a
union meeting g and the three co-vertex pairs P_1, P_2, P_3 of v.
This script enumerates ALL such configurations (every type triple with W-sum >= 36, every g up to automorphisms of the
pieces, every set of three co-vertex pairs satisfying the degree, linearity and Claim-B conditions), builds H, tests
H in C_3 (own code), computes tau(H), A(H) and an explicit L*-family X of H with DEF_H(X) >= -A(H) (a certificate of
P(H) >= 0), or reports P(H) < 0.
Also (part 0): the pure (D1) case H - v = F (one piece, all six co-vertices in F), as an independent check that does
not use L021 Theorem 7(ii).
Run: timeout 7200 nice -n 10 python3 pattern_a.py [part] > pattern_a_output.txt"""
import sys, itertools, json, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L024')
from hyp24 import *
t0 = time.time()
pieces = load_pieces()
byname = {P['name']: P for P in pieces}
for P in pieces:
    P['aut'] = automorphisms(P['n'], P['edges'])

def orbit_reps(P, cand):
    seen = set(); reps = []
    for x in cand:
        if x in seen: continue
        reps.append(x)
        for a in P['aut']: seen.add(a[x])
    return reps

def maximal(sets):
    sets = sorted(set(sets), key=lambda s: -bin(s).count('1'))
    out = []
    for s in sets:
        if not any(s & t == s for t in out): out.append(s)
    return out

def minimal(sets):
    sets = sorted(set(sets), key=lambda s: bin(s).count('1'))
    out = []
    for s in sets:
        if not any(t & s == t for t in out): out.append(s)
    return out

def hitting_triples(Cs, valid_pairs, k=3):
    """all sets of k pairwise disjoint valid pairs such that every set in Cs contains one of the pairs."""
    sols = set()
    def rec(chosen, used, rem):
        if len(chosen) == k:
            if not rem: sols.add(frozenset(chosen))
            return
        if not rem:
            # every remaining choice of disjoint valid pairs completes a solution
            avail = [p for p in valid_pairs if not p & used]
            for extra in itertools.combinations(avail, k - len(chosen)):
                u = used; ok = True
                for p in extra:
                    if p & u: ok = False; break
                    u |= p
                if ok: sols.add(frozenset(list(chosen) + list(extra)))
            return
        best = None
        for C in rem:
            cnt = [p for p in valid_pairs if p & C == p and not p & used]
            if best is None or len(cnt) < len(best[1]):
                best = (C, cnt)
                if not cnt: return
        for p in best[1]:
            rec(chosen + [p], used | p, [C for C in rem if p & C != p])
    rec([], 0, Cs)
    return sols

def check_H(n, edges, sumtau, members):
    """membership, tau, A, DEF certificate."""
    if not in_C3(n, edges): return dict(inC3=False)
    t = tau(n, edges)
    A = CN * n + CM * len(edges) - CT * t
    res = dict(inC3=True, tau=t, tau_ok=(t == sumtau + 1), A=A)
    if A >= 0:
        res.update(DEF=None, P_lower=A, fam=[]); return res
    D, fam, ncop = def_certificate(n, edges, pieces, -A)
    # independent recomputation of the certificate's value
    if fam:
        Dchk = family_def(n, edges, [(S, w) for (S, w, nm) in fam])
        assert Dchk == D, (Dchk, D)
    res.update(DEF_found=D, P_lower=A + D, fam=[(bin(S).count('1'), nm, S) for (S, w, nm) in fam], copies=ncop)
    return res

out = dict(part0=[], part1=[])
stats = {}
part = sys.argv[1] if len(sys.argv) > 1 else 'all'

# ---------- part 0: (D1) with H - v = F ----------
if part in ('all', '0'):
    tot = dict(configs=0, inC3=0, Pneg=0)
    for P in pieces:
        n0 = P['n']; E0 = P['edges']; d0 = P['deg']
        low = [x for x in range(n0) if d0[x] <= 2]
        inside = set()
        for e in E0:
            for a, b in itertools.combinations(e, 2): inside.add((min(a, b), max(a, b)))
        pairs = [(1 << a) | (1 << b) for a, b in itertools.combinations(low, 2) if (a, b) not in inside]
        mts = P['mts']
        cnt = 0
        for trip in itertools.combinations(pairs, 3):
            if trip[0] & trip[1] or trip[0] & trip[2] or trip[1] & trip[2]: continue
            # Claim B: no minimum transversal of F meets all three pairs
            if any(all(T & p for p in trip) for T in mts): continue
            cnt += 1
            v = n0
            E = list(E0)
            for p in trip:
                a, b = [x for x in range(n0) if p >> x & 1]
                E.append(tuple(sorted((a, b, v))))
            r = check_H(n0 + 1, E, P['tau'], [P['name']])
            tot['configs'] += 1
            if r.get('inC3'):
                tot['inC3'] += 1
                if r['P_lower'] < 0:
                    tot['Pneg'] += 1
                    print('PART0 NEGATIVE', P['name'], E, r, flush=True)
                out['part0'].append(dict(piece=P['name'], edges=E, A=r['A'], tau=r['tau'], P_lower=r['P_lower'],
                                         fam=[(k, nm) for (k, nm, S) in r['fam']]))
        print('part0', P['name'], 'Claim-B triples', cnt, f'[{time.time()-t0:.0f}s]', flush=True)
    print('PART0 TOTAL', tot, flush=True)
    stats['part0'] = tot

# ---------- part 1: (D3) with H - v = F1 + F2 + F3 + g ----------
if part in ('all', '1'):
    classes = sorted(set(P['W'] for P in pieces), reverse=True)
    names_by_W = {w: [P['name'] for P in pieces if P['W'] == w] for w in classes}
    trip_types = []
    for ws in itertools.combinations_with_replacement(classes, 3):
        if sum(ws) >= 36: trip_types.append(ws)
    print('weight triples with sum >= 36:', trip_types, flush=True)
    tot = dict(type_triples=0, g_choices=0, configs=0, inC3=0, tau_ok=0, Pneg=0)
    for ws in trip_types:
        # all multisets of piece classes with these weights
        lists = [names_by_W[w] for w in ws]
        combos = set()
        for c in itertools.product(*lists):
            combos.add(tuple(sorted(c, key=lambda nm: (byname[nm]['W'], nm), reverse=True)))
        for combo in sorted(combos):
            tot['type_triples'] += 1
            Ps = [byname[nm] for nm in combo]
            offs = [0, Ps[0]['n'], Ps[0]['n'] + Ps[1]['n']]
            N = sum(P['n'] for P in Ps)
            E0 = []
            for P, o in zip(Ps, offs):
                E0 += [tuple(x + o for x in e) for e in P['edges']]
            d0 = degrees(N, E0)
            sumtau = sum(P['tau'] for P in Ps)
            MT = [[T << o for T in P['mts']] for P, o in zip(Ps, offs)]
            gcand = [orbit_reps(P, [x for x in range(P['n']) if P['deg'][x] <= 2]) for P in Ps]
            nconf_combo = 0
            for gl in itertools.product(*gcand):
                g = tuple(x + o for x, o in zip(gl, offs))
                tot['g_choices'] += 1
                E1 = E0 + [tuple(sorted(g))]
                d1 = list(d0)
                for x in g: d1[x] += 1
                Lmask = 0
                for x in range(N):
                    if d1[x] <= 2: Lmask |= 1 << x
                inside = set()
                for e in E1:
                    for a, b in itertools.combinations(e, 2): inside.add((min(a, b), max(a, b)))
                low = [x for x in range(N) if Lmask >> x & 1]
                valid = [(1 << a) | (1 << b) for a, b in itertools.combinations(low, 2) if (a, b) not in inside]
                # maximal traces
                Us = set()
                for i0 in range(3):
                    parts = []
                    for i in range(3):
                        if i == i0:
                            parts.append(maximal([T & Lmask for T in MT[i] if T >> g[i] & 1]))
                        else:
                            parts.append(maximal([T & Lmask for T in MT[i]]))
                    for a in parts[0]:
                        for b in parts[1]:
                            for c in parts[2]:
                                Us.add(a | b | c)
                Cs = minimal([Lmask & ~U for U in Us])
                sols = hitting_triples(Cs, valid)
                for sol in sols:
                    v = N
                    E = list(E1)
                    for p in sol:
                        a, b = [x for x in range(N) if p >> x & 1]
                        E.append(tuple(sorted((a, b, v))))
                    tot['configs'] += 1; nconf_combo += 1
                    r = check_H(N + 1, E, sumtau, combo)
                    if not r.get('inC3'): continue
                    tot['inC3'] += 1
                    if r['tau_ok']: tot['tau_ok'] += 1
                    if r['P_lower'] < 0:
                        tot['Pneg'] += 1
                        print('PART1 NEGATIVE', combo, E, r, flush=True)
                    out['part1'].append(dict(types=combo, g=g, edges=E, A=r['A'], tau=r['tau'], P_lower=r['P_lower'],
                                             fam=[(k, nm) for (k, nm, S) in r['fam']]))
            print('part1', combo, 'N', N, 'configs', nconf_combo, 'running', tot, f'[{time.time()-t0:.0f}s]', flush=True)
    print('PART1 TOTAL', tot, flush=True)
    stats['part1'] = tot
json.dump(dict(stats=stats, **out), open(f'/home/user/Erdos-757/experiments/prover/L024/pattern_a_results_{part}.json', 'w'))
print('done', f'[{time.time()-t0:.0f}s]')
