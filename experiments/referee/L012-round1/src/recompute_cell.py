"""Referee: independent recomputation of the TOP recursion level of a prover cell (n,m,t,D) with the referee's own tools:
decompositions by the referee's brute force (arith_decomp.decomps), inputs = all multisets of the prover's component-class
representatives, extensions by rext (no F7 pruning), filters by rfilt, isomorphism classes by networkx VF2 (no nauty); the result
is compared with the prover's list cell(n,m,t,D) (both directions: every connected survivor matches a listed class, every listed
class is hit, listed classes pairwise non-isomorphic within WL buckets)."""
import sys, os, math, itertools, subprocess, collections, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from closure_check import edges_of, inc, wl, nm, iso, CD
HERE = '/home/user/Erdos-757/experiments/referee/L012-round1'
def types(nn, smax):
    if nn == 1: return [(1, 0, 0)] if 3 <= smax else []
    if nn == 2: return []
    out = []
    for mm in range(math.ceil((nn - 1) / 2), nn - 1):
        for t in range(1, mm + 1):
            s = 3 * nn + 2 * mm - 11 * t
            if 0 <= s <= smax and 17 * t <= 5 * nn + 3 * mm: out.append((nn, mm, t))
    return out
def decomps(N, M, S):
    res = set()
    def rec(remN, remM, remS, maxpart, cur):
        if remN == 0:
            if remM == 0 and remS == 0: res.add(tuple(sorted(cur)))
            return
        for part in range(min(remN, maxpart), 0, -1):
            for ty in types(part, remS):
                s = 3 * ty[0] + 2 * ty[1] - 11 * ty[2]
                if ty[1] <= remM and s <= remS: rec(remN - part, remM - ty[1], remS - s, part, cur + [ty])
    rec(N, M, S, N, [])
    return sorted(res)
def load(n, m, t, D):
    fn = os.path.join(CD, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
    if (n, m) == (1, 0): return [[]]
    if not os.path.exists(fn): return None
    return [edges_of(l) for l in open(fn) if l.startswith('FOUND')]
n, m, t, D = map(int, sys.argv[1].split(','))
tag = '%d_%d_%d_D%d' % (n, m, t, D)
survivors = []
for d in range(max(1, math.ceil(3 * m / n)), D + 1):
    for tp in (t - 1, t):
        Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
        if Sp < 0: continue
        decs = decomps(n - 1, m - d, Sp); inputs = []
        for dec in decs:
            groups = collections.Counter(dec); gl = []
            for typ, k in sorted(groups.items()):
                L = load(*typ, d)
                if L is None: print('MISSING cell list', typ, d); L = []
                gl.append((typ, L, list(itertools.combinations_with_replacement(range(len(L)), k))))
            for combo in itertools.product(*[g[2] for g in gl]):
                es = []; off = 0
                for (typ, L, _), idxs in zip(gl, combo):
                    for i in idxs: es += [tuple(v + off for v in e) for e in L[i]]; off += typ[0]
                inputs.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
        if tp == t:
            if inputs: print('branch tp = t with inputs: not handled by this script', file=sys.stderr); sys.exit(3)
            print('branch d=%d tp=%d S\'=%d decompositions=%d inputs=0 (tp = t branch, nothing to extend)' % (d, tp, Sp, len(decs))); continue
        if not inputs: print('branch d=%d tp=%d S\'=%d decompositions=%d inputs=0' % (d, tp, Sp, len(decs))); continue
        fin = os.path.join(HERE, 'out', 'rc_%s_d%d_in.txt' % (tag, d)); open(fin, 'w').write('\n'.join(inputs) + '\n')
        fx = fin.replace('_in.txt', '_x.txt'); ff = fin.replace('_in.txt', '_f.txt')
        subprocess.run('nice -n 5 %s/out/bin/rext %d %d %d < %s > %s' % (HERE, n - 1, d, d - 1, fin, fx), shell=True, check=True)
        subprocess.run('nice -n 5 %s/out/bin/rfilt %d %s < %s > %s' % (HERE, n - 1, fin, fx, ff), shell=True, check=True)
        tl = open(fx).read().strip().splitlines()[-1]; fl = open(ff).read().strip().splitlines()[-1]
        bad_t = sum(1 for l in open(fx) if l.startswith('G:') and (' t=%d ' % tp) not in l)
        print('branch d=%d tp=%d S\'=%d decompositions=%d inputs=%d | rext %s | inputs with tau != tp: %d | rfilt %s' % (d, tp, Sp, len(decs), len(inputs), tl, bad_t, fl))
        survivors += [edges_of(l) for l in open(ff) if l.startswith('S:') and '#conn=1' in l]
reps = load(n, m, t, D)
RG = [inc(E, range(n)) for E in reps]; B = collections.defaultdict(list)
for i, G in enumerate(RG): B[wl(G)].append(i)
pairs = sum(len(v) * (len(v) - 1) // 2 for v in B.values())
isop = sum(1 for v in B.values() for a, b in itertools.combinations(v, 2) if iso.GraphMatcher(RG[a], RG[b], node_match=nm).is_isomorphic())
hit = collections.Counter(); unmatched = 0
for E in survivors:
    G = inc(E, range(n)); k = wl(G); f = None
    for i in B.get(k, []):
        if iso.GraphMatcher(G, RG[i], node_match=nm).is_isomorphic(): f = i; break
    if f is None: unmatched += 1
    else: hit[f] += 1
print('cell %s: connected survivors %d, UNMATCHED %d, listed classes %d, hit %d, listed pairs in WL buckets %d, isomorphic pairs %d' % (sys.argv[1], len(survivors), unmatched, len(reps), len(hit), pairs, isop))
