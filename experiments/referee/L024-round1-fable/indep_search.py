"""Referee (fable): independent exhaustive search for pattern (a) configurations (L024 Theorem 4, C4).
Configuration: pieces F1,F2,F3 (disjoint), g = (g1,g2,g3) with g_i in F_i of piece-degree <= 2 (one representative per
Aut(F_i)-orbit, orbits from networkx), three pairwise disjoint pairs of vertices of G-degree <= 2 (G = F1+F2+F3+g), no pair
inside an edge of G, Claim B: no union T1|T2|T3 of minimum transversals meets g and all three pairs.
Method (different from pattern_a3.py): hitting is monotone, so Claim B holds iff no MAXIMAL g-hitting union meets the
three pairs; maximal g-hitting unions = unions of componentwise-maximal traces (trace = T restricted to low vertices plus
g_i) that meet g.  For each p1, bad[p2,p3] = exists u: U_u meets p1,p2,p3 is a boolean matrix product (numpy float32).
All triples p1<p2<p3 of disjoint valid pairs are examined; nothing is skipped.
Then every configuration found is rebuilt, tested for C_3 (own brute force), tau (brute force), A, isomorphism to a piece.
Run: timeout 3000 nice -n 10 python3 -I indep_search.py [mode] > indep_search_output.txt"""
import sys, itertools, time, json
import numpy as np
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L024-round1-fable')
from ref_lib import *
t0 = time.time()
pieces = load_pieces()
byname = {P['name']: P for P in pieces}
for P in pieces:
    P['tau'] = tau_brute(P['n'], P['edges'])
    P['mts'] = min_transversals_brute(P['n'], P['edges'], P['tau'])
    P['deg'] = degrees(P['n'], P['edges'])
    P['W'] = -A_val(P['n'], P['m'], P['tau'])
    P['orbits'] = automorphism_orbits(P['n'], P['edges'])
    P['low_reps'] = sorted(min(o) for o in P['orbits'] if P['deg'][min(o)] <= 2)
E1 = '(3,1,1)#0'; T = lambda k: '(10,7,4)#%d' % k; Q = lambda k: '(8,5,3)#%d' % k
mode = sys.argv[1] if len(sys.argv) > 1 else 'poor'
if mode == 'poor':
    TYPES = [(E1, E1, E1), (E1, E1, T(1)), (E1, E1, T(2)), (E1, E1, Q(0)), (E1, E1, Q(1)),
             (E1, T(1), T(1)), (E1, T(1), T(2)), (E1, T(2), T(2)),
             (T(1), T(1), T(1)), (T(1), T(1), T(2)), (T(1), T(2), T(2)), (T(2), T(2), T(2))]
elif mode == 'small':
    TYPES = [(E1, E1, E1), (E1, E1, T(1)), (E1, E1, T(2)), (E1, E1, Q(0)), (E1, E1, Q(1))]
elif mode == 'mid':
    TYPES = [(E1, T(1), T(1)), (E1, T(1), T(2)), (E1, T(2), T(2))]
elif mode == 'big':
    TYPES = [(T(1), T(1), T(1)), (T(1), T(1), T(2)), (T(1), T(2), T(2)), (T(2), T(2), T(2))]
elif mode == 'rich':  # cross-check of Lemma 2 on the two rich (10,7,4) pieces with two E1's
    TYPES = [(E1, E1, T(0)), (E1, E1, T(3))]
# sanity on the type list: all non-rich (by own richness computation) and sum W >= 36
def rich(P):
    return all(any(x in Tm and y in Tm for Tm in P['mts']) for x, y in itertools.combinations(range(P['n']), 2))
nonrich = [P['name'] for P in pieces if not rich(P)]
if mode == 'poor':
    combos = set()
    for a, b, c in itertools.combinations_with_replacement(sorted(nonrich), 3):
        if byname[a]['W'] + byname[b]['W'] + byname[c]['W'] >= 36: combos.add(tuple(sorted((a, b, c))))
    print('own list of non-rich type triples with sum W >= 36:', len(combos), 'equal to the 12 of the certificate:',
          combos == set(tuple(sorted(t)) for t in TYPES), flush=True)
print('low-degree orbit representatives:', {P['name']: P['low_reps'] for P in pieces if P['name'] in set(x for t in TYPES for x in t)}, flush=True)
grand = dict(types=0, g_orbits=0, configs=0, inC3=0, tau_ok=0, iso_piece=0, Pneg=0)
summary = {}
for combo in TYPES:
    Ps = [byname[nm] for nm in combo]
    offs = [0, Ps[0]['n'], Ps[0]['n'] + Ps[1]['n']]
    N = sum(P['n'] for P in Ps)
    E0 = []
    for P, o in zip(Ps, offs):
        E0 += [tuple(x + o for x in e) for e in P['edges']]
    sumtau = sum(P['tau'] for P in Ps)
    nconf = 0; found = []
    gorb = 0
    for gl in itertools.product(*[P['low_reps'] for P in Ps]):
        gorb += 1
        gt = tuple(x + o for x, o in zip(gl, offs))
        EG = E0 + [tuple(sorted(gt))]
        dG = degrees(N, EG)
        low = [x for x in range(N) if dG[x] <= 2]
        lowset = set(low)
        inside = set()
        for e in EG:
            for a, b in itertools.combinations(sorted(e), 2): inside.add((a, b))
        pairs = [(a, b) for a, b in itertools.combinations(low, 2) if (a, b) not in inside]
        Pn = len(pairs)
        if Pn < 3: continue
        # maximal traces per piece (restricted to low vertices plus g_i)
        Umax = []
        per_piece = []
        for i, (P, o) in enumerate(zip(Ps, offs)):
            keep = lowset | {gt[i]}
            traces = set(frozenset(x + o for x in Tm if (x + o) in keep) for Tm in P['mts'])
            mx = [t for t in traces if not any(t < t2 for t2 in traces)]
            per_piece.append(mx)
        for t1 in per_piece[0]:
            for t2 in per_piece[1]:
                for t3 in per_piece[2]:
                    U = t1 | t2 | t3
                    if U & set(gt): Umax.append(U)
        assert Umax, 'no g-hitting union: impossible by (L1)'
        Un = len(Umax)
        Hp = np.zeros((Un, Pn), dtype=np.float32)
        for u, U in enumerate(Umax):
            for p, (a, b) in enumerate(pairs):
                if a in U or b in U: Hp[u, p] = 1.0
        # disjointness matrix
        pa = np.array(pairs)
        Dm = (pa[:, 0][:, None] != pa[:, 0][None, :]) & (pa[:, 0][:, None] != pa[:, 1][None, :]) & \
             (pa[:, 1][:, None] != pa[:, 0][None, :]) & (pa[:, 1][:, None] != pa[:, 1][None, :])
        triu = np.triu(np.ones((Pn, Pn), dtype=bool), k=1)
        for p1 in range(Pn - 2):
            w = Hp[:, p1]
            if not w.any():
                bad = np.zeros((Pn, Pn), dtype=bool)
            else:
                M1 = Hp * w[:, None]
                bad = (M1.T @ Hp) > 0.5
            ok = (~bad) & Dm & Dm[p1][:, None] & Dm[p1][None, :] & triu
            ok[:p1 + 1, :] = False; ok[:, :p1 + 1] = False
            for p2, p3 in zip(*np.nonzero(ok)):
                found.append((gt, (pairs[p1], pairs[int(p2)], pairs[int(p3)])))
                nconf += 1
    # verify every configuration found: Claim B by brute force, C_3, tau, A, isomorphism
    inC3 = 0; tau_ok = 0; iso_piece = 0; isos = {}; Avals = set(); whys = {}
    for gt, prs in found:
        EG = E0 + [tuple(sorted(gt))]
        MT = [[frozenset(x + o for x in Tm) for Tm in P['mts']] for P, o in zip(Ps, offs)]
        clauses = [set(gt)] + [set(p) for p in prs]
        assert not any(all((T1 | T2 | T3) & c for c in clauses) for T1 in MT[0] for T2 in MT[1] for T3 in MT[2]), 'brute force Claim B failed'
        v = N; EH = EG + [tuple(sorted(p + (v,))) for p in prs]; n = N + 1
        ok, why = in_C3(n, EH)
        if not ok:
            whys[why] = whys.get(why, 0) + 1; continue
        inC3 += 1
        t = tau_bb(n, EH)
        if t == sumtau + 1: tau_ok += 1
        A = A_val(n, len(EH), t); Avals.add(A)
        hits = [P['name'] for P in pieces if isomorphic(n, EH, P['n'], P['edges'])]
        if len(hits) == 1:
            iso_piece += 1; isos[hits[0]] = isos.get(hits[0], 0) + 1
            if A + byname[hits[0]]['W'] < 0: grand['Pneg'] += 1; print('NEGATIVE P', combo, gt, prs)
        else:
            print('NOT A PIECE', combo, gt, prs, 'A', A, flush=True)
    grand['types'] += 1; grand['g_orbits'] += gorb; grand['configs'] += nconf; grand['inC3'] += inC3
    grand['tau_ok'] += tau_ok; grand['iso_piece'] += iso_piece
    summary[str(combo)] = dict(N=N, g_orbits=gorb, configs=nconf, inC3=inC3, tau_ok=tau_ok, iso_piece=iso_piece, iso_classes=isos, A=sorted(Avals), notC3=whys)
    print(combo, 'N', N, 'g-orbits', gorb, 'configs', nconf, 'inC3', inC3, 'tau_ok', tau_ok, 'iso to piece', iso_piece, 'classes', isos,
          'A', sorted(Avals), 'not-C3 reasons', whys, f'[{time.time()-t0:.0f}s]', flush=True)
print('GRAND', grand, f'[{time.time()-t0:.0f}s]')
json.dump(dict(grand=grand, summary=summary), open(f'/home/user/Erdos-757/experiments/referee/L024-round1-fable/indep_search_{mode}.json', 'w'), indent=1)
