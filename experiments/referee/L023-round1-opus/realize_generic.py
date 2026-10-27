"""Referee L023 round 1 (own code; no import of e757/, judge/ or any prover script).
Decides, for a 3-graph X on vertices 0..n-1, whether there is a (4,5)-set A and a bijection phi: V -> A mapping every edge to a
3-term AP -- from the DEFINITION of a (4,5)-set only (no use of K3/K5/K6, of the midpoint injectivity or of the max principle).

Method. Depth-first search over ALL midpoint assignments (each edge chooses any of its 3 vertices as the middle term: 3^m leaves
before pruning). A node is the linear subspace V of R^n cut out by the chosen equations x_a + x_c - 2 x_mid = 0; it is stored as
vectors r_v in Q^k (x_v = <r_v, lambda>, lambda in R^k free), exactly, with Fractions.
Test of a node ("the generic point of V"): the bad set {x in V : x not injective, or some 4 points of x have <= 4 distinct distances}
is a finite union of linear subspaces of V (|x_i-x_j| = |x_k-x_l| iff x_i-x_j = +-(x_k-x_l)); since V is irreducible it is all of V
iff one of these subspaces is V, i.e. iff the relation holds identically, i.e. in terms of the r_v. So:
   generic point bad  <=>  some r_i = r_j, or some 4-set whose 6 difference vectors r_i - r_j fall into <= 4 classes modulo sign.
If the generic point of V is bad, every point of V and of every subspace of V is bad: prune (sound). If a leaf (all edges assigned)
has a good generic point, a generic point of V is a (4,5)-set on which all edges are 3-term APs: REALIZABLE. Otherwise, after the
complete search, NOT-REALIZABLE.  Exactness: all arithmetic in Fractions; no floating point."""
import sys, re, json, itertools, time
from fractions import Fraction

def parse(line):
    return [tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\((\d+,\d+,\d+)\)', line)]

def norm(vec):
    for c in vec:
        if c != 0:
            return vec if c > 0 else tuple(-x for x in vec)
    return None   # zero vector

def generic_bad(R, n):
    """R[v] = tuple of Fractions. Returns None if the generic point is good, else a reason."""
    cls = {}
    pairs = {}
    for i in range(n):
        for j in range(i + 1, n):
            d = norm(tuple(a - b for a, b in zip(R[i], R[j])))
            if d is None: return ('EQUAL', i, j)
            pairs[(i, j)] = d
            cls.setdefault(d, []).append((i, j))
    cand = set()
    for d, L in cls.items():
        if len(L) < 2: continue
        for p, q in itertools.combinations(L, 2):
            U = set(p) | set(q)
            if len(U) == 4: cand.add(tuple(sorted(U)))
            else:
                for w in range(n):
                    if w not in U: cand.add(tuple(sorted(U | {w})))
    for S in cand:
        k = len(set(pairs[(a, b)] for a, b in itertools.combinations(S, 2)))
        if k <= 4: return ('FOUR', S, k)
    return None

def add_eq(R, a, mid, c):
    k = len(R[0])
    coef = [R[a][t] + R[c][t] - 2 * R[mid][t] for t in range(k)]
    j = next((t for t in range(k) if coef[t] != 0), None)
    if j is None: return R  # implied
    # lambda_j = -(1/coef_j) * sum_{t != j} coef_t lambda_t
    fac = [(-coef[t] / coef[j]) for t in range(k)]
    out = []
    for r in R:
        rj = r[j]
        out.append(tuple(r[t] + rj * fac[t] for t in range(k) if t != j))
    return out

def order_edges(E):
    rest = list(E); out = [rest.pop(0)]; seenv = set(out[0])
    while rest:
        best = max(range(len(rest)), key=lambda i: (len(set(rest[i]) & seenv), -i))
        e = rest.pop(best); out.append(e); seenv |= set(e)
    return out

def decide(E, n):
    E = order_edges(E)
    R0 = [tuple(Fraction(int(v == t)) for t in range(n)) for v in range(n)]
    stats = dict(nodes=0, pruned=0, leaves_good=0, reasons={})
    witness = []
    def rec(i, R):
        stats['nodes'] += 1
        bad = generic_bad(R, n)
        if bad is not None:
            stats['pruned'] += 1; stats['reasons'][bad[0]] = stats['reasons'].get(bad[0], 0) + 1
            return False
        if i == len(E):
            stats['leaves_good'] += 1; witness.append(R); return True
        a, b, c = E[i]
        for mid, x, y in ((a, b, c), (b, a, c), (c, a, b)):
            if rec(i + 1, add_eq(R, x, mid, y)): return True
        return False
    t0 = time.time(); ok = rec(0, R0); stats['secs'] = round(time.time() - t0, 1)
    return ok, stats, (witness[0] if witness else None)

if __name__ == '__main__':
    src = sys.argv[1]; which = sys.argv[2] if len(sys.argv) > 2 else 'all'
    if src == 'Q8':
        graphs = [('Q8', [(0, 2, 3), (0, 4, 5), (0, 6, 7), (1, 3, 4), (1, 5, 6), (1, 2, 7)], 8)]
    elif src == 'set':   # positive control: the AP hypergraph of an explicit set of integers
        A = sorted(json.loads(sys.argv[3])); pos = {x: i for i, x in enumerate(A)}; S = set(A)
        E = []
        for i, x in enumerate(A):
            for z in A[i + 1:]:
                if (x + z) % 2 == 0 and (x + z) // 2 in S: E.append(tuple(sorted((i, pos[(x + z) // 2], pos[z]))))
        graphs = [('set', E, len(A))]
    else:
        L = [parse(l) for l in open(src) if '(' in l]
        idx = range(len(L)) if which == 'all' else map(int, which.split(','))
        graphs = [('X_%d' % i, L[i], 1 + max(v for e in L[i] for v in e)) for i in idx]
    for name, E, n in graphs:
        ok, st, w = decide(E, n)
        print(name, 'n=%d m=%d' % (n, len(E)), 'REALIZABLE' if ok else 'NOT-REALIZABLE', json.dumps(st), flush=True)
        if ok:
            k = len(w[0]); print('  witness dimension', k)
