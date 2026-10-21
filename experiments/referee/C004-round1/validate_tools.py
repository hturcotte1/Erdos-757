"""Validate the referee tools on small instances against brute force, and rebuild the reader's family S_K
(O = {0,49,75,83,98,101,117,119,121,159,269}, phi(x) = 101 + 18x/269) to check the provenance of the claim set."""
import itertools
import json
import random
import sys
import time
from fractions import Fraction

sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402
from pysat.solvers import Solver  # noqa: E402

out = {'instances': []}


def sat_max(A, forb):
    n = len(A)
    best = 0
    for k in range(1, n + 1):
        cnf, top = R.sidon_cnf(n, forb, k)
        with Solver(name='minisat22', bootstrap_with=cnf) as s:
            if s.solve():
                m = s.get_model()
                ch = [A[v] for v in range(n) if m[v] > 0]
                assert R.is_sidon_sums(ch) and len(ch) >= k
                best = k
            else:
                break
    return best


def run(name, A, expect=None, defn_brute=True):
    A = sorted(A)
    n = len(A)
    t = time.time()
    ok45, mind, n5, bad, tot = R.is45_literal(A) if n >= 4 else (True, None, 0, None, 0)
    forb, census = R.forbidden_sets(A)
    ve, w, I = R.ve_max_independent(n, forb)
    assert R.check_independent(I, forb) and len(I) == ve and R.is_sidon_sums([A[i] for i in I])
    bm, cnt = R.brute_max(n, forb) if n <= 22 else (None, None)
    bd = R.brute_max_by_definition(A) if (defn_brute and n <= 14) else None
    sm = sat_max(A, forb)
    agree = (ve == sm) and (bm is None or bm == ve) and (bd is None or bd == ve) and (expect is None or expect == ve)
    rec = dict(name=name, n=n, is45=ok45, census=census, h_ve=ve, width=w, h_brute_forb=bm, n_max_sets=cnt,
               h_brute_def=bd, h_sat=sm, expect=expect, agree=agree, secs=round(time.time() - t, 2))
    print(rec, flush=True)
    out['instances'].append(rec)
    return rec


# 1. records on disk
recs = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
for key, v in recs.items():
    run('record_' + key, v['set'], expect=v['h'])
# third 12-point set from START_HERE section 6
run('12pt_third', [0, 269, 385, 467, 501, 511, 521, 523, 535, 538, 549, 575], expect=7)

# 2. Fibonacci prefixes {2,3,5,8,...}
fib = [2, 3]
while len(fib) < 22:
    fib.append(fib[-1] + fib[-2])
for k in (8, 12, 16, 20, 22):
    run(f'fib{k}', fib[:k], defn_brute=(k <= 12))

# 3. negative controls for the (4,5) test
for name, S in (('1235', [1, 2, 3, 5]), ('0123', [0, 1, 2, 3]), ('AP5', [0, 1, 2, 3, 4]),
                ('parallelogram', [0, 1, 10, 11])):
    ok45 = R.is45_literal(S)[0]
    print('negative control', name, 'is45 =', ok45)
    out.setdefault('neg45', {})[name] = ok45

# 4. random sets with many sum collisions (NOT weak Sidon): checks the general forbidden-set logic
rng = random.Random(20261021)
for trial in range(14):
    nn = rng.randint(8, 14)
    S = rng.sample(range(0, 3 * nn), nn)
    run(f'rand_dense_{trial}', S, defn_brute=True)

# 5. random (4,5)-sets from small ranges (many 3-APs), n up to 22
for trial in range(8):
    target = rng.choice([16, 18, 20, 22])
    S = []
    pool = list(range(0, 400))
    rng.shuffle(pool)
    for x in pool:
        T = sorted(S + [x])
        # incremental (4,5) test: only 4-sets containing x
        okx = True
        for q in itertools.combinations([y for y in S], 3):
            Q = q + (x,)
            ds = {abs(a - b) for a, b in itertools.combinations(Q, 2)}
            if len(ds) < 5:
                okx = False
                break
        if okx:
            S.append(x)
        if len(S) == target:
            break
    run(f'rand45_{trial}', S, defn_brute=False)

# 6. the reader's family S_K and its Lemma-E extension
O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]


def S_K(K):
    pts = set(Fraction(x) for x in O)
    cur = [Fraction(x) for x in O]
    for _ in range(K):
        cur = [Fraction(101) + Fraction(18, 269) * x for x in cur]
        pts |= set(cur)
    scale = 269 ** K
    ints = sorted(int(x * scale) for x in pts)
    assert all((x * scale).denominator == 1 for x in pts)
    return ints


fam = {}
for K in range(0, 6):
    S = S_K(K)
    n = len(S)
    forb, census = R.forbidden_sets(S)
    h, w, _ = R.ve_max_independent(n, forb)
    # universality of min and max: alpha(H - v) = h - 1
    def alpha_minus(v):
        keep = [i for i in range(n) if i != v]
        mp = {i: j for j, i in enumerate(keep)}
        f2 = [tuple(mp[i] for i in F) for F in forb if v not in F]
        return R.ve_max_independent(n - 1, f2)[0]
    amin, amax = alpha_minus(0), alpha_minus(n - 1)
    ok45 = R.is45_literal(S)[0] if n <= 60 else None
    rec = dict(K=K, n=n, n_expected=11 + 9 * K, m=census.get(3, 0), four=census.get(4, 0), h=h,
               h_expected=7 + 5 * K, alpha_minus_min=amin, alpha_minus_max=amax, is45=ok45, width=w)
    # Lemma-E extension at the min with the experiment's t
    span = S[-1] - S[0]
    t1 = 3 * span + 1000003
    E1 = sorted([S[0] - t1, S[0] + t1] + S)
    E1 = [x - E1[0] for x in E1]
    fE, cE = R.forbidden_sets(E1)
    hE, _, _ = R.ve_max_independent(len(E1), fE)
    rec.update(E1_n=len(E1), E1_h=hE, E1_m=cE.get(3, 0), E1_four=cE.get(4, 0), E1_is45=R.is45_literal(E1)[0])
    fam[K] = (S, E1)
    print('family', rec, flush=True)
    out.setdefault('family', []).append(rec)

claim = sorted(R.as_int_list(R.load_claim('/home/user/Erdos-757/results/claims/C004-lemmaE-SK5-E1.json')['set']))
S5, E1_5 = fam[5]
print('claim set == translate(S_5 u {min - t, min + t}) with t = 3*span + 1000003:', claim == E1_5)
print('span(S_5) == 269^6:', S5[-1] - S5[0] == 269 ** 6)
out['claim_equals_E1_K5'] = claim == E1_5
with open('/home/user/Erdos-757/experiments/referee/C004-round1/validate_tools.json', 'w') as fh:
    json.dump(out, fh, indent=1, default=str)
print('ALL AGREE:', all(r['agree'] for r in out['instances']))
