"""Referee (fable): third implementation of the independent exhaustive pattern-(a) search (same mathematics as indep_search2.py,
fully vectorised over (P1,P2,P3) with numpy; written because the machine is heavily loaded).
For each g: for every piece i and minimum transversal T_t of F_i, pattern[t,p1,p2] = [T meets g_i] + 2[T meets P_{p1}] + 4[T meets P_{p2}];
U_i[k][p1,p2] = OR of the low-vertex traces of the T's of piece i with pattern k; present_i[k][p1,p2] = some T has pattern k.
uni[p1,p2] = OR over (k1,k2,k3) with k1|k2|k3 = 7 and all present of U_1[k1]|U_2[k2]|U_3[k3]
          = the set of low vertices lying in some union T1|T2|T3 that meets g, P_{p1}, P_{p2}.
Claim B for {P1,P2,P3} <=> P3 avoids uni[p1,p2].  All triples p1<p2<p3 of pairwise disjoint valid pairs are tested.
Each configuration found is re-verified by brute force over all (T1,T2,T3) and tested for C_3, tau, A, isomorphism to a piece.
Run: timeout 3000 nice -n 10 python3 -I indep_search3.py <mode> > indep_search3_<mode>_output.txt"""
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
ALL = {'small': [(E1, E1, E1), (E1, E1, T(1)), (E1, E1, T(2)), (E1, E1, Q(0)), (E1, E1, Q(1))],
       'mid': [(E1, T(1), T(1)), (E1, T(1), T(2)), (E1, T(2), T(2))],
       'big': [(T(1), T(1), T(1)), (T(1), T(1), T(2)), (T(1), T(2), T(2)), (T(2), T(2), T(2))],
       'rich': [(E1, E1, T(0)), (E1, E1, T(3))]}
ALL['poor'] = ALL['small'] + ALL['mid'] + ALL['big']
ALL['midbig'] = ALL['mid'] + ALL['big']
TYPES = ALL[mode]
COMBOS = [(k1, k2, k3) for k1 in range(8) for k2 in range(8) for k3 in range(8) if (k1 | k2 | k3) == 7]
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
    MTg = [[sum(1 << (x + o) for x in Tm) for Tm in P['mts']] for P, o in zip(Ps, offs)]
    nconf = 0; found = []; gorb = 0
    for gl in itertools.product(*[P['low_reps'] for P in Ps]):
        gorb += 1
        gt = tuple(x + o for x, o in zip(gl, offs))
        EG = E0 + [tuple(sorted(gt))]
        dG = degrees(N, EG)
        low = [x for x in range(N) if dG[x] <= 2]
        lowmask = sum(1 << x for x in low)
        inside = set()
        for e in EG:
            for a, b in itertools.combinations(sorted(e), 2): inside.add((a, b))
        pairs = [(a, b) for a, b in itertools.combinations(low, 2) if (a, b) not in inside]
        Pn = len(pairs)
        if Pn < 3: continue
        pm = np.array([(1 << a) | (1 << b) for a, b in pairs], dtype=np.int64)
        tr = [np.array([Tm & lowmask for Tm in MTg[i]], dtype=np.int64) for i in range(3)]
        hitg = [np.array([(Tm >> gt[i]) & 1 for Tm in MTg[i]], dtype=np.int8) for i in range(3)]
        hitP = [((tr[i][:, None] & pm[None, :]) != 0).astype(np.int8) for i in range(3)]
        U = []; present = []
        for i in range(3):
            pat = hitg[i][:, None, None] + 2 * hitP[i][:, :, None] + 4 * hitP[i][:, None, :]   # (T, P1, P2)
            Ui = np.zeros((8, Pn, Pn), dtype=np.int64); Pr = np.zeros((8, Pn, Pn), dtype=bool)
            for k in range(8):
                msk = (pat == k)
                Pr[k] = msk.any(axis=0)
                Ui[k] = np.bitwise_or.reduce(np.where(msk, tr[i][:, None, None], 0), axis=0)
            U.append(Ui); present.append(Pr)
        uni = np.zeros((Pn, Pn), dtype=np.int64)
        for k1, k2, k3 in COMBOS:
            ok = present[0][k1] & present[1][k2] & present[2][k3]
            if ok.any():
                uni |= np.where(ok, U[0][k1] | U[1][k2] | U[2][k3], 0)
        pa = np.array(pairs)
        Dm = (pa[:, 0][:, None] != pa[:, 0][None, :]) & (pa[:, 0][:, None] != pa[:, 1][None, :]) & \
             (pa[:, 1][:, None] != pa[:, 0][None, :]) & (pa[:, 1][:, None] != pa[:, 1][None, :])
        idx = np.arange(Pn)
        order = (idx[:, None, None] < idx[None, :, None]) & (idx[None, :, None] < idx[None, None, :])
        disj = Dm[:, :, None] & Dm[:, None, :] & Dm[None, :, :]
        avoid = (pm[None, None, :] & uni[:, :, None]) == 0
        sols = np.nonzero(avoid & disj & order)
        for p1, p2, p3 in zip(*sols):
            found.append((gt, (pairs[int(p1)], pairs[int(p2)], pairs[int(p3)]))); nconf += 1
    inC3 = 0; tau_ok = 0; iso_piece = 0; isos = {}; Avals = set(); whys = {}
    for gt, prs in found:
        EG = E0 + [tuple(sorted(gt))]
        clauses = [sum(1 << x for x in gt)] + [(1 << a) | (1 << b) for a, b in prs]
        assert not any(all((T1 | T2 | T3) & c for c in clauses) for T1 in MTg[0] for T2 in MTg[1] for T3 in MTg[2]), 'brute force Claim B failed'
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
json.dump(dict(grand=grand, summary=summary), open(f'/home/user/Erdos-757/experiments/referee/L024-round1-fable/indep_search3_{mode}.json', 'w'), indent=1)
