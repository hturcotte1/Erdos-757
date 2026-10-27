"""Referee's own helper functions (independent of e757/ and judge/). Exact integer/Fraction arithmetic."""
import itertools
from fractions import Fraction
import numpy as np


def parse(raw):
    vals = [Fraction(str(x)) for x in raw]
    assert len(set(vals)) == len(vals), 'repeated elements'
    den = 1
    for v in vals:
        den = den * v.denominator // np.gcd(den, v.denominator) if False else den
    # scale to integers exactly (lcm of denominators)
    from math import lcm
    L = 1
    for v in vals:
        L = lcm(L, v.denominator)
    ints = sorted(int(v * L) for v in vals)
    assert len(set(ints)) == len(ints)
    return ints


def is45_bf(A):
    for B in itertools.combinations(A, 4):
        if len({abs(x - y) for x, y in itertools.combinations(B, 2)}) < 5:
            return False
    return True


def aps(A):
    n = len(A)
    return [(i, j, k) for i, j, k in itertools.combinations(range(n), 3) if A[i] + A[k] == 2 * A[j]]


def weak_sidon(A):
    s = [x + y for x, y in itertools.combinations(A, 2)]
    return len(s) == len(set(s))


def linear(E):
    return all(len(set(e) & set(f)) <= 1 for e, f in itertools.combinations(E, 2))


def sidon(S):
    d = [y - x for x, y in itertools.combinations(sorted(S), 2)]
    return len(d) == len(set(d))


def obstructions(A):
    n = len(A)
    by = {}
    for i, j in itertools.combinations(range(n), 2):
        by.setdefault(A[j] - A[i], []).append((i, j))
    ob = set()
    for L in by.values():
        for p, q in itertools.combinations(L, 2):
            ob.add(sum(1 << v for v in set(p) | set(q)))
    return sorted(ob)


def h_numpy(A):
    n = len(A)
    assert n <= 24
    N = 1 << n
    masks = np.arange(N, dtype=np.int64)
    bad = np.zeros(N, dtype=bool)
    for U in obstructions(A):
        bad |= (masks & U) == U
    pc = np.bitwise_count(masks.astype(np.uint64))
    return int(pc[~bad].max())


def h_cpsat(A):
    from ortools.sat.python import cp_model
    n = len(A)
    md = cp_model.CpModel()
    x = [md.NewBoolVar(f'x{i}') for i in range(n)]
    for U in obstructions(A):
        vs = [i for i in range(n) if U >> i & 1]
        md.Add(sum(x[i] for i in vs) <= len(vs) - 1)
    md.Maximize(sum(x))
    s = cp_model.CpSolver()
    s.parameters.num_workers = 1
    s.parameters.max_time_in_seconds = 300
    st = s.Solve(md)
    assert s.StatusName(st) == 'OPTIMAL', s.StatusName(st)
    sol = [A[i] for i in range(n) if s.Value(x[i])]
    assert sidon(sol)
    return int(round(s.ObjectiveValue()))


def tau_bf(n, E):
    for k in range(0, n + 1):
        for T in itertools.combinations(range(n), k):
            Ts = set(T)
            if all(Ts & set(e) for e in E):
                return k


F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]


def f7_homs(n, E):
    """number of injective maps phi: V(F7) -> V(H) sending every F7 edge to an edge of H."""
    Es = {frozenset(e) for e in E}
    inc = {v: [e for e in E if v in e] for v in range(n)}
    cnt = 0
    for v in range(n):
        for e1, e2, e3 in itertools.permutations(inc[v], 3):
            o = [[u for u in e if u != v] for e in (e1, e2, e3)]
            if any(len(x) != 2 for x in o):
                continue
            for a in (o[0], o[0][::-1]):
                for b in (o[1], o[1][::-1]):
                    for c in (o[2], o[2][::-1]):
                        phi = {0: v, 1: a[0], 2: a[1], 3: b[0], 4: b[1], 5: c[0], 6: c[1]}
                        if len(set(phi.values())) != 7:
                            continue
                        if frozenset((phi[1], phi[3], phi[5])) in Es and frozenset((phi[2], phi[4], phi[6])) in Es:
                            cnt += 1
    return cnt


def f7_subsets(E):
    import networkx as nx
    def incg(edges):
        G = nx.Graph()
        for t, e in enumerate(edges):
            G.add_node(('e', t), kind='e')
            for v in e:
                G.add_node(('v', v), kind='v')
                G.add_edge(('e', t), ('v', v))
        return G
    GF = incg(F7)
    nm = nx.algorithms.isomorphism.categorical_node_match('kind', None)
    c = 0
    for E5 in itertools.combinations(E, 5):
        if len(set().union(*map(set, E5))) == 7 and nx.is_isomorphic(incg(E5), GF, node_match=nm):
            c += 1
    return c
