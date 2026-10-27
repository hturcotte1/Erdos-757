"""Theorem 1 (i)-(iii) of L020, own code: all minimum transversals, vertex/pair co-transversality
(checked also by direct exact transversal searches, independent of the enumeration), NC pairs,
and every triple of pairwise disjoint 2-sets not inside an edge (coverage; K+v in C for the uncovered)."""
import json, sys, time, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg
CLS = '/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'
cls = json.load(open(CLS))
which = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else range(len(cls))
direct = True
tot_viol = 0
for ci in which:
    t0 = time.time()
    n = cls[ci]['n']; es = [tuple(e) for e in cls[ci]['edges']]
    t = hg.tau_bb(es)
    TL = hg.all_min_transversals(es, t)
    masks = hg.to_masks(es)
    assert len(set(TL)) == len(TL)
    assert all(hg.popcount(T) == t and all(T & e for e in masks) for T in TL)
    d = hg.degrees(n, es)
    B = [0] * n
    for k, T in enumerate(TL):
        for x in hg.bits(T):
            B[x] |= 1 << k
    vert_ok = all(B[x] for x in range(n))
    low = [x for x in range(n) if d[x] <= 2]
    nc = [(x, y) for x, y in itertools.combinations(low, 2) if B[x] & B[y] == 0]
    # independent check by direct searches (no enumeration): vertex x co-transversal iff a transversal of size t contains x
    mism = 0
    if direct and ci in (0, 1, 2):
        for x in range(n):
            if hg.has_transversal_of_size(es, t, forced_in=1 << x) != bool(B[x]):
                mism += 1
        for x, y in itertools.combinations(range(n), 2):
            if hg.has_transversal_of_size(es, t, forced_in=(1 << x) | (1 << y)) != bool(B[x] & B[y]):
                mism += 1
    inside = set()
    for e in es:
        for p in itertools.combinations(sorted(e), 2):
            inside.add(p)
    pairs = [p for p in itertools.combinations(range(n), 2) if p not in inside]
    PB = [B[x] | B[y] for x, y in pairs]
    pm = [(1 << x) | (1 << y) for x, y in pairs]
    P = len(pairs)
    pp_fail = 0
    unc = []
    ntrip = 0
    for i in range(P):
        bi = PB[i]; mi = pm[i]
        for j in range(i + 1, P):
            if pm[j] & mi:
                continue
            bij = bi & PB[j]
            if bij == 0:
                pp_fail += 1
            mij = mi | pm[j]
            for k in range(j + 1, P):
                if pm[k] & mij:
                    continue
                ntrip += 1
                if bij & PB[k] == 0:
                    unc.append((pairs[i], pairs[j], pairs[k]))
    viol = []
    for tr in unc:
        v = n
        es2 = es + [tuple(sorted((v,) + p)) for p in tr]
        if hg.in_C(n + 1, es2):
            t2 = hg.tau_bb(es2)
            viol.append((tr, t2, hg.slack(n + 1, len(es2), t2)))
    tot_viol += len(viol)
    print(f"class {ci}: tau {t}, #min transversals {len(TL)}, all vertices covered {vert_ok}, "
          f"#deg<=2 vertices {len(low)}, NC pairs {len(nc)}, direct-search mismatches {mism if ci in (0,1,2) else 'n/a'}, "
          f"#pairs not inside an edge {P}, #triples examined {ntrip}, pair-pair failures {pp_fail}, uncovered triples {len(unc)}, "
          f"uncovered with K+v in C {len(viol)} {viol[:3]}, secs {time.time()-t0:.1f}", flush=True)
print('TOTAL K+v in C among uncovered triples:', tot_viol)
