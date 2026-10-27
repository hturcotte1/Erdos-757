"""L017, falsification test of the structure theorem (Theorems 1-5) on vertex-minimal I11 violators among ALL connected
linear 3-graphs with at most NMAX vertices (not only class C: the proofs of Theorems 1-5 use only linearity and the
fact that proper induced subgraphs satisfy I11, see Remark 6.4; so every vertex-minimal linear violator must satisfy them).

Pipeline: for every (N, M) with lo = floor((3N+2M)/11)+1 <= M, L007's enumerator `enum_conn N M lo N 1` lists a labelled
copy of every connected linear 3-graph with N vertices, M edges and tau >= lo (L007 Lemma D); `canon` (nauty) reduces to
one representative per class; tau of EVERY vertex subset is computed exactly by the DP
tau(S) = 1 + min_{x in e} tau(S - x) (e = first edge inside S), so every claim below is checked exactly.
A violator H (slack < 0) is vertex-minimal if every proper induced subgraph has slack >= 0.
Usage: python3 minimal_violators.py NMAX [NMIN]"""
import sys, os, subprocess, itertools, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hyp import contains_F7, is_linear
BIN = '/home/user/Erdos-757/experiments/prover/L012/bin'

def enum(N, M, lo):
    out = subprocess.run([os.path.join(BIN, 'enum_conn'), str(N), str(M), str(lo), str(N), '1'], capture_output=True,
                         text=True, timeout=3000).stdout
    found = [l for l in out.splitlines() if l.startswith('FOUND:')]
    if not found: return []
    c = subprocess.run([os.path.join(BIN, 'canon'), str(N)], input='\n'.join(found) + '\n', capture_output=True, text=True,
                       timeout=3000).stdout.split('\n')
    keys = sorted(set(l for l in c if l.startswith('C ')))
    return [[tuple(map(int, p.split('.'))) for p in k.split()[2:]] for k in keys]

class HG:
    def __init__(self, N, edges):
        self.N = N; self.E = edges; self.em = [(1 << a) | (1 << b) | (1 << c) for (a, b, c) in edges]
        full = (1 << N) - 1; T = [0] * (1 << N); EC = [0] * (1 << N)
        for S in range(1, 1 << N):
            inside = [e for e in self.em if e & S == e]
            EC[S] = len(inside)
            if inside:
                e = inside[0]; best = 99; m = e
                while m:
                    b = m & -m; m ^= b
                    best = min(best, T[S ^ b])
                T[S] = 1 + best
        self.T = T; self.EC = EC; self.full = full
        self.deg = [sum(1 for e in edges if x in e) for x in range(N)]
    def slack(self, S): return 3 * bin(S).count('1') + 2 * self.EC[S] - 11 * self.T[S]
    def comps(self, S):
        """components of H[S] as bitmasks."""
        res = []; rest = S
        while rest:
            b = rest & -rest; comp = b; grow = True
            while grow:
                grow = False
                for e in self.em:
                    if e & S == e and e & comp and e & ~comp:
                        comp |= e; grow = True
            res.append(comp); rest &= ~comp
        return res
    def deg_in(self, x, S): return sum(1 for e in self.em if e & S == e and e >> x & 1)
    def dpair(self, x, y, S):
        return sum(1 for e in self.em if e & S == e and (e >> x & 1 or e >> y & 1))
    def in_min_T(self, X, S):
        """is the vertex set X (bitmask, X subset of S) contained in a minimum transversal of H[S]?"""
        return self.T[S & ~X] == self.T[S] - bin(X).count('1')

def bit(x): return 1 << x

def check(H, log):
    """returns list of failed claims (empty if all hold)."""
    fails = []; N = H.N; V = H.full; s = H.slack(V); tau = H.T[V]; d = H.deg
    def need(c, msg):
        if not c: fails.append(msg)
    # Theorem 1
    need(len(H.comps(V)) == 1, 'T1a connected')
    need(max(d) <= 3, 'T1c Delta<=3')
    for v in range(N):
        need(H.T[V & ~bit(v)] == tau - 1, 'T1b tau(H-v)=tau-1 v=%d' % v)
        need(H.slack(V & ~bit(v)) == s + 8 - 2 * d[v], 'T1b slack(H-v) v=%d' % v)
    need(max(d) == 3, 'Lemma M: Delta=3')
    if max(d) == 3: need(s in (-1, -2), 'T1e slack in {-1,-2}')
    # Theorem 3
    for e in H.E:
        ds = sorted(d[x] for x in e)
        need(sum(ds) >= 5, 'T3a degree sum >= 5 %s' % (e,))
        need(ds.count(1) <= 1, 'T3c two degree-1 vertices %s' % (e,))
        if ds[0] == 1: need(ds == [1, 2, 2], 'T3b pattern (1,2,2) %s' % (e,))
    for x in range(N):
        pend = [e for e in H.E if x in e and any(d[y] == 1 for y in e if y != x)]
        need(len(pend) <= 1, 'T3d vertex %d in two edges with degree-1 vertices' % x)
    if 1 in d: need(s == -1, 'T3e degree-1 vertex => slack -1')
    # Theorem 4 (degree-3 vertices)
    for v in range(N):
        if d[v] != 3: continue
        Ev = [e for e in H.E if v in e]; P = [tuple(y for y in e if y != v) for e in Ev]
        W = V & ~bit(v); cs = H.comps(W)
        need(all(d[y] >= 2 for p in P for y in p), 'T4a co-vertex degrees >= 2 v=%d' % v)
        need(all(bin(c).count('1') >= 3 for c in cs), 'T4b no isolated vertex in H-v v=%d' % v)
        sl = [H.slack(c) for c in cs]
        need(all(x >= 0 for x in sl) and sum(sl) == s + 2, 'T4c component slacks v=%d' % v)
        r = len(cs); need(r <= 3, 'T4d r<=3 v=%d' % v)
        cid = {}
        for i, c in enumerate(cs):
            for y in range(N):
                if c >> y & 1: cid[y] = i
        # Hall: is there a system of distinct components for the three pairs?
        hall_ok = any(len(set(ch)) == 3 for ch in itertools.product(*[[cid[y] for y in p] for p in P]))
        need(not hall_ok, 'T4 Hall must fail v=%d' % v)
        # (star): no minimum transversal of H - v meets all three pairs
        star = not any(H.in_min_T(bit(a) | bit(b) | bit(c), W) for a in P[0] for b in P[1] for c in P[2])
        need(star, 'T4 (star) v=%d' % v)
        # pattern
        types = []
        for p in P:
            ci = sorted(set(cid[y] for y in p)); types.append(('in', ci[0]) if len(ci) == 1 else ('split', tuple(ci)))
        key = pattern_name(r, types)
        log['pattern3'][key] += 1
        # per-pattern equivalent condition (computed from the components, compared with (star))
        cond = pattern_condition(H, r, P, types, cs, cid)
        need(cond == star, 'T4 pattern condition equivalence v=%d %s' % (v, key))
        need(key in ('a', 'b', 'c1', 'c2', 'e', 'f', 'd'), 'T4 pattern list v=%d %s' % (v, key))
        # pair lemma consequences: every pair required to be uncovered satisfies 2|d(x,y)| <= slack(F) + 5
        for (x, y, c) in required_uncovered(r, P, types, cs, cid):
            need(not H.in_min_T(bit(x) | bit(y), c), 'T4 required uncovered pair %d %d' % (x, y))
            need(2 * H.dpair(x, y, c) <= H.slack(c) + 5, 'T4 pair lemma %d %d' % (x, y))
    # Theorem 5 (degree-2 and degree-1 vertices)
    for v in range(N):
        if d[v] == 2:
            Ev = [e for e in H.E if v in e]; P = [tuple(y for y in e if y != v) for e in Ev]
            W = V & ~bit(v); cs = H.comps(W)
            need(H.slack(W) == s + 4, 'T5 slack(H-v)=s+4')
            iso = [c for c in cs if bin(c).count('1') == 1]; nontriv = [c for c in cs if bin(c).count('1') > 1]
            need(len(iso) <= 1, 'T5 at most one isolated vertex v=%d' % v)
            need(len(nontriv) == 1, 'T5 exactly one non-trivial component v=%d' % v)
            if iso:
                need(s == -1 and H.slack(nontriv[0]) == 0, 'T5 isolated => s=-1, F tight v=%d' % v)
                log['deg2'] += ['beta']
            else:
                log['deg2'] += ['alpha']
            star2 = not any(H.in_min_T(bit(a) | bit(b), W) for a in P[0] for b in P[1] if d[a] >= 2 and d[b] >= 2) \
                    and not any(H.in_min_T(bit(a) | bit(b), W) for a in P[0] for b in P[1])
            need(star2, 'T5 (star2) v=%d' % v)
            F = nontriv[0]
            for a in P[0]:
                for b in P[1]:
                    if F >> a & 1 and F >> b & 1:
                        need(2 * H.dpair(a, b, F) <= H.slack(F) + 5, 'T5 pair lemma v=%d' % v)
        if d[v] == 1:
            e = [e for e in H.E if v in e][0]; a, b = [y for y in e if y != v]
            W = V & ~bit(v)
            need(len(H.comps(W)) == 1 and H.slack(W) == 5, 'T5 deg1: H-y connected, slack 5')
            need(not H.in_min_T(bit(a), W) and not H.in_min_T(bit(b), W), 'T5 deg1: a,b in no min transversal of H-y')
            for (p, q) in ((a, b), (b, a)):
                W2 = V & ~bit(v) & ~bit(p)
                need(H.slack(W2) == 0 and len(H.comps(W2)) == 1, 'T5 deg1: H-{y,a} connected tight')
                f = [g for g in H.E if p in g and v not in g][0]; c1, c2 = [y for y in f if y != p]
                need(not H.in_min_T(bit(q) | bit(c1), W2) and not H.in_min_T(bit(q) | bit(c2), W2), 'T5 deg1: (b,c),(b,d) uncovered')
            log['deg1'] += 1
    return fails

def pattern_name(r, types):
    if r == 1: return 'a'
    if r == 3:
        ins = [t for t in types if t[0] == 'in']
        if len(ins) == 2 and ins[0][1] == ins[1][1]: return 'd'
        return 'r3-other'
    if r >= 4: return 'r>=4'
    # r == 2
    nin1 = sum(1 for t in types if t == ('in', 0)); nin2 = sum(1 for t in types if t == ('in', 1)); nsp = sum(1 for t in types if t[0] == 'split')
    k = tuple(sorted([nin1, nin2], reverse=True)) + (nsp,)
    return {(0, 0, 3): 'b', (2, 0, 1): 'c1', (2, 1, 0): 'c2', (1, 1, 1): 'e', (1, 0, 2): 'f'}.get(k, 'r2-%s' % (k,))

def pattern_condition(H, r, P, types, cs, cid):
    """the exact condition of Theorem 4 (iv) for the pattern, evaluated on the components."""
    def cov(X, c): return H.in_min_T(X, c)
    if r == 1:
        c = cs[0]
        return not any(cov(bit(a) | bit(b) | bit(x), c) for a in P[0] for b in P[1] for x in P[2])
    if r == 3:
        # two pairs inside one component F1: no min transversal of F1 meets both
        ins = [i for i, t in enumerate(types) if t[0] == 'in']; c = cs[types[ins[0]][1]]
        return not any(cov(bit(a) | bit(b), c) for a in P[ins[0]] for b in P[ins[1]])
    nin = [sum(1 for t in types if t == ('in', i)) for i in range(2)]
    if 3 in [sum(1 for t in types if t[0] == 'split')] or (nin == [0, 0]):
        # (b): no min transversal of F_i contains two attachment vertices
        ok = True
        for i in range(2):
            xs = [y for p in P for y in p if cid[y] == i]
            if any(cov(bit(x) | bit(y), cs[i]) for x, y in itertools.combinations(xs, 2)): ok = False
        return ok
    # orient so that component 0 holds the larger number of internal pairs
    if nin[1] > nin[0]: o = 1
    else: o = 0
    F1, F2 = cs[o], cs[1 - o]
    inF1 = [p for p, t in zip(P, types) if t == ('in', o)]; inF2 = [p for p, t in zip(P, types) if t == ('in', 1 - o)]
    spl = [p for p, t in zip(P, types) if t[0] == 'split']
    if len(inF1) == 2:   # c1 or c2: no min transversal of F1 meets both internal pairs
        return not any(cov(bit(a) | bit(b), F1) for a in inF1[0] for b in inF1[1])
    if len(inF1) == 1 and len(inF2) == 1:   # e = {1,2,s}
        q = spl[0]; e1 = [y for y in q if cid[y] == o][0]; f2 = [y for y in q if cid[y] == 1 - o][0]
        c1 = not any(cov(bit(a) | bit(e1), F1) for a in inF1[0])
        c2 = not any(cov(bit(a) | bit(f2), F2) for a in inF2[0])
        return c1 and c2
    if len(inF1) == 1 and len(spl) == 2:    # f = {1,s,s}
        ce = [[y for y in q if cid[y] == o][0] for q in spl]; df = [[y for y in q if cid[y] == 1 - o][0] for q in spl]
        c1 = not any(cov(bit(a) | bit(x), F1) for a in inF1[0] for x in ce)
        c2 = not cov(bit(df[0]) | bit(df[1]), F2)
        return c1 and c2
    raise ValueError('unexpected pattern')

def required_uncovered(r, P, types, cs, cid):
    """pairs (x, y, component) that the pattern condition requires to lie in no common minimum transversal."""
    out = []
    if r == 1: return out
    if r == 3:
        ins = [i for i, t in enumerate(types) if t[0] == 'in']; c = cs[types[ins[0]][1]]
        return [(a, b, c) for a in P[ins[0]] for b in P[ins[1]]]
    nin = [sum(1 for t in types if t == ('in', i)) for i in range(2)]
    if nin == [0, 0]:
        for i in range(2):
            xs = [y for p in P for y in p if cid[y] == i]
            out += [(x, y, cs[i]) for x, y in itertools.combinations(xs, 2)]
        return out
    o = 1 if nin[1] > nin[0] else 0
    F1, F2 = cs[o], cs[1 - o]
    inF1 = [p for p, t in zip(P, types) if t == ('in', o)]; inF2 = [p for p, t in zip(P, types) if t == ('in', 1 - o)]
    spl = [p for p, t in zip(P, types) if t[0] == 'split']
    if len(inF1) == 2: return [(a, b, F1) for a in inF1[0] for b in inF1[1]]
    if len(inF1) == 1 and len(inF2) == 1:
        q = spl[0]; e1 = [y for y in q if cid[y] == o][0]; f2 = [y for y in q if cid[y] == 1 - o][0]
        return [(a, e1, F1) for a in inF1[0]] + [(a, f2, F2) for a in inF2[0]]
    if len(inF1) == 1 and len(spl) == 2:
        ce = [[y for y in q if cid[y] == o][0] for q in spl]; df = [[y for y in q if cid[y] == 1 - o][0] for q in spl]
        return [(a, x, F1) for a in inF1[0] for x in ce] + [(df[0], df[1], F2)]
    return out

if __name__ == '__main__':
    NMAX = int(sys.argv[1]); NMIN = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    log = {'pattern3': collections.Counter(), 'deg2': [], 'deg1': 0}
    allfails = 0; minimal = []; nviol = collections.Counter()
    for N in range(NMIN, NMAX + 1):
        for M in range(1, N * (N - 1) // 6 + 1):
            lo = (3 * N + 2 * M) // 11 + 1
            if lo > M: continue
            reps = enum(N, M, lo)
            for es in reps:
                H = HG(N, es)
                if H.slack(H.full) >= 0: continue
                nviol[(N, M)] += 1
                if any(H.slack(S) < 0 for S in range(1, H.full)): continue
                f = check(H, log)
                info = dict(N=N, M=M, tau=H.T[H.full], slack=H.slack(H.full), edges=es, degrees=sorted(H.deg, reverse=True),
                            F7free=not contains_F7(N, es), P3=all(H.EC[S] <= bin(S).count('1') - 2 for S in range(1, H.full + 1) if bin(S).count('1') >= 2),
                            fails=f)
                minimal.append(info); allfails += len(f)
                print(json.dumps(info), flush=True)
        print('N=%d done; connected linear violators (classes) by M: %s' % (N, {k[1]: v for k, v in nviol.items() if k[0] == N}), flush=True)
    print('SUMMARY: %d vertex-minimal violators with %d <= N <= %d; total failed claims: %d; degree-3 patterns: %s; degree-2 cases: %s; degree-1 vertices checked: %d'
          % (len(minimal), NMIN, NMAX, allfails, dict(log['pattern3']), dict(collections.Counter(log['deg2'])), log['deg1']))
