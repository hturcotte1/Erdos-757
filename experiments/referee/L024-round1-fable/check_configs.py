"""Referee check of L024 C4 output: rebuild every configuration of pattern_a3_poor_results.json and re-verify with own code:
(C1) degrees, (C2) linearity of pairs, (C3) Claim B by brute force over all triples of minimum transversals,
C_3 membership (own brute-force tests) against the stored flag, tau = sum tau_i + 1, A, isomorphism to a piece of L*,
and that the stored DEF certificate is a single member covering all of V(H)."""
import sys, json, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L024-round1-fable')
from ref_lib import *
t0 = time.time()
pieces = load_pieces()
byname = {P['name']: P for P in pieces}
for P in pieces:
    P['tau'] = tau_brute(P['n'], P['edges'])
    P['mts'] = min_transversals_brute(P['n'], P['edges'], P['tau'])
D = json.load(open('/home/user/Erdos-757/experiments/prover/L024/pattern_a3_poor_results.json'))
print('stored totals', D['totals'])
cfgs = D['configs']
stats = dict(total=0, c1c2_ok=0, claimB_ok=0, inC3_agree=0, inC3=0, tau_ok=0, iso_piece=0, single_member_all=0, A_ok=0)
by_type = {}
bad = []
for c in cfgs:
    stats['total'] += 1
    Ps = [byname[nm] for nm in c['types']]
    offs = [0, Ps[0]['n'], Ps[0]['n'] + Ps[1]['n']]
    N = sum(P['n'] for P in Ps)
    E = []
    for P, o in zip(Ps, offs):
        E += [tuple(x + o for x in e) for e in P['edges']]
    g = tuple(sorted(c['g']))
    EG = E + [g]
    dG = degrees(N, EG)
    pairs = [tuple(sorted(p)) for p in c['pairs']]
    # C1: g_i in piece i with piece-degree <= 2; co-vertices G-degree <= 2
    piece_of = lambda x: 0 if x < offs[1] else (1 if x < offs[2] else 2)
    c1 = sorted(piece_of(x) for x in g) == [0, 1, 2] and all(degrees(N, E)[x] <= 2 for x in g) and all(dG[x] <= 2 for p in pairs for x in p)
    inside = set()
    for e in EG:
        for a, b in itertools.combinations(sorted(e), 2): inside.add((a, b))
    c2 = all(p not in inside for p in pairs) and len(set(x for p in pairs for x in p)) == 6
    if c1 and c2: stats['c1c2_ok'] += 1
    # C3: Claim B brute force
    MT = [[frozenset(x + o for x in T) for T in P['mts']] for P, o in zip(Ps, offs)]
    clauses = [set(g)] + [set(p) for p in pairs]
    claimB = True
    for T1 in MT[0]:
        for T2 in MT[1]:
            U12 = T1 | T2
            for T3 in MT[2]:
                U = U12 | T3
                if all(U & cl for cl in clauses): claimB = False; break
            if not claimB: break
        if not claimB: break
    if claimB: stats['claimB_ok'] += 1
    v = N
    EH = EG + [tuple(sorted(p + (v,))) for p in pairs]
    n = N + 1
    ok, why = in_C3(n, EH)
    if ok == c['inC3']: stats['inC3_agree'] += 1
    else: bad.append(('inC3 disagreement', c['types'], c['g'], c['pairs'], ok, why, c['inC3']))
    key = tuple(c['types'])
    by_type.setdefault(key, dict(configs=0, inC3=0, A=set(), iso=set(), notC3_why={}))
    by_type[key]['configs'] += 1
    if not ok:
        by_type[key]['notC3_why'][why] = by_type[key]['notC3_why'].get(why, 0) + 1
    if ok:
        stats['inC3'] += 1
        by_type[key]['inC3'] += 1
        t = tau_brute(n, EH)
        sumtau = sum(P['tau'] for P in Ps)
        if t == sumtau + 1: stats['tau_ok'] += 1
        A = A_val(n, len(EH), t)
        by_type[key]['A'].add(A)
        if c.get('A') == A and c.get('tau') == t: stats['A_ok'] += 1
        else: bad.append(('tau/A disagreement', c['types'], c['g'], c['pairs'], t, A, c.get('tau'), c.get('A')))
        hits = [P['name'] for P in pieces if isomorphic(n, EH, P['n'], P['edges'])]
        if len(hits) == 1: stats['iso_piece'] += 1; by_type[key]['iso'].add(hits[0])
        else: bad.append(('not a piece / ambiguous', c['types'], c['g'], c['pairs'], hits))
        fam = c.get('family', [])
        if len(fam) == 1 and sorted(fam[0][1]) == list(range(n)) and (not hits or fam[0][0] == hits[0]):
            stats['single_member_all'] += 1
        else: bad.append(('family not single full member', c['types'], c['g'], c['pairs'], fam, hits))
        if A + byname[hits[0]]['W_claimed'] != 0 if hits else True:
            bad.append(('P != 0', c['types'], A, hits))
print('STATS', stats, f'[{time.time()-t0:.0f}s]')
for k, vv in sorted(by_type.items()):
    print(k, 'configs', vv['configs'], 'inC3', vv['inC3'], 'A values', sorted(vv['A']), 'iso classes', sorted(vv['iso']), 'notC3 reasons', vv['notC3_why'])
print('BAD', len(bad))
for b in bad[:20]: print(b)
