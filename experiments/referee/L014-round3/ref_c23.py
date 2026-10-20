"""Referee (L014 round 3): exact integer verification of the witness C23 (Theorem 2), with no repository code."""
import itertools, json
C23 = [0,269,385,467,501,511,521,523,535,538,549,575,1000000000,16909350190,23979971882,27868723536,28399336131,30343711958,30696250000,31050593574,31757475190,32818700380,60392500000]
A = sorted(C23); n = len(A); assert n == 23 and len(set(A)) == 23
# construction check against data/small_records.json
rec = json.load(open('/home/user/Erdos-757/data/small_records.json'))
B12 = [0,269,385,467,501,511,521,523,535,538,549,575]
cands = []
def walk(o):
    if isinstance(o, dict):
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        if o and all(isinstance(x, int) for x in o) and len(o) == 11: cands.append(sorted(o))
        else:
            for v in o: walk(v)
walk(rec)
match = [b for b in cands if sorted(B12 + [10**9 + 7919 * x for x in b]) == A]
print('construction B12 u (1e9 + 7919*B11) matches an 11-point set of data/small_records.json:', len(match) > 0, match[:1])
# (4,5)-set: every 4-subset has >= 5 distinct absolute differences
bad = 0; nsub = 0
for Q in itertools.combinations(A, 4):
    nsub += 1
    diffs = set(abs(x - y) for x, y in itertools.combinations(Q, 2))
    if len(diffs) < 5: bad += 1
print('4-subsets', nsub, 'with < 5 distinct differences:', bad)
# weak Sidon: sums x+y (x<y) distinct
sums = [x + y for x, y in itertools.combinations(A, 2)]
print('weak Sidon (all x+y, x<y, distinct):', len(sums) == len(set(sums)))
# 3-APs
idx = {x: i for i, x in enumerate(A)}
aps = []
for i in range(n):
    for j in range(i + 1, n):
        for k in range(j + 1, n):
            if A[i] + A[k] == 2 * A[j]: aps.append((i, j, k))
print('3-term APs:', len(aps))
E = [(1 << i) | (1 << j) | (1 << k) for (i, j, k) in aps]
# tau by own exact branching
def cover_le(chosen, k):
    for e in E:
        if not (e & chosen):
            if k <= 0: return False
            return any(cover_le(chosen | (1 << v), k - 1) for v in (i for i in range(n) if e >> i & 1))
    return True
tau = 0
while not cover_le(0, tau): tau += 1
print('tau (branching) =', tau)
# brute force: no cover of size tau-1 (all subsets), some cover of size tau
full = (1 << n) - 1
def is_cover(S): return all(e & S for e in E)
cnt_small = sum(1 for S in itertools.combinations(range(n), tau - 1) if is_cover(sum(1 << v for v in S)))
print('covers of size %d (all C(23,%d) subsets):' % (tau - 1, tau - 1), cnt_small)
# a maximum 3-AP-free subset = complement of a minimum cover; verify it is Sidon by definition
def find_cover(chosen, k):
    for e in E:
        if not (e & chosen):
            if k <= 0: return None
            for v in range(n):
                if e >> v & 1:
                    r = find_cover(chosen | (1 << v), k - 1)
                    if r is not None: return r
            return None
    return chosen
cov = find_cover(0, tau); S = [A[i] for i in range(n) if not (cov >> i & 1)]
d = [abs(x - y) for x, y in itertools.combinations(S, 2)]
print('Sidon subset of size', len(S), 'all differences distinct:', len(d) == len(set(d)), S)
# every subset of size n - tau + 1 contains a 3-AP (equivalently no cover of size tau - 1): already shown by brute force above.
# Also direct definitional check that no 15-subset is Sidon would be C(23,15)=490314 subsets: do it.
big = 0
for Q in itertools.combinations(range(n), n - tau + 1):
    m = sum(1 << v for v in Q)
    if not any((e & m) == e for e in E): big += 1
print('3-AP-free subsets of size %d (brute force over C(23,%d)):' % (n - tau + 1, n - tau + 1), big)
print('h(C23) =', n - tau, '; 14/23 =', 14 / 23, '>= 4/7:', 14 * 7 >= 4 * 23)
