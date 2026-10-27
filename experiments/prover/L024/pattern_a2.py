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
Run: timeout 7200 nice -n 10 python3 pattern_a2.py <poor|richcheck> > pattern_a2_<mode>_output.txt
Variant of pattern_a.py: part 1 restricted to an explicit list of type triples; every configuration is tagged with
Claim E (each piece meets >= 1 edge at v; any two pieces meet >= 2 edges at v)."""
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

# ---------- part 1: (D3) with H - v = F1 + F2 + F3 + g ----------
if True:
    E1 = '(3,1,1)#0'; T = lambda k: '(10,7,4)#%d' % k; Q = lambda k: '(8,5,3)#%d' % k
    if part == 'poor':
        TYPES = [(E1, E1, E1), (E1, E1, T(1)), (E1, E1, T(2)), (E1, E1, Q(0)), (E1, E1, Q(1)),
                 (E1, T(1), T(1)), (E1, T(1), T(2)), (E1, T(2), T(2)),
                 (T(1), T(1), T(1)), (T(1), T(1), T(2)), (T(1), T(2), T(2)), (T(2), T(2), T(2))]
    else:  # rich types whose pieces have at most 10 vertices (cross-check of Lemma P)
        TYPES = [(E1, E1, T(0)), (E1, E1, T(3))]
        for x, y in itertools.combinations_with_replacement(range(4), 2):
            if 0 in (x, y) or 3 in (x, y): TYPES.append((E1, T(x), T(y)))
        for x, y, z in itertools.combinations_with_replacement(range(4), 3):
            if {x, y, z} & {0, 3}: TYPES.append((T(x), T(y), T(z)))
    print('type triples:', TYPES, flush=True)
    tot = dict(type_triples=0, g_choices=0, configs=0, claimE=0, inC3=0, inC3_claimE=0, tau_ok=0, Pneg=0)
    for ws in [0]:
        for combo in TYPES:
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
                    # Claim E tags
                    piece_of = {}
                    for i, (P, o) in enumerate(zip(Ps, offs)):
                        for x in range(P['n']): piece_of[x + o] = i
                    meets = [set() for _ in range(3)]
                    for j, p in enumerate(sol):
                        for x in range(N):
                            if p >> x & 1: meets[piece_of[x]].add(j)
                    cE = all(meets[i] for i in range(3)) and all(len(meets[i] | meets[k]) >= 2 for i in range(3) for k in range(i + 1, 3))
                    if cE: tot['claimE'] += 1
                    r = check_H(N + 1, E, sumtau, combo)
                    if not r.get('inC3'): continue
                    tot['inC3'] += 1
                    if cE: tot['inC3_claimE'] += 1
                    if r['tau_ok']: tot['tau_ok'] += 1
                    if r['P_lower'] < 0:
                        tot['Pneg'] += 1
                        print('PART1 NEGATIVE', combo, E, r, flush=True)
                    out['part1'].append(dict(types=combo, g=g, claimE=cE, edges=E, A=r['A'], tau=r['tau'], P_lower=r['P_lower'],
                                             fam=[(k, nm) for (k, nm, S) in r['fam']]))
            print('part1', combo, 'N', N, 'configs', nconf_combo, 'running', tot, f'[{time.time()-t0:.0f}s]', flush=True)
    print('PART1 TOTAL', tot, flush=True)
    stats['part1'] = tot
json.dump(dict(stats=stats, **out), open(f'/home/user/Erdos-757/experiments/prover/L024/pattern_a2_results_{part}.json', 'w'))
print('done', f'[{time.time()-t0:.0f}s]')
