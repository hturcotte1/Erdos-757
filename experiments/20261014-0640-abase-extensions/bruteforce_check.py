"""Independent completeness check of K13 (no e757 / extend.py imports; plain Python integers).
All values are doubled so half-integers become integers.  Window: half-integers v/2, v in [-600, 3399].
For every unordered pair {x,y} of window values with A u {x}, A u {y}, A u {x,y} (4,5)-sets we
 (a) find a 3-AP-free 10-subset of A u {x,y} (explicit, checked: 10 points, no p+r=2q, sums distinct) -> h>=10;
     h<=10 is the trivial bound h(B)<=h(A)+2 with h(A)=8 (checked here by exhaustive subset search too);
 (b) classify the pair and, if it has a new AP involving both new points that is not a 'line-generic' pair,
     check that it is in results.json."""
import json, itertools, sys
from fractions import Fraction as F
A = [2*a for a in [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]]
AS = set(A)
n = len(A)
def dist_ok(q):
    return len({abs(p - r) for p, r in itertools.combinations(q, 2)}) >= 5
def ap_free(S):
    s = set(S); L = sorted(S)
    return not any(2*L[j] - L[i] in s for i in range(len(L)) for j in range(i+1, len(L)))
def sidon(S):
    L = sorted(S); sums = [p + q for i, p in enumerate(L) for q in L[i:]]
    return len(sums) == len(set(sums))
assert all(dist_ok(q) for q in itertools.combinations(A, 4))
S8 = [c for c in itertools.combinations(A, 8) if ap_free(c)]
assert max(len(c) for c in itertools.combinations(A, 9) if ap_free(c)) if any(ap_free(c) for c in itertools.combinations(A, 9)) else True
assert not any(ap_free(c) for c in itertools.combinations(A, 9)), 'h(A)>=9?'
print('h(A)=8 ok; maximum Sidon 8-subsets:', len(S8), flush=True)
AB = [(a, b, abs(a - b)) for a, b in itertools.combinations(A, 2)]
# P_x in doubled coordinates: values creating an AP with two A points
Px = {}
for a, b in itertools.combinations(A, 2):
    if (a + b) % 2 == 0: Px.setdefault((a + b)//2, 0); Px[(a + b)//2] += 1
    for v in (2*a - b, 2*b - a): Px.setdefault(v, 0); Px[v] += 1
def single_ok(v):
    return all(dist_ok((v,) + t) for t in itertools.combinations(A, 3))
R = json.load(open('results.json'))
stored = {frozenset((F(a), F(b))) for a, b, h in R['stored']}   # exact Fraction keys
assert len(stored) == len(R['stored'])
LO, HI = -600, 3400   # window in doubled coordinates: [LO, HI)
def in_win(q): return (2*q).denominator == 1 and LO <= 2*q < HI
stored_win = {k for k in stored if all(in_win(q) for q in k)}
matched = set()
vals = [v for v in range(LO, HI) if v not in AS and single_ok(v)]
print('valid singles', len(vals), flush=True)
IJ = [(i, j, abs(A[i]-A[j])) for i in range(n) for j in range(i+1, n)]
def pair_ok(x, y):
    d = abs(x - y)
    dx = [abs(x - a) for a in A]; dy = [abs(y - a) for a in A]
    for i, j, dab in IJ:
        if len({d, dx[i], dx[j], dy[i], dy[j], dab}) < 5: return False
    return True
S8set = [(c, set(c)) for c in S8]
def witness(x, y):
    for c, s in S8set:
        # new APs can only involve x or y; test the 10-set directly
        T = c + (x, y)
        if ap_free(T): return T
    for T in itertools.combinations(A + [x, y], 10):   # fallback exhaustive
        if ap_free(T): return T
    return None
Pxs = {v for v in Px if v not in AS}
npairs = nclass = nline = nmiss = nwitfail = 0
total45 = 0
for x, y in itertools.combinations(vals, 2):
    if not pair_ok(x, y): continue
    total45 += 1
    T = witness(x, y)
    if T is None or len(T) != 10 or not ap_free(T) or not sidon(T) or not set(T) <= AS | {x, y}:
        nwitfail += 1; print('WITNESS FAIL', x/2, y/2); continue
    # classification: cross APs containing both x and y
    cross = sum(1 for a in A if 2*a == x + y) + sum(1 for a in A if 2*x == a + y) + sum(1 for a in A if 2*y == a + x)
    kxx = x in Pxs; kyy = y in Pxs
    inx = kxx or cross > 0; iny = kyy or cross > 0
    if not (inx and iny): continue          # a new point in no AP (generic) -- covered by T1a/T0
    if not kxx and not kyy and cross == 1:
        nline += 1; continue                # generic point of a T2 line: witness checked above
    npairs += 1
    key = frozenset((F(x, 2), F(y, 2)))
    if key in stored: matched.add(key)
    if key not in stored:
        nmiss += 1
        if nmiss < 10: print('NOT STORED', x/2, y/2)
print('both-points-in-APs (4,5) pairs:', npairs + nline)
print('(4,5) pairs total', total45, '| witness failures', nwitfail, '| non-line-generic pairs with both points in APs', npairs,
      '| missing from stored', nmiss, '| line-generic (4,5) pairs (all witnessed)', nline, '| stored total', len(stored), '| stored in window', len(stored_win), '| stored matched', len(matched), '| stored-in-window not matched', len(stored_win - matched))
