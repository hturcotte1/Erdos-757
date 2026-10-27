"""Referee check of L024 C1/C2: n, m, tau, W, degree sequences, (L1), richness of the 32 pieces (brute force),
plus the same for the stored (17,13,7), (15,11,6), (10,7,4), (8,5,3), (3,1,1) lists and an isomorphism match
between closure_results.json and the stored lists."""
import sys, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L024-round1-fable')
from ref_lib import *
t0 = time.time()
pieces = load_pieces()
rich_claimed = {'(10,7,4)#0', '(10,7,4)#3'} | {'(17,13,7)#%d' % i for i in range(6)} | {'(15,11,6)#%d' % i for i in (4,5,14,15,16,17)}
problems = 0
info = {}
for P in pieces:
    n, E = P['n'], P['edges']
    t = tau_brute(n, E)
    W = -A_val(n, len(E), t)
    mts = min_transversals_brute(n, E, t)
    d = degrees(n, E)
    L1 = all(any(x in T for T in mts) for x in range(n))
    nc = [(x, y) for x, y in itertools.combinations(range(n), 2) if not any(x in T and y in T for T in mts)]
    rich = (len(nc) == 0)
    ok_c3, why = in_C3(n, E)
    conn = connected(n, E)
    s = 3*n + 2*len(E) - 11*t
    # pair-lemma bound on non-co-transversal pairs
    share = set()
    for e in E:
        for a, b in itertools.combinations(e, 2): share.add((a, b))
    bnd = all(d[x] + d[y] - (1 if (x, y) in share else 0) <= (2 if s == 0 else 3) for x, y in nc)
    flag = ''
    if t != P['tau_claimed'] or W != P['W_claimed']: flag += ' TAU/W-MISMATCH'; problems += 1
    if rich != (P['name'] in rich_claimed): flag += ' RICHNESS-MISMATCH'; problems += 1
    if not L1: flag += ' L1-FAILS'; problems += 1
    if not ok_c3 or not conn: flag += ' NOT-IN-C3/conn ' + why; problems += 1
    if not bnd: flag += ' PAIR-LEMMA-BOUND-VIOLATED'; problems += 1
    info[P['name']] = (n, len(E), t)
    print(P['name'], 'n', n, 'm', len(E), 'tau', t, 'W', W, 's', s, 'degseq', ''.join(map(str, sorted(d, reverse=True))),
          '#mt', len(mts), 'L1', L1, 'RICH' if rich else 'poor', 'nc-pairs', nc, flag, flush=True)
print('pieces with maxdeg<=2:', [P['name'] for P in pieces if max(degrees(P['n'], P['edges'])) <= 2])
print('--- stored lists vs closure pieces (isomorphism) ---')
for cell, expect in [('cell_17_13_7.txt', 6), ('cell_15_11_6.txt', 19), ('cell_10_7_4.txt', 4), ('cell_8_5_3.txt', 2), ('cell_3_1_1.txt', 1)]:
    L = read_cell_txt(RICH_IN + cell)
    L3 = [(n, m, t, E) for (n, m, t, E) in L if max(degrees(n, E)) <= 3]
    matched = []
    for (n, m, t, E) in L3:
        tt = tau_brute(n, E); assert tt == t, (cell, t, tt)
        mts = min_transversals_brute(n, E, t)
        nc = [(x, y) for x, y in itertools.combinations(range(n), 2) if not any(x in T and y in T for T in mts)]
        hits = [P['name'] for P in pieces if isomorphic(n, E, P['n'], P['edges'])]
        matched.append(hits)
        print(cell, 'graph', (n, m, t), 'RICH' if not nc else 'poor (%d nc pairs)' % len(nc), 'iso to', hits)
    names = sorted(h for hs in matched for h in hs)
    allnames = sorted(P['name'] for P in pieces if (P['n'], P['m'], P['tau_claimed']) == (L3[0][0], L3[0][1], L3[0][2]))
    print(cell, 'Delta<=3 graphs', len(L3), 'expected', expect, 'each matched exactly one piece:', all(len(h) == 1 for h in matched),
          'all pieces of the cell covered:', names == allnames)
    if len(L3) != expect or not all(len(h) == 1 for h in matched) or names != allnames: problems += 1
print('PROBLEMS', problems, f'[{time.time()-t0:.0f}s]')
