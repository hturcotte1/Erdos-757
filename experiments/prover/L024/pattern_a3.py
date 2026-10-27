"""L024 item (iii), fast exhaustive search (same configuration space as pattern_a.py / pattern_a2.py, different algorithm).
Configuration: pieces F1,F2,F3 (disjoint copies), g = {g1,g2,g3} (g_i in F_i, d_{F_i}(g_i) <= 2), and three pairwise
disjoint co-vertex pairs P1,P2,P3 of vertices of G-degree <= 2 (G = F1+F2+F3+g), no pair inside an edge of G, such that
(Claim B) no choice of minimum transversals T_i of F_i has a union meeting g, P1, P2, P3.
Search (complete; WLOG relabelling of the pairs):
  level 0: U0 = a union of minimum transversals meeting g (largest found); some pair avoids U0, call it P1.
  level 1: U1 = a union meeting g and P1; some other pair avoids U1, call it P2.
  level 2: N = vertices of L lying in NO union of minimum transversals meeting g, P1, P2; P3 must lie in N
           (if no union meets g, P1, P2, every P3 completes a solution).
Every solution is re-verified by brute force over all triples (T1,T2,T3) of minimum transversals.
Then: H in C_3 (own code), tau(H), A(H), an explicit L*-family certificate of DEF, Claim-E tag.
Run: timeout 7000 nice -n 10 python3 pattern_a3.py <mode> > pattern_a3_<mode>_output.txt
modes: poor (the 12 all-non-rich type triples), small (cross-check types also run by pattern_a2.py), richcheck"""
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

def cover_info(MT, Lmask, clauses):
    """MT[i]: min transversals of piece i (global masks).  clauses: list of vertex masks.
    Returns (exists, bestU, unionU): whether some (T1,T2,T3) meets all clauses; a largest such union restricted to
    Lmask among those built from per-pattern largest traces; the union over ALL such (T1,T2,T3) of (T1|T2|T3)&Lmask."""
    k = len(clauses); full = (1 << k) - 1
    groups = []
    for i in range(3):
        best = {}; uni = {}
        for T in MT[i]:
            pat = 0
            for j, c in enumerate(clauses):
                if T & c: pat |= 1 << j
            tr = T & Lmask
            uni[pat] = uni.get(pat, 0) | tr
            if pat not in best or bin(tr).count('1') > bin(best[pat]).count('1'): best[pat] = tr
        groups.append((best, uni))
    exists = False; bestU = None; unionU = 0
    for p1, b1 in groups[0][0].items():
        for p2, b2 in groups[1][0].items():
            p12 = p1 | p2
            for p3, b3 in groups[2][0].items():
                if p12 | p3 == full:
                    exists = True
                    U = b1 | b2 | b3
                    if bestU is None or bin(U).count('1') > bin(bestU).count('1'): bestU = U
                    unionU |= groups[0][1][p1] | groups[1][1][p2] | groups[2][1][p3]
    return exists, bestU, unionU

def brute_B(MT, clauses):
    """True iff NO (T1,T2,T3) meets all clauses."""
    # reduce: for each piece, the distinct patterns
    pats = []
    for i in range(3):
        s = set()
        for T in MT[i]:
            pat = 0
            for j, c in enumerate(clauses):
                if T & c: pat |= 1 << j
            s.add(pat)
        pats.append(s)
    full = (1 << len(clauses)) - 1
    for a in pats[0]:
        for b in pats[1]:
            for c in pats[2]:
                if a | b | c == full: return False
    return True

def solve(Ps, offs, g, MT, Lmask, valid):
    sols = set()
    ex, U0, _ = cover_info(MT, Lmask, [g])
    assert ex
    C0 = Lmask & ~U0
    for P1 in valid:
        if P1 & C0 != P1: continue
        ex1, U1, _ = cover_info(MT, Lmask, [g, P1])
        if not ex1:
            raise RuntimeError('g and one pair not coverable (impossible by L1)')
        C1 = Lmask & ~U1
        for P2 in valid:
            if P2 & C1 != P2 or P2 & P1: continue
            ex2, _, uni = cover_info(MT, Lmask, [g, P1, P2])
            N = Lmask & ~uni if ex2 else Lmask
            for P3 in valid:
                if P3 & N != P3 or P3 & (P1 | P2): continue
                sols.add(frozenset((P1, P2, P3)))
    return sols

def run(TYPES, tag):
    tot = dict(type_triples=0, g_choices=0, configs=0, claimE=0, inC3=0, inC3_claimE=0, tau_ok=0, Pneg=0)
    out = []
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
        piece_of = {}
        for i, (P, o) in enumerate(zip(Ps, offs)):
            for x in range(P['n']): piece_of[x + o] = i
        gcand = [orbit_reps(P, [x for x in range(P['n']) if P['deg'][x] <= 2]) for P in Ps]
        nconf = 0
        for gl in itertools.product(*gcand):
            gt = tuple(x + o for x, o in zip(gl, offs))
            tot['g_choices'] += 1
            g = (1 << gt[0]) | (1 << gt[1]) | (1 << gt[2])
            E1 = E0 + [tuple(sorted(gt))]
            d1 = list(d0)
            for x in gt: d1[x] += 1
            Lmask = 0
            for x in range(N):
                if d1[x] <= 2: Lmask |= 1 << x
            inside = set()
            for e in E1:
                for a, b in itertools.combinations(e, 2): inside.add((min(a, b), max(a, b)))
            low = [x for x in range(N) if Lmask >> x & 1]
            valid = [(1 << a) | (1 << b) for a, b in itertools.combinations(low, 2) if (a, b) not in inside]
            sols = solve(Ps, offs, g, MT, Lmask, valid)
            for sol in sorted(sols, key=lambda s: sorted(s)):
                assert brute_B(MT, [g] + list(sol))
                nconf += 1; tot['configs'] += 1
                meets = [set() for _ in range(3)]
                for j, p in enumerate(sorted(sol)):
                    for x in range(N):
                        if p >> x & 1: meets[piece_of[x]].add(j)
                cE = all(meets[i] for i in range(3)) and all(len(meets[i] | meets[k]) >= 2 for i in range(3) for k in range(i + 1, 3))
                if cE: tot['claimE'] += 1
                v = N; E = list(E1)
                for p in sorted(sol):
                    a, b = [x for x in range(N) if p >> x & 1]
                    E.append(tuple(sorted((a, b, v))))
                n = N + 1
                if not in_C3(n, E):
                    out.append(dict(types=combo, g=gt, pairs=[sorted(x for x in range(N) if p >> x & 1) for p in sorted(sol)], claimE=cE, inC3=False))
                    continue
                tot['inC3'] += 1
                if cE: tot['inC3_claimE'] += 1
                t = tau(n, E)
                if t == sumtau + 1: tot['tau_ok'] += 1
                A = CN * n + CM * len(E) - CT * t
                D, fam, ncop = (0, [], 0) if A >= 0 else def_certificate(n, E, pieces, -A)
                if fam:
                    assert family_def(n, E, [(S, w) for (S, w, nm) in fam]) == D
                if A + D < 0:
                    tot['Pneg'] += 1
                    print('NEGATIVE', combo, gt, sorted(sol), A, D, flush=True)
                out.append(dict(types=combo, g=gt, pairs=[sorted(x for x in range(N) if p >> x & 1) for p in sorted(sol)],
                                claimE=cE, inC3=True, tau=t, A=A, DEF_found=D, P_lower=A + D,
                                family=[(nm, sorted(x for x in range(n) if S >> x & 1)) for (S, w, nm) in fam]))
        print(tag, combo, 'N', N, 'g-orbits', len(list(itertools.product(*gcand))), 'configs', nconf, 'running', tot,
              f'[{time.time()-t0:.0f}s]', flush=True)
    print(tag, 'TOTAL', tot, flush=True)
    return tot, out

E1 = '(3,1,1)#0'; T = lambda k: '(10,7,4)#%d' % k; Q = lambda k: '(8,5,3)#%d' % k
mode = sys.argv[1]
if mode == 'poor':
    TYPES = [(E1, E1, E1), (E1, E1, T(1)), (E1, E1, T(2)), (E1, E1, Q(0)), (E1, E1, Q(1)),
             (E1, T(1), T(1)), (E1, T(1), T(2)), (E1, T(2), T(2)),
             (T(1), T(1), T(1)), (T(1), T(1), T(2)), (T(1), T(2), T(2)), (T(2), T(2), T(2))]
elif mode == 'small':
    TYPES = [(E1, E1, E1), (E1, E1, T(0)), (E1, E1, T(1)), (E1, E1, T(2)), (E1, E1, T(3)), (E1, E1, Q(0)), (E1, E1, Q(1))]
else:
    TYPES = [(E1, E1, T(0)), (E1, E1, T(3))]
    for x, y in itertools.combinations_with_replacement(range(4), 2):
        if 0 in (x, y) or 3 in (x, y): TYPES.append((E1, T(x), T(y)))
    for x, y, z in itertools.combinations_with_replacement(range(4), 3):
        if {x, y, z} & {0, 3}: TYPES.append((T(x), T(y), T(z)))
print('mode', mode, 'types', TYPES, flush=True)
tot, out = run(TYPES, mode)
json.dump(dict(totals=tot, configs=out), open(f'/home/user/Erdos-757/experiments/prover/L024/pattern_a3_{mode}_results.json', 'w'))
print('done', f'[{time.time()-t0:.0f}s]')
