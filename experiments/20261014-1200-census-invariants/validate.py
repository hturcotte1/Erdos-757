import json, os, sys, time
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir('/home/user/Erdos-757')
from invariants import TIERS
from e757 import sat_indep, cpsat_extra
from e757.saturated import map_of_set
rec = json.load(open('data/small_records.json'))['sets']
def pattern(A):
    lo, hi, mid = map_of_set(A)
    return tuple(sorted((a, j, c) for j, (a, c) in mid.items()))
p10 = pattern(rec['10']['set']); print('n=10 record pattern', p10, flush=True)
res = {}
for tier in ('t1', 't2'):
    ex = TIERS[tier]
    # n=10: the record pattern (or its reflection) must satisfy the invariants: force all its edges (+ complement edges false)
    from itertools import combinations
    refl = tuple(sorted((9 - k, 9 - j, 9 - i) for (i, j, k) in p10))
    for name, pat in (('rec', p10), ('refl', refl)):
        fixed = [(t, True) for t in pat] + [(t, False) for t in combinations(range(10), 3) if t not in set(pat)]
        t0 = time.time()
        s_, e_ = sat_indep.decide(10, 6, 8, extra=ex, gl_constraints='LR', extra_unit=fixed, time_limit=300)
        res['%s_n10_%s_forced' % (tier, name)] = s_
        print(tier, 'n=10 record pattern forced', name, s_, round(time.time() - t0, 1), flush=True)
    for n, T, m in ((12, 7, 10), (14, 8, 12)):
        for eng in ('glucose4', 'cpsat'):
            if tier == 't2' and n == 12:
                continue   # t2 is sample-based (n=14) and false for many n=12 patterns
            t0 = time.time()
            if eng == 'cpsat':
                s, e, _ = cpsat_extra.feasible(n, T, m, extra=ex, time_limit=900, workers=2)
            else:
                s, e = sat_indep.decide(n, T, m, extra=ex, gl_constraints='LR', time_limit=900)
            print(tier, n, T, m, eng, s, round(time.time()-t0,1), flush=True)
            res['%s_%d_%s' % (tier, n, eng)] = s
json.dump(res, open('validation.json', 'w'), indent=1)
