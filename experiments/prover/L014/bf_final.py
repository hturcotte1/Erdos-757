"""(L014) Cross-check (e2): brute force for the extension step, independent of ext_d's kill search.
python3 bf_final.py NG TG T d EP SAMPLEFILE EXT_D_BINARY [FULLCHECK_FIRST_K]
For each input line G (NG vertices) of SAMPLEFILE:
 1. tau(G) = TG exactly by pyverify's branching (cover of size TG exists, none of size TG-1);
 2. all TG-covers of G by branching (pyverify.all_covers_exact; complete because tau = TG); for the first K inputs also by
    itertools.combinations over all TG-subsets of the NG vertices (must give the same set);
 3. admissible pairs {a,b}: a < b < NG, not inside an edge of G, G-degrees <= EP;
 4. every d-set of pairwise disjoint admissible pairs (itertools.combinations): H = G + {NG,a,b}; H is a hit iff every TG-cover of G
    is disjoint from some pair (then tau(H) >= T; L012 3.5); otherwise a TG-cover meeting all pairs is an explicit cover of H of size
    TG < T.  The first 20 hits of every input are re-checked by an exact tau computation (pyverify.cover_le(H, T-1) must be False);
 5. the set of hits is compared with `EXT_D NG TG T d EP noprune` run on that single input (HIT lines; edge sets as frozensets);
 6. every hit is classified by pyverify (linear; F7; (P3) for the linear F7-free ones; connected on NG+1 vertices).
Prints one line per input and a SUMMARY."""
import sys, os, subprocess, itertools, re, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyverify as pv
NG, TG, T, d, EP = map(int, sys.argv[1:6]); sample = sys.argv[6]; EXT = sys.argv[7]; K = int(sys.argv[8]) if len(sys.argv) > 8 else 0
tot = dict(inputs=0, equal=0, different=0, hits=0, hits_inC=0, hits_F7=0, hits_P3fail=0, hits_disconnected=0, tau_checked=0, cover_full_checked=0, dsets=0)
for li, line in enumerate(open(sample)):
    a = list(map(int, line.split()))
    if not a: continue
    m = a[0]; G = [tuple(a[1 + 3 * i: 4 + 3 * i]) for i in range(m)]
    assert pv.cover_le(G, TG) and not pv.cover_le(G, TG - 1), 'tau(G) != TG'
    covers = pv.all_covers_exact(G, TG)
    if li < K:
        masks = [sum(1 << v for v in e) for e in G]
        bf = set()
        for S in itertools.combinations(range(NG), TG):
            sm = sum(1 << v for v in S)
            if all(sm & me for me in masks): bf.add(frozenset(S))
        assert bf == covers, 'cover lists differ'; tot['cover_full_checked'] += 1
    deg = [0] * NG
    for e in G:
        for v in e: deg[v] += 1
    inedge = set()
    for e in G:
        for x, y in itertools.combinations(sorted(e), 2): inedge.add((x, y))
    pairs = [(x, y) for x in range(NG) for y in range(x + 1, NG) if deg[x] <= EP and deg[y] <= EP and (x, y) not in inedge]
    cl = list(covers); ALL = (1 << len(cl)) - 1
    kill = []
    for (x, y) in pairs:
        b = 0
        for i, c in enumerate(cl):
            if x not in c and y not in c: b |= 1 << i
        kill.append(b)
    hits = set(); nd = 0
    for S in itertools.combinations(range(len(pairs)), d):
        vs = set()
        for i in S: vs.update(pairs[i])
        if len(vs) != 2 * d: continue
        nd += 1
        acc = 0
        for i in S: acc |= kill[i]
        if acc == ALL:
            H = G + [tuple(sorted((pairs[i][0], pairs[i][1], NG))) for i in S]
            hits.add(frozenset(frozenset(e) for e in H))
    tot['dsets'] += nd
    r = subprocess.run([EXT, str(NG), str(TG), str(T), str(d), str(EP), 'noprune'], input=line, capture_output=True, text=True, check=True)
    eh = set()
    for l in r.stdout.splitlines():
        if l.startswith('HIT:'):
            eh.add(frozenset(frozenset(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)))
    ok = (eh == hits); tot['inputs'] += 1; tot['equal' if ok else 'different'] += 1; tot['hits'] += len(hits)
    for hi, H in enumerate(sorted(hits, key=lambda h: sorted(tuple(sorted(e)) for e in h))):
        E = [tuple(sorted(e)) for e in H]
        if hi < 20:   # redundant exact re-check of tau(H) >= T on the first 20 hits of each input
            assert not pv.cover_le(E, T - 1), 'hit with tau < T'; tot['tau_checked'] += 1
        lin = pv.linear(E); f7 = pv.has_f7(E); p3 = pv.p3(E) if (lin and not f7) else None; cn = pv.connected(E, range(NG + 1))
        tot['hits_F7'] += f7; tot['hits_P3fail'] += (p3 is False); tot['hits_disconnected'] += (not cn)
        if lin and not f7 and p3: tot['hits_inC'] += 1
    print('input %d: covers %d pairs %d dsets %d bf_hits %d ext_d_hits %d %s' % (li, len(cl), len(pairs), nd, len(hits), len(eh), 'EQUAL' if ok else 'DIFFERENT'), flush=True)
print('SUMMARY', ' '.join('%s=%d' % kv for kv in tot.items()))
