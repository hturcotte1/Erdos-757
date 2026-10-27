"""Referee check of Theorem 1 of L020 on the explicit graph K_29 (edges copied from the certificate text).
Own code only (ref3.py).  Usage: python3 verify_k29.py [--p3complete]"""
import sys, time, itertools, json
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-fable')
import ref3 as R

K29_TEXT = """{0,1,14},{1,2,15},{2,16,17},{3,4,13},{3,10,18},{4,11,18},{5,8,9},{5,15,16},{6,7,16},{6,8,17},{7,9,17},{10,11,19},{12,14,15},
{12,18,19},{13,14,19},{20,21,22},{21,25,26},{22,24,27},{23,24,26},{23,25,27},{28,1,12},{28,21,23},{28,0,20}"""

def parse_text(txt):
    txt = txt.replace('\n', '')
    parts = txt.split('},{')
    E = []
    for p in parts:
        p = p.strip('{}')
        E.append(tuple(sorted(int(x) for x in p.split(','))))
    return E

def full_check(n, E, label, p3complete=False, f7brute=False):
    t0 = time.time()
    res = {}
    res['uniform_distinct'] = R.is_3uniform_distinct(n, E)
    d = R.degrees(n, E)
    res['degrees_hist'] = {k: d.count(k) for k in sorted(set(d))}
    res['max_deg'] = max(d)
    res['linear'] = R.is_linear(E)
    res['F7_direct'] = R.contains_F7_direct(n, E)
    if f7brute:
        res['F7_bruteforce'] = R.contains_F7_bruteforce(n, E)
    res['P3_hall'] = R.p3_hall(n, E)
    if p3complete:
        res['P3_complete'] = R.p3_complete(n, E)
    res['connected'] = R.connected(n, E)
    masks = R.edge_masks(E)
    T12 = R.min_transversal(masks, 12)
    res['transversal12'] = None if T12 is None else sorted(i for i in range(n) if (T12 >> i) & 1)
    if T12 is not None:
        assert all(mk & T12 for mk in masks)
        assert bin(T12).count('1') <= 12
    res['exists11'] = R.exists_transversal(masks, 11)
    res['tau'] = R.tau(n, E)
    res['slack'] = 3 * n + 2 * len(E) - 11 * res['tau']
    res['secs'] = round(time.time() - t0, 2)
    print(label, json.dumps(res), flush=True)
    ok = (res['uniform_distinct'] and res['linear'] and not res['F7_direct'] and res['P3_hall'] and res['connected']
          and res['max_deg'] == 3 and res['tau'] == 12 and res['slack'] == 1 and not res['exists11'])
    if f7brute:
        ok = ok and not res['F7_bruteforce']
    if p3complete:
        ok = ok and res['P3_complete']
    return ok, res

def main():
    p3c = '--p3complete' in sys.argv
    E = parse_text(K29_TEXT)
    n = 29
    print('K29 edges', len(E))
    ok, res = full_check(n, E, 'K29', p3complete=p3c, f7brute=True)
    print('K29 main statement OK:', ok)

    # components after deleting v = 28
    n2, E2, keep = R.sub(n, E, [28])
    comps = R.components(n2, E2)
    print('components of K29 - 28 (sizes):', [len(c) for c in comps])
    F_idx = [x for x in range(20)]
    X_idx = [x for x in range(20, 28)]
    EF = [e for e in E if all(x < 20 for x in e)]
    EX = [tuple(x - 20 for x in e) for e in E if all(20 <= x < 28 for x in e)]
    Ev = [e for e in E if 28 in e]
    print('F edges', len(EF), 'X edges', len(EX), 'v edges', Ev)
    tF = R.tau(20, EF); tX = R.tau(8, EX)
    print('tau(F) =', tF, 'slack(F) =', 60 + 2 * len(EF) - 11 * tF, '| tau(X) =', tX, 'slack(X) =', 24 + 2 * len(EX) - 11 * tX)
    print('F in C:', R.is_linear(EF), not R.contains_F7_direct(20, EF), R.p3_hall(20, EF), 'connected', R.connected(20, EF), 'maxdeg', max(R.degrees(20, EF)))
    print('X in C:', R.is_linear(EX), not R.contains_F7_direct(8, EX), R.p3_hall(8, EX), 'connected', R.connected(8, EX), 'maxdeg', max(R.degrees(8, EX)))
    # e-configurations (0;1,12) in F and (20;21,23) in X  (NC pairs: tau(F - x - y) == tau(F) - 1 fails)
    dF = R.degrees(20, EF)
    for (z, a, b) in [(0, 1, 12)]:
        print('F e-config (%d;%d,%d): degrees' % (z, a, b), dF[z], dF[a], dF[b],
              '| {z,a} co-transversal?', R.cotransversal(20, EF, [z, a], tF),
              '| {z,b} co-transversal?', R.cotransversal(20, EF, [z, b], tF),
              '| a,b share an edge?', any(a in e and b in e for e in EF),
              '| z,a,b each co-transversal?', [R.cotransversal(20, EF, [u], tF) for u in (z, a, b)])
    dX = R.degrees(8, EX)
    for (z, a, b) in [(0, 1, 3)]:
        print('X e-config (%d;%d,%d) [labels -20]: degrees' % (z, a, b), dX[z], dX[a], dX[b],
              '| {z,a} co-transversal?', R.cotransversal(8, EX, [z, a], tX),
              '| {z,b} co-transversal?', R.cotransversal(8, EX, [z, b], tX),
              '| a,b share an edge?', any(a in e and b in e for e in EX))
    # (i) every vertex and every pair co-transversal
    t0 = time.time()
    bad_v = [x for x in range(n) if not R.cotransversal(n, E, [x], 12)]
    print('vertices NOT co-transversal:', bad_v, '(%.1fs)' % (time.time() - t0))
    t0 = time.time()
    d = R.degrees(n, E)
    bad_pairs = []
    npairs_low = 0
    for x, y in itertools.combinations(range(n), 2):
        if d[x] <= 2 and d[y] <= 2:
            npairs_low += 1
        if not R.cotransversal(n, E, [x, y], 12):
            bad_pairs.append((x, y, d[x], d[y]))
    print('pairs of degree<=2 vertices:', npairs_low, '| pairs (any degrees) NOT co-transversal:', bad_pairs, '(%.1fs)' % (time.time() - t0))

    # (ii) triple coverage
    t0 = time.time()
    masks = R.edge_masks(E)
    Ts, t = R.all_min_transversals(masks, n)
    print('number of minimum transversals:', len(Ts), 'tau', t, '(%.1fs)' % (time.time() - t0))
    assert len(set(Ts)) == len(Ts)
    for T in Ts:
        assert bin(T).count('1') == t and all(mk & T for mk in masks)
    inedge = set()
    for e in E:
        for x, y in itertools.combinations(e, 2):
            inedge.add((x, y))
    pairs = [(x, y) for x, y in itertools.combinations(range(n), 2) if (x, y) not in inedge]
    print('pairs not inside an edge:', len(pairs))
    # bitmask over transversals: which transversals meet the pair
    pm = []
    for (x, y) in pairs:
        b = 0
        for i, T in enumerate(Ts):
            if (T >> x) & 1 or (T >> y) & 1:
                b |= 1 << i
        pm.append(b)
    uncovered = []
    P = len(pairs)
    t0 = time.time()
    for i in range(P):
        xi, yi = pairs[i]
        for j in range(i + 1, P):
            xj, yj = pairs[j]
            if xj in (xi, yi) or yj in (xi, yi):
                continue
            bij = pm[i] & pm[j]
            if not bij:
                # pair-pair uncovered (should not happen per certificate: K+w(Q1,Q2) would need checking)
                uncovered.append(('PAIRPAIR', pairs[i], pairs[j]))
                continue
            for k in range(j + 1, P):
                xk, yk = pairs[k]
                if xk in (xi, yi, xj, yj) or yk in (xi, yi, xj, yj):
                    continue
                if not (bij & pm[k]):
                    uncovered.append((pairs[i], pairs[j], pairs[k]))
    print('uncovered triples:', len(uncovered), uncovered, '(%.1fs)' % (time.time() - t0))
    # for each uncovered triple: K + v(P1,P2,P3) must be outside C
    viol = 0
    for tr in uncovered:
        if tr[0] == 'PAIRPAIR':
            print('PAIR-PAIR UNCOVERED', tr)
            viol += 1
            continue
        E3 = list(E) + [tuple(sorted((29,) + p)) for p in tr]
        lin = R.is_linear(E3); f7 = R.contains_F7_direct(30, E3); p3 = R.p3_hall(30, E3)
        inC = lin and not f7 and p3
        tt = R.tau(30, E3) if inC else None
        print('  triple', tr, 'K+v: linear', lin, 'F7', f7, 'P3', p3, 'in C', inC, 'tau', tt)
        if inC:
            viol += 1
    print('violators (uncovered admissible triples):', viol)

if __name__ == '__main__':
    main()
