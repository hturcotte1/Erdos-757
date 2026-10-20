"""(L016) An explicit 27-point (4,5)-set with h = 16 (upper bound f(27) <= 16 without K1), exact integers.
C27 = A_base U (10**9 + 7919*B13), A_base = the Ma-Tang 14-point set (h = 8), B13 = A_base minus its maximum 1056 (a 13-point subset of
a (4,5)-set, so a (4,5)-set, with h <= 8).  Checks (as L014's c23_construction.py): (4,5) by brute force over all 4-subsets (at least
5 distinct absolute differences); weak Sidon; the AP hypergraph and its membership in C (pyverify, pure Python); tau by pyverify's exact
branching; h = n - tau (K4), cross-checked by an explicit Sidon subset of size h (complement of a minimum cover found by branching)
and by e757.core.alpha (repository code, unchanged)."""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/user/Erdos-757')
import pyverify as pv
ABASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
B13 = [x for x in ABASE if x != 1056]
def analyse(A, name):
    A = sorted(A); n = len(A)
    ok45 = all(len({abs(x - y) for x, y in itertools.combinations(Q, 2)}) >= 5 for Q in itertools.combinations(A, 4))
    sums = [x + y for x, y in itertools.combinations(A, 2)]; weak = len(sums) == len(set(sums))
    idx = {a: i for i, a in enumerate(A)}
    E = sorted((idx[a], idx[b], idx[c]) for a, b, c in itertools.combinations(A, 3) if a + c == 2 * b)
    t = pv.tau(E)
    def find_cover(S, k):          # a cover of size <= k containing S, by branching on the first uncovered edge
        for e in E:
            if not (S & set(e)):
                if k == 0: return None
                for v in e:
                    r = find_cover(S | {v}, k - 1)
                    if r is not None: return r
                return None
        return S
    cov = find_cover(set(), t); assert cov is not None and len(cov) <= t and find_cover(set(), t - 1) is None
    S = [A[i] for i in range(n) if i not in cov]
    def is_sidon(X):
        s = [x + y for x, y in itertools.combinations_with_replacement(X, 2)]; return len(s) == len(set(s))
    from e757.core import alpha
    print('%s = %s' % (name, A))
    print('  n = %d, (4,5): %s, weak Sidon: %s, 3-APs m = %d, in C: %s, tau = %d, h = n - tau = %d' % (n, ok45, weak, len(E), pv.in_C(E), t, n - t))
    print('  explicit Sidon subset of size %d: %s, Sidon: %s; e757.core.alpha = %d' % (len(S), S, is_sidon(S), alpha(A)))
    return n - t
analyse(ABASE, 'A_base'); analyse(B13, 'B13')
C27 = ABASE + [10 ** 9 + 7919 * b for b in B13]
h = analyse(C27, 'C27')
print('RESULT C27: 27 points, h = %d, 16/27 %s 4/7' % (h, '<' if 16 * 7 < 4 * 27 else '>='))
