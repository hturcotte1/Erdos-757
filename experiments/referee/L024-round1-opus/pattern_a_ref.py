"""Referee's independent enumeration of pattern (a) / (D3) configurations of L024 Theorem 4.

Configuration: G = F1 + F2 + F3 (disjoint pieces of L*) + g, g = {g1,g2,g3}, g_i in V(F_i), d_{F_i}(g_i) <= 2;
H = G + v + three edges {v} u P_j, P_1,P_2,P_3 pairwise disjoint 2-sets of vertices of G-degree <= 2, no P_j inside an
edge of G; Claim B: no choice of minimum transversals T_i of F_i with T_1 u T_2 u T_3 meeting g, P_1, P_2, P_3.

Search (own design): with C = candidate co-vertices, the family of restricted unions U n C (U a union of minimum
transversals meeting g) is reduced to its inclusion-maximal members; a pair P 'kills' U if P n U = empty; a solution is a
triple of pairwise disjoint pairs killing every maximal restricted union.  All solutions are found by the three-level
branching on 'the pair that kills the first not-yet-killed union' (complete; see review), deduplicated as frozensets,
and every solution is re-verified by brute force over all triples of (unrestricted) minimum transversals.

usage: python3 pattern_a_ref.py <mode> [--all-g]
  mode = poor  : the 12 non-rich type triples of L024 Step 6.2
         rich10: all type triples with sum W >= 36 containing a rich piece, pieces with <= 10 vertices
  --all-g: do not reduce g by automorphisms (default: one g per orbit of Aut(F1) x Aut(F2) x Aut(F3))
"""
import sys, json, time
from itertools import combinations, combinations_with_replacement, product
from rlib import *

t0 = time.time()
pieces = load_pieces()
P = {name: (n, E) for name, n, E, rec in pieces}
W = {name: rec['W'] for name, n, E, rec in pieces}
MT = {}
for name, (n, E) in P.items():
    MT[name] = min_transversals(n, E)
RICH = set()
for name, (n, E) in P.items():
    t, mts = MT[name]
    if all(any((T >> x & 1) and (T >> y & 1) for T in mts) for x, y in combinations(range(n), 2)):
        RICH.add(name)
AUT = {}


def orbits(name):
    n, E = P[name]
    if name not in AUT:
        AUT[name] = automorphisms(n, E)
    auts = AUT[name]
    seen, orbs = set(), []
    for x in range(n):
        if x in seen:
            continue
        o = sorted(set(a[x] for a in auts))
        seen.update(o)
        orbs.append(o)
    return orbs


def maximal(sets):
    sets = sorted(set(sets), key=lambda s: -bin(s).count('1'))
    out = []
    for s in sets:
        if not any((s | t) == t for t in out):
            out.append(s)
    return out


def run_type(types, all_g=False):
    offs, Eall, nG = [], [], 0
    for nm in types:
        n, E = P[nm]
        offs.append(nG)
        Eall += [tuple(x + nG for x in e) for e in E]
        nG += n
    tau_sum = sum(MT[nm][0] for nm in types)
    mts = [[T << offs[i] for T in MT[nm][1]] for i, nm in enumerate(types)]
    dF = [degs(*P[nm]) for nm in types]
    gcands = []
    for i, nm in enumerate(types):
        if all_g:
            reps = [x for x in range(P[nm][0]) if dF[i][x] <= 2]
        else:
            reps = [o[0] for o in orbits(nm) if dF[i][o[0]] <= 2]
        gcands.append([x + offs[i] for x in reps])
    stats = dict(g_choices=0, configs=0, inC3=0, tau_ok=0, in_Lstar=0, not_in_Lstar_inC3=0, need2_zero_events=0)
    found = []
    for g in product(*gcands):
        stats['g_choices'] += 1
        gE = tuple(sorted(g))
        EG = Eall + [gE]
        d = degs(nG, EG)
        C = [x for x in range(nG) if d[x] <= 2]
        Cmask = sum(1 << x for x in C)
        inedge = set()
        for e in EG:
            for p in combinations(e, 2):
                inedge.add(p)
        pairs = [(a, b) for a, b in combinations(C, 2) if (a, b) not in inedge]
        pm = [(1 << a) | (1 << b) for a, b in pairs]
        gmask = sum(1 << x for x in gE)
        # restricted traces per piece: all, and those meeting g_i
        R_all = [maximal([T & Cmask for T in mts[i]]) for i in range(3)]
        R_g = [maximal([T & Cmask for T in mts[i] if T & gmask]) for i in range(3)]
        U = []
        for i in range(3):
            fac = [R_all[j] if j != i else R_g[j] for j in range(3)]
            for a, b, c in product(*fac):
                U.append(a | b | c)
        U = maximal(U)
        K = len(U)
        ALL = (1 << K) - 1
        kappa = []
        for m in pm:
            k = 0
            for idx, u in enumerate(U):
                if not (u & m):
                    k |= 1 << idx
            kappa.append(k)
        avoid = [[] for _ in range(K)]
        for pi, k in enumerate(kappa):
            kk = k
            while kk:
                low = kk & -kk
                avoid[low.bit_length() - 1].append(pi)
                kk ^= low
        sols = set()
        if K == 0:
            raise RuntimeError('no union meets g?')
        u0 = min(range(K), key=lambda u: len(avoid[u]))
        for p1 in avoid[u0]:
            need1 = ALL & ~kappa[p1]
            assert need1 != 0  # a single pair never kills every union ((L1))
            # choose the not-yet-killed union with fewest killers
            u1 = min((u for u in range(K) if need1 >> u & 1), key=lambda u: len(avoid[u]))
            for p2 in avoid[u1]:
                if pm[p2] & pm[p1]:
                    continue
                need2 = need1 & ~kappa[p2]
                if need2 == 0:
                    stats['need2_zero_events'] += 1
                    for p3 in range(len(pairs)):
                        if pm[p3] & (pm[p1] | pm[p2]):
                            continue
                        sols.add(frozenset((p1, p2, p3)))
                    continue
                low = need2 & -need2
                u2 = low.bit_length() - 1
                for p3 in avoid[u2]:
                    if pm[p3] & (pm[p1] | pm[p2]):
                        continue
                    if kappa[p3] & need2 == need2:
                        sols.add(frozenset((p1, p2, p3)))
        for s in sols:
            trip = [pairs[i] for i in sorted(s)]
            # brute-force re-verification of Claim B over all triples of minimum transversals
            clauses = [gmask] + [(1 << a) | (1 << b) for a, b in trip]
            bad = False
            for T1 in mts[0]:
                for T2 in mts[1]:
                    for T3 in mts[2]:
                        Un = T1 | T2 | T3
                        if all(Un & cl for cl in clauses):
                            bad = True
                            break
                    if bad:
                        break
                if bad:
                    break
            assert not bad, ('Claim B violated?', types, g, trip)
            # (C1),(C2) re-check
            vs = [x for pr in trip for x in pr]
            assert len(set(vs)) == 6 and all(d[x] <= 2 for x in vs)
            v = nG
            EH = EG + [tuple(sorted((v, a, b))) for a, b in trip]
            nH = nG + 1
            stats['configs'] += 1
            inc3 = in_C3(nH, EH)
            rec = dict(types=types, g=list(gE), pairs=trip, inC3=inc3)
            # Claim E on subfamilies of X_v = {F1,F2,F3} with E*_H = {g, e1, e2, e3}
            pmask = [sum(1 << x for x in range(offs[i], offs[i] + P[types[i]][0])) for i in range(3)]
            Estar = [gmask] + [(1 << a) | (1 << b) for a, b in trip]
            cE = True
            for r in (1, 2, 3):
                for Y in combinations(range(3), r):
                    vy = 0
                    for i in Y:
                        vy |= pmask[i]
                    if sum(1 for e in Estar if e & vy) < r + 1:
                        cE = False
            rec['claimE'] = cE
            stats['claimE'] = stats.get('claimE', 0) + cE
            stats['claimE_and_rich'] = stats.get('claimE_and_rich', 0) + (cE and any(t in RICH for t in types))
            if inc3:
                stats['inC3'] += 1
                t = tau_bb(nH, EH)
                rec['tau'] = t
                if t == tau_sum + 1:
                    stats['tau_ok'] += 1
                m = len(EH)
                rec['cell'] = (nH, m, t)
                rec['A'] = 27 * nH + 35 * m - 132 * t
                iso = [name for name, (n2, E2) in P.items() if isomorphic(nH, EH, n2, E2)]
                rec['iso'] = iso
                if iso:
                    stats['in_Lstar'] += 1
                else:
                    stats['not_in_Lstar_inC3'] += 1
            found.append(rec)
    return stats, found


def type_list(mode):
    names = list(P.keys())
    if mode == 'poor':
        NR = ['(3,1,1)#0', '(8,5,3)#0', '(8,5,3)#1', '(10,7,4)#1', '(10,7,4)#2'] + \
             [nm for nm in names if nm.startswith('(15,11,6)') and nm not in RICH]
        # all multisets of 3 non-rich pieces with sum W >= 36
        out = [t for t in combinations_with_replacement(NR, 3) if sum(W[x] for x in t) >= 36]
        return out
    if mode == 'rich10':
        small = [nm for nm in names if P[nm][0] <= 10]
        out = [t for t in combinations_with_replacement(small, 3)
               if sum(W[x] for x in t) >= 36 and any(x in RICH for x in t)]
        return out
    raise ValueError(mode)


if __name__ == '__main__':
    mode = sys.argv[1]
    all_g = '--all-g' in sys.argv
    TL = type_list(mode)
    print('mode', mode, 'all_g', all_g, 'type triples', len(TL), flush=True)
    tot = {}
    allrecs = []
    for types in TL:
        st, recs = run_type(list(types), all_g)
        n = 1 + sum(P[x][0] for x in types)
        print(n, types, st, 'cells', sorted(set(tuple(r['cell']) for r in recs if r['inC3'])),
              'iso', sorted(set(i for r in recs if r['inC3'] for i in r['iso'])), 'elapsed %.0f' % (time.time() - t0), flush=True)
        for k, v in st.items():
            tot[k] = tot.get(k, 0) + v
        allrecs += recs
    print('TOTAL', tot, flush=True)
    json.dump(allrecs, open('pattern_a_ref_%s%s.json' % (mode, '_allg' if all_g else ''), 'w'))
