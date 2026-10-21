#!/usr/bin/env python3
"""Referee L016 round 1: brute-force validation of bin/myext on small random 3-graphs (own code).
For random linear 3-graphs G on NG <= 10 vertices: tau(G) by brute force; all d-sets of pairwise disjoint admissible pairs;
tau(X) by brute force; F7 by 5-edge subsets; (P3) over all vertex subsets; connectivity; max degree.
Compares the counters sol/f7free/inC/conn and the set of printed X with myext."""
import itertools, random, subprocess, sys

MYEXT = sys.argv[1]
NTRIALS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 1)

def tau(n, edges):
    for k in range(0, n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if all(s & set(e) for e in edges):
                return k
    return None

def has_f7(edges):
    for F in itertools.combinations(edges, 5):
        vs = {}
        for e in F:
            for v in e:
                vs[v] = vs.get(v, 0) + 1
        if len(vs) == 7 and sorted(vs.values()) == [2, 2, 2, 2, 2, 2, 3]:
            return True
    return False

def p3(n, edges):
    for k in range(2, n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if sum(1 for e in edges if set(e) <= s) > k - 2:
                return False
    return True

def conn(n, edges):
    adj = {v: set() for v in range(n)}
    for e in edges:
        for a in e:
            for b in e:
                if a != b:
                    adj[a].add(b)
    seen = {0}; st = [0]
    while st:
        v = st.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w); st.append(w)
    return len(seen) == n

def rand_linear(n, mtarget):
    edges = []
    pairs = set()
    tries = 0
    while len(edges) < mtarget and tries < 2000:
        tries += 1
        e = tuple(sorted(rng.sample(range(n), 3)))
        ps = {(e[0], e[1]), (e[0], e[2]), (e[1], e[2])}
        if ps & pairs:
            continue
        pairs |= ps
        edges.append(e)
    return edges

bad = 0
tot = dict(sol=0, f7free=0, inC=0, conn=0)
for trial in range(NTRIALS):
    NG = rng.randint(5, 9)
    mt = rng.randint(1, NG)
    G = rand_linear(NG, mt)
    if not G:
        continue
    tG = tau(NG, G)
    TG = tG if rng.random() < 0.85 else max(1, tG + rng.choice([-1, 1]))
    d = rng.randint(1, 3)
    EP = rng.randint(1, 4)
    DMAX = rng.choice([3, 4, 9])
    deg = [0] * NG
    for e in G:
        for v in e:
            deg[v] += 1
    adm = [(a, b) for a in range(NG) for b in range(a + 1, NG)
           if deg[a] <= EP and deg[b] <= EP and not any(a in e and b in e for e in G)]
    exp = dict(sol=0, f7free=0, inC=0, conn=0)
    expX = set()
    if TG == tG and TG >= 1:
        for S in itertools.combinations(adm, d):
            vs = [v for p in S for v in p]
            if len(set(vs)) != 2 * d:
                continue
            X = G + [tuple(sorted((a, b, NG))) for (a, b) in S]
            if tau(NG + 1, X) < TG + 1:
                continue
            exp['sol'] += 1
            if has_f7(X):
                continue
            exp['f7free'] += 1
            if not p3(NG + 1, X):
                continue
            exp['inC'] += 1
            dg = [0] * (NG + 1)
            for e in X:
                for v in e:
                    dg[v] += 1
            if conn(NG + 1, X) and max(dg) <= DMAX:
                exp['conn'] += 1
                expX.add(tuple(sorted(X)))
    inp = "%d %s\n" % (len(G), " ".join("%d %d %d" % e for e in G))
    out = subprocess.run([MYEXT, str(NG), str(TG), str(d), str(EP), str(DMAX)], input=inp, capture_output=True, text=True)
    got = {}
    gotX = set()
    for line in out.stdout.splitlines():
        if line.startswith('MYSUMMARY'):
            for kv in line.split()[1:]:
                k, v = kv.split('=')
                got[k] = int(v)
        elif line.startswith('X:'):
            es = [tuple(sorted(int(x) for x in t.strip('()').split(','))) for t in line[2:].split()]
            gotX.add(tuple(sorted(es)))
    ok = all(got.get(k) == exp[k] for k in exp) and gotX == expX and (got.get('badtau') == (0 if (TG == tG and TG >= 1) else 1))
    for k in exp:
        tot[k] += exp[k]
    if not ok:
        bad += 1
        print("MISMATCH", NG, TG, tG, d, EP, DMAX, G, exp, got, len(expX), len(gotX))
print("BF-VALIDATE trials=%d mismatches=%d totals=%s" % (NTRIALS, bad, tot))
