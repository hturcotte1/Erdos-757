"""(L014) An explicit 23-point (4,5)-set with h = 14 (upper bound f(23) <= 14 without K1/K24), exact integers.
C23 = B12 U (10**9 + 7919*B11), B12 = the third 12-point record of kb/00_START_HERE.md section 6 (h = 7), B11 = data/small_records.json
'11' (h = 7).  Checks: (4,5) by brute force over all 4-subsets (at least 5 distinct absolute differences); weak Sidon; the AP hypergraph;
h = largest Sidon subset, computed as n - tau(H) (K4: for weak Sidon sets the Sidon subsets are the 3-AP-free subsets) with pyverify's
exact tau, and cross-checked by an explicit Sidon subset of size h and by e757.core.alpha."""
import sys, os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, '/home/user/Erdos-757')
import pyverify as pv
B12 = [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575]
B11 = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']['11']['set']
A = sorted(B12 + [10 ** 9 + 7919 * b for b in B11]); n = len(A)
ok45 = all(len({abs(x - y) for x, y in itertools.combinations(Q, 2)}) >= 5 for Q in itertools.combinations(A, 4))
sums = [x + y for x, y in itertools.combinations(A, 2)]; weak = len(sums) == len(set(sums))
idx = {a: i for i, a in enumerate(A)}
E = sorted((idx[a], idx[b], idx[c]) for a, b, c in itertools.combinations(A, 3) if a + c == 2 * b)
t = pv.tau(E); h = n - t
def is_sidon(S):
    s = [x + y for x, y in itertools.combinations_with_replacement(S, 2)]; return len(s) == len(set(s))
# explicit Sidon subset of size h: complement of a minimum cover
cov = None
for T in itertools.combinations(range(n), t):
    st = set(T)
    if all(st & set(e) for e in E): cov = st; break
S = [A[i] for i in range(n) if i not in cov]
from e757.core import alpha
print('C23 =', A)
print('n = %d, (4,5): %s, weak Sidon: %s, 3-APs m = %d, in C: %s, tau = %d, h = n - tau = %d' % (n, ok45, weak, len(E), pv.in_C(E), t, h))
print('explicit Sidon subset of size %d: %s, Sidon: %s; e757.core.alpha = %d' % (len(S), S, is_sidon(S), alpha(A)))
