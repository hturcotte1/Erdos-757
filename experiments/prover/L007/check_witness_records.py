"""(1) W from the definitions only (no e757): (4,5), its APs, and h by testing all subsets for the Sidon property.
(2) I11 slack and (n,m,h,tau) of A_base, the two omega 12-point sets, W and the Fibonacci set {F_3..F_16} (e757.core)."""
import sys, itertools
W = [0, 323, 523, 566, 569, 572, 595, 609, 621, 646, 723, 851, 919, 1379]
def sidon(S):
    s = [x + y for i, x in enumerate(S) for y in S[i:]]; return len(s) == len(set(s))
def nd(q): return len({abs(a - b) for a, b in itertools.combinations(q, 2)})
print('W (4,5):', all(nd(q) >= 5 for q in itertools.combinations(W, 4)), '(%d four-subsets)' % len(list(itertools.combinations(W, 4))))
aps = [(a, b, c) for a, b, c in itertools.combinations(W, 3) if a + c == 2 * b]
print('W APs:', len(aps), aps)
print('W h (Sidon definition, all subsets):', max(k for k in range(1, 15) if any(sidon(S) for S in itertools.combinations(W, k))))
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import ap_edges, is_45_set, alpha, KNOWN
fib = [1, 2]
while len(fib) < 30: fib.append(fib[-1] + fib[-2])
sets = dict(KNOWN); sets['W'] = W; sets['Fibonacci F_3..F_16'] = fib[1:15]
for name, A in sets.items():
    E = ap_edges(A); h = alpha(A, E); n = len(A); m = len(E); t = n - h
    print('%s: (4,5)=%s n=%d m=%d h=%d tau=%d I11 slack=%d' % (name, is_45_set(A), n, m, h, t, 3*n + 2*m - 11*t))
