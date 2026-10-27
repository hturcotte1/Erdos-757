"""Referee round 2 (opus): data test of the gadget step 6.5' (Theorem 6(b')).
For each class F (tight or slack 1, Delta<=3) and every two disjoint admissible pairs P1, P2
(vertices of F-degree 1 or 2, not inside an edge of F), build H1 = F + v + {v}uP1 + {v}uP2 and check
  tau(H1) = tau(F)+1  <=>  no minimum transversal of F meets both P1 and P2      (logic of 6.5')
  and slack(H1) = slack(F) - 4 in that case.
Also report whether any such H1 with tau(H1)=tau(F)+1 is in C (linear always; F7-freeness and
e(S)<=|S|-2 tested): such an H1 would violate I11 with < 28 vertices (contradicting L016). Own code."""
import sys, re, itertools

def parse(fn):
    out = []
    for line in open(fn):
        if line.startswith('FOUND:'):
            out.append([tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)])
    return out

def all_min_transversals(E, n):
    inc = [0] * n
    for i, e in enumerate(E):
        for v in e: inc[v] |= 1 << i
    full = (1 << len(E)) - 1
    for k in range(0, n + 1):
        sols = []
        for T in itertools.combinations(range(n), k):
            c = 0
            for v in T: c |= inc[v]
            if c == full: sols.append(frozenset(T))
        if sols: return k, sols

def tau(E, n):
    inc = [0] * n
    for i, e in enumerate(E):
        for v in e: inc[v] |= 1 << i
    memo = {}
    def rec(mask):
        if mask == 0: return 0
        if mask in memo: return memo[mask]
        i = (mask & -mask).bit_length() - 1
        r = min(1 + rec(mask & ~inc[u]) for u in E[i]); memo[mask] = r; return r
    return rec((1 << len(E)) - 1)

F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def has_f7(E):
    deg = {}
    for S in itertools.combinations(E, 5):
        V = set(v for e in S for v in e)
        if len(V) != 7: continue
        d = {}
        for e in S:
            for v in e: d[v] = d.get(v, 0) + 1
        if sorted(d.values()) == [2,2,2,2,2,2,3]: return True  # linear + this degree pattern = F7 (Lemma 0.7)
    return False

def ecount_ok(E, n):
    # e_ind(S) <= |S|-2 for all S, |S|>=2: check via all edge subsets' vertex unions (|V(F)| >= |F|+2)
    m = len(E)
    for k in range(1, m + 1):
        for S in itertools.combinations(E, k):
            if len(set(v for e in S for v in e)) < k + 2: return False
    return True

stats = dict(classes=0, instances=0, logic_viol=0, tau_up=0, tau_up_in_C=0)
for fn in sys.argv[1:]:
    n, m, t = map(int, re.search(r'cell_(\d+)_(\d+)_(\d+)_D', fn).groups())
    sl = 3*n + 2*m - 11*t
    for E in parse(fn):
        stats['classes'] += 1
        k, mins = all_min_transversals(E, n); assert k == t
        deg = [0]*n
        for e in E:
            for v in e: deg[v] += 1
        low = [v for v in range(n) if 1 <= deg[v] <= 2]
        inedge = set()
        for e in E:
            for a, b in itertools.combinations(sorted(e), 2): inedge.add((a, b))
        pairs = [P for P in itertools.combinations(low, 2) if P not in inedge]
        for P1, P2 in itertools.combinations(pairs, 2):
            if set(P1) & set(P2): continue
            stats['instances'] += 1
            v = n
            H1 = E + [(v,) + P1, (v,) + P2]
            t1 = tau(H1, n + 1)
            meets = any((T & set(P1)) and (T & set(P2)) for T in mins)
            if (t1 == t + 1) != (not meets): stats['logic_viol'] += 1
            if t1 == t + 1:
                stats['tau_up'] += 1
                s1 = 3*(n+1) + 2*(m+2) - 11*t1
                assert s1 == sl - 4
                lin = all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(H1, 2))
                if lin and not has_f7(H1) and ecount_ok(H1, n + 1):
                    stats['tau_up_in_C'] += 1; print('VIOLATOR IN C?', fn, H1)
    print(fn.split('/')[-1], 'slack', sl, dict(stats)); sys.stdout.flush()
print('TOTAL', stats)
