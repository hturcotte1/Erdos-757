"""L026 sanity check: the AP hypergraph of A_base (tight (14,12,6)) has no b-triple (Theorem 13)."""
import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L
A = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
idx = {x: i for i, x in enumerate(A)}
E = []
for i, j in itertools.combinations(range(len(A)), 2):
    s = A[i] + A[j]
    if s % 2 == 0 and s // 2 in idx and idx[s // 2] not in (i, j):
        E.append(tuple(sorted((i, j, idx[s // 2]))))
E = sorted(set(E))
n = len(A); m = len(E); t = L.tau(E)
print('A_base AP hypergraph: n', n, 'm', m, 'tau', t, 'slack', 3 * n + 2 * m - 11 * t, 'in C', L.is_linear(E) and not L.has_F7(n, E) and L.p3_ok(n, E))
T = L.all_min_transversals(E, t)
co = set()
for Tm in T:
    vs = [i for i in range(n) if Tm >> i & 1]
    for p in itertools.combinations(vs, 2): co.add(p)
Es = set(E)
bt = [tr for tr in itertools.combinations(range(n), 3) if all(p not in co for p in itertools.combinations(tr, 2)) and tr not in Es]
print('minimum transversals', len(T), 'NC pairs', sum(1 for p in itertools.combinations(range(n), 2) if p not in co), 'b-triples', len(bt))
