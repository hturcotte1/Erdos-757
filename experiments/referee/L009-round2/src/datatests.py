"""Referee L009 round 2: numerical tests of Theorem 3 (I11: 11 tau <= 3n+2m for n <= 18) and Theorem 1 (tau <= 7 at n = 18) on the
AP hypergraphs of real (4,5)-sets: A_base and all its subsets, the small records and all their subsets, Fibonacci sets, the 2,910
census 14-point sets (+ deletions), the 54,243 extremal 12-point sets, the 2,337 15-point sets of data/ext15_sets, A_18 and all its
subsets, and generic gluings.  Own code only (no e757, no judge)."""
import json, gzip, itertools, random, sys
from fractions import Fraction
random.seed(20261017)
def aps(A):
    A = sorted(A); idx = {a: i for i, a in enumerate(A)}; E = []
    for i in range(len(A)):
        for k in range(i + 2, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 and s // 2 in idx: E.append((1 << i) | (1 << idx[s // 2]) | (1 << k))
    return E
def cover_le(E, k):
    if not E: return True
    if k == 0: return False
    used = 0; c = 0
    for e in E:
        if not e & used: used |= e; c += 1
        if c > k: return False
    e = E[0]
    while e:
        x = e & -e; e ^= x
        if cover_le([f for f in E if not f & x], k - 1): return True
    return False
def tau(E):
    k = 0
    while not cover_le(E, k): k += 1
    return k
def is45(A):
    for q in itertools.combinations(A, 4):
        if len({abs(a - b) for a, b in itertools.combinations(q, 2)}) < 5: return False
    return True
stats = {}
worst = {}
def test(name, A, check45=False):
    A = sorted(A); n = len(A)
    if check45 and not is45(A): return False
    E = aps(A); m = len(E); t = tau(E); s = 3 * n + 2 * m - 11 * t
    st = stats.setdefault(name, [0, 0, 99, None, 0]); st[0] += 1
    if s < 0: st[1] += 1; print("I11 VIOLATION", name, A, n, m, t, s)
    if s < st[2]: st[2] = s; st[3] = (n, m, t)
    if n == 18 and t >= 8: st[4] += 1; print("TAU>=8 at n=18", name, A)
    return True
def subsets(A, kmin=3):
    for r in range(kmin, len(A) + 1):
        for S in itertools.combinations(A, r): yield S
SR = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
Abase = SR['14']['set']
assert sorted(Abase) == [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
for S in subsets(Abase): test('A_base subsets', S)
for key in ('8', '10', '11', '12', '12b', '12c'):
    for S in subsets(SR[key]['set']): test('small_records[%s] subsets' % key, S)
fib = [2, 3]
while len(fib) < 18: fib.append(fib[-1] + fib[-2])
print("Fibonacci 2..%d is a (4,5)-set:" % fib[-1], is45(fib))
for i in range(18):
    for j in range(i + 3, 19): test('Fibonacci windows', fib[i:j])
for _ in range(20000):
    r = random.randint(6, 18); test('Fibonacci random subsets', random.sample(fib, r))
for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt'):
    A = json.loads(l)['set']; test('census14 full', A)
    for x in A: test('census14 minus a point', [a for a in A if a != x])
    for _ in range(10): test('census14 random subsets', random.sample(A, random.randint(5, 13)))
for l in gzip.open('/home/user/Erdos-757/data/ext12_all_rows.jsonl.gz', 'rt'):
    test('ext12 (54,243 extremal 12-point sets)', json.loads(l)['set'])
for l in gzip.open('/home/user/Erdos-757/data/ext15_sets.jsonl.gz', 'rt'):
    A = json.loads(l)['set']; test('ext15 full', A)
    for x in A: test('ext15 minus a point', [a for a in A if a != x])
A18 = [0,352,492,600,632,704,916,1200,1264,1388,1613,1696,1767,1838,2176,2476,4352,7440]
for S in subsets(A18, 10): test('A_18 subsets of size >= 10', S)
# generic gluings X u (qY + t), q = p1/p2 with random large primes, t large; kept only if the union is a (4,5)-set
pool = [Abase, SR['12']['set'], SR['12b']['set'], SR['12c']['set'], SR['11']['set'], SR['10']['set'], SR['8']['set'], fib[:8], A18]
primes = [1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097]
ng = 0
for _ in range(400):
    X = random.choice(pool); Y = random.choice(pool)
    nx = random.randint(4, min(14, len(X))); ny = random.randint(4, min(18 - nx, len(Y))) if 18 - nx >= 4 else 0
    if ny == 0: continue
    Xs = sorted(random.sample(X, nx)); Ys = sorted(random.sample(Y, ny))
    p1, p2 = random.sample(primes, 2)
    t = 10 ** 7 + random.randint(0, 10 ** 5)
    Z = Xs + [Fraction(p1 * y, p2) + t for y in Ys]
    Z = [z * p2 for z in Z]; Z = [int(z) for z in Z]
    if len(set(Z)) != len(Z): continue
    if test('gluings n<=18', Z, check45=True): ng += 1
print("gluings tested:", ng)
print("\nSUMMARY name: graphs | I11 violations | min slack (n,m,tau at min) | n=18 with tau>=8")
for k, v in stats.items(): print("  %-40s %8d | %d | %d %s | %d" % (k, v[0], v[1], v[2], v[3], v[4]))
