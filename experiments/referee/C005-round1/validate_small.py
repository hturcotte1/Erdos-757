"""Validate own tools (4-subset test, forbidden-set extraction, frontier DP, SAT encoding) against
brute force from the definitions on small instances."""
import sys, json, random, itertools, time
from fractions import Fraction
sys.path.insert(0, '.')
from common import *
from sat_check import decide

def h_bruteforce_definition(A):
    """Largest Sidon subset by enumerating subsets in decreasing size, testing the sum definition only."""
    n = len(A)
    for k in range(n, 0, -1):
        for S in itertools.combinations(A, k):
            if is_sidon_def(S):
                return k
    return 0

def run(name, A, defbf=True):
    A = sorted(A); n = len(A)
    ok45 = four_subset_literal(A)[0]
    F, _ = forbidden_sets_from_sums(A)
    Fd = forbidden_sets_from_diffs(A)
    assert F == Fd, name
    bf = alpha_bruteforce(n, F)
    d1, w1, _ = alpha_frontier_dp(n, F, greedy_order(n, F))
    d2, w2, _ = alpha_frontier_dp(n, F, list(range(n)))
    rnd = list(range(n)); random.shuffle(rnd)
    d3, w3, _ = alpha_frontier_dp(n, F, rnd)
    for w in (w1, w2, w3):
        assert is_sidon_def([A[i] for i in w]), name
    hdef = h_bruteforce_definition(A) if defbf else None
    s1 = decide(A, bf)[0]; s2 = decide(A, bf + 1)[0] if bf < n else False
    agree = (bf == d1 == d2 == d3) and (hdef is None or hdef == bf) and s1 and not s2
    print(f'{name:28s} n={n:2d} (4,5)={ok45!s:5s} |F|={len(F):3d} sizes={sorted(set(len(f) for f in F))} '
          f'h_bf={bf} h_def={hdef} dp={d1},{d2},{d3} sat(h)={s1} sat(h+1)={s2} AGREE={agree}')
    assert agree, name
    return ok45, bf

random.seed(20261021)
t0 = time.time()
# 4-subset test sanity on non-(4,5) sets
for B in ([1, 2, 3, 5], [0, 1, 2, 3], [0, 1, 3, 4], [2, 3, 5, 8]):
    print('4-subset test', B, four_subset_literal(B)[0])
d = json.load(open('/home/user/Erdos-757/data/small_records.json'))
for key, rec in d['sets'].items():
    A = [int(x) for x in rec['set']]
    exp = rec.get('h')
    ok, h = run(f'small_records[{key}] h_exp={exp}', A, defbf=len(A) <= 14)
    assert ok and h == exp, key
Abase = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
run('A_base (h=8 expected)', Abase)
run('12pt third set (h=7)', [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575])
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]
run('O (h=7 expected)', O)
I1 = sorted(set([269 * x for x in O] + [269 * 101 + 18 * x for x in O]))
run('I_1 = 269*S_1 (h=12 exp)', I1, defbf=False)
t = 3 * (max(I1) - min(I1)) + 1000003
E1_1 = sorted(set([x + t for x in I1] + [0, 2 * t]))
run('E1(S_1) (h=13 exp)', E1_1, defbf=False)
fib = [2, 3]
while len(fib) < 20:
    fib.append(fib[-1] + fib[-2])
for k in (6, 10, 14, 18, 20):
    run(f'Fibonacci F3..(k={k})', fib[:k], defbf=k <= 14)
# random induced subsets of the claim set
raw, pts = load_claim('/home/user/Erdos-757/results/claims/C005-lemmaE-SK6-E1.json')
C = sorted(pts)
for r in range(12):
    k = random.choice([12, 14, 16, 18, 20, 22])
    start = random.randrange(0, len(C) - k)
    sub = C[start:start + k] if r % 2 == 0 else random.sample(C, k)
    run(f'claim subset #{r} (k={k})', sub, defbf=k <= 14)
# random small integer sets (with parallelogram relations, size-4 forbidden sets)
for r in range(12):
    k = random.randint(6, 14)
    A = random.sample(range(0, 60), k)
    run(f'random int set #{r}', A, defbf=k <= 12)
print(f'all validations agree ({time.time()-t0:.1f}s)')
