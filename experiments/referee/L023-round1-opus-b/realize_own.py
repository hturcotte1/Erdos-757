"""Referee L023 round 1 (opus-b): own exact realizability decision for 3-graphs as AP hypergraphs of (4,5)-sets.
Written from scratch for this review; imports nothing from e757/, judge/ or the prover's/worker's scripts.

Question decided: is there an injective x: V -> R such that every edge {p,q,r} is a 3-term AP of x(V) (in some order) and x(V) is
a (4,5)-set?

Facts used (proved in the review, all elementary):
 (F1) x(V) is a (4,5)-set  <=>  x injective, weak Sidon (no x_a+x_b = x_c+x_d for disjoint pairs a<b, c<d), and no two 3-term APs
      of x(V) share two points.  [A coincidence |x_p-x_q| = |x_r-x_s| of two distinct pairs is either an AP (pairs share a point) or a
      weak-Sidon violation (disjoint pairs); a 4-set needs two coincidences to have < 5 distinct differences, and two APs inside a 4-set
      share two points.]
 (F2) For a fixed midpoint assignment mu (one midpoint per edge), the realizations with assignment mu are the injective points of the
      kernel W_mu of the homogeneous system 2x_mid - x_p - x_q = 0.  A linear relation l(x) = 0 holds on all of W iff sum_v l_v r_v = 0,
      where r_v is row v of a basis matrix of W.  Relations that hold on all of W persist on every subspace (adding equations).
Method (no use of the injective-midpoint rule K5 and no maximum principle): depth-first search over ALL 3^|E| midpoint assignments,
edges in a connectivity order, keeping an integer kernel basis; a node is pruned iff W already forces one of
   EQ     r_a = r_b (a != b),
   SIDON  r_a + r_b = r_c + r_d (pairs a<b, c<d distinct; after EQ is excluded they are disjoint),
   NONLIN two forced 3-term APs sharing two vertices.
Every realization survives all its ancestors (a forced relation would hold at the realization, contradicting (F1)).  A leaf with no
forced relation is realizable: a generic point of W is injective, weak Sidon, and has no two APs sharing two points; the program then
constructs an explicit integer point and checks the (4,5) property directly on all 4-subsets.
"""
import sys, json, itertools, random
from math import gcd

def kernel_init(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def add_equation(K, coeffs):
    """K: list of n rows (length k); coeffs: dict v -> c.  Returns new K (kernel of the extra equation inside span(K))."""
    k = len(K[0]) if K else 0
    g = [0] * k
    for v, c in coeffs.items():
        row = K[v]
        for j in range(k):
            if row[j]: g[j] += c * row[j]
    nz = [j for j in range(k) if g[j]]
    if not nz:
        return K, False
    j0 = min(nz, key=lambda j: abs(g[j]))
    gj = g[j0]
    others = [i for i in range(k) if i != j0]
    newK = []
    for row in K:
        rj = row[j0]
        newK.append([gj * row[i] - g[i] * rj for i in others])
    # normalize columns by gcd
    kk = len(others)
    for i in range(kk):
        d = 0
        for row in newK:
            if row[i]:
                d = gcd(d, row[i])
                if d == 1: break
        if d > 1:
            for row in newK: row[i] //= d
    return newK, True

def forced_violation(K, n):
    """returns None or a description of a forced EQ / SIDON / NONLIN relation."""
    vecs = [tuple(K[v]) for v in range(n)]
    pos = {}
    for v, t in enumerate(vecs):
        if t in pos: return ('EQ', pos[t], v)
        pos[t] = v
    k = len(K[0]) if K else 0
    sums = {}
    for a in range(n):
        ra = vecs[a]
        for b in range(a + 1, n):
            rb = vecs[b]
            s = tuple(ra[i] + rb[i] for i in range(k))
            if s in sums: return ('SIDON', sums[s], (a, b))
            sums[s] = (a, b)
    # forced APs: triples with r_p + r_q = 2 r_m (m middle)
    third = {}
    for a in range(n):
        ra = vecs[a]
        for b in range(a + 1, n):
            rb = vecs[b]
            found = set()
            t1 = tuple(2 * rb[i] - ra[i] for i in range(k))   # b middle, third point beyond b
            if t1 in pos: found.add(pos[t1])
            t2 = tuple(2 * ra[i] - rb[i] for i in range(k))   # a middle
            if t2 in pos: found.add(pos[t2])
            s = [ra[i] + rb[i] for i in range(k)]
            if all(x % 2 == 0 for x in s):
                t3 = tuple(x // 2 for x in s)                  # third point is the middle
                if t3 in pos: found.add(pos[t3])
            if len(found) >= 2: return ('NONLIN', (a, b), tuple(sorted(found)))
    return None

def edge_order(edges):
    rem = list(range(len(edges))); order = []; seen = set()
    while rem:
        best = max(rem, key=lambda i: (len(set(edges[i]) & seen), -i))
        order.append(best); rem.remove(best); seen |= set(edges[best])
    return order

def is45(xs):
    xs = list(xs)
    if len(set(xs)) != len(xs): return False
    for B in itertools.combinations(xs, 4):
        if len({abs(p - q) for p, q in itertools.combinations(B, 2)}) < 5: return False
    return True

def witness(K, n, edges, mids, tries=50):
    rng = random.Random(12345)
    k = len(K[0])
    for _ in range(tries):
        t = [rng.randint(-10**6, 10**6) for _ in range(k)]
        x = [sum(K[v][j] * t[j] for j in range(k)) for v in range(n)]
        ok = all(x[p] + x[q] == 2 * x[m] for (p, m, q) in mids)
        if ok and is45(x): return x
    return None

def decide(edges, n=None, prune=True, stop_at_first=True):
    if n is None: n = 1 + max(max(e) for e in edges)
    order = edge_order(edges)
    stats = {'nodes': 0, 'EQ': 0, 'SIDON': 0, 'NONLIN': 0, 'dependent_eq': 0, 'leaves_ok': 0}
    sols = []
    def rec(depth, K, mids):
        stats['nodes'] += 1
        if depth == len(order):
            if prune:
                viol = None
            else:
                viol = forced_violation(K, n)
                if viol: stats[viol[0]] += 1; return False
            stats['leaves_ok'] += 1
            w = witness(K, n, edges, mids)
            sols.append((list(mids), w))
            return stop_at_first
        e = edges[order[depth]]
        for m in e:
            p, q = [v for v in e if v != m]
            coeffs = {m: 2, p: -1, q: -1}
            K2, indep = add_equation(K, coeffs)
            if not indep: stats['dependent_eq'] += 1
            if prune:
                viol = forced_violation(K2, n)
                if viol:
                    stats[viol[0]] += 1; continue
            if rec(depth + 1, K2, mids + [(p, m, q)]): return True
        return False
    rec(0, kernel_init(n), [])
    return stats, sols

def count_injective_labellings(edges):
    used = set(); cnt = [0]
    def rec(i):
        if i == len(edges): cnt[0] += 1; return
        for v in edges[i]:
            if v not in used:
                used.add(v); rec(i + 1); used.discard(v)
    rec(0)
    return cnt[0]

if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    for name, edges in data.items():
        edges = [tuple(e) for e in edges]
        st, sols = decide(edges)
        print(name, 'REALIZABLE' if sols else 'NOT-REALIZABLE', json.dumps(st), ('witness_is45=%s' % (sols[0][1] is not None)) if sols else '', flush=True)
