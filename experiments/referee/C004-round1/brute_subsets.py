"""Brute-force cross-check (n <= 22) of the exact VE solver on induced subsets of the C004 set itself
(random subsets, windows in sorted order, neighbourhoods of the new AP) and on family members with n <= 22."""
import json
import random
import sys
import time

sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C004-round1')
import reflib as R  # noqa: E402

A = sorted(R.as_int_list(R.load_claim('/home/user/Erdos-757/results/claims/C004-lemmaE-SK5-E1.json')['set']))
n = len(A)
rng = random.Random(757)
subs = []
for s in range(0, n - 22 + 1, 6):
    subs.append(('window%d' % s, A[s:s + 22]))
for t in range(10):
    subs.append(('rand%d' % t, sorted(rng.sample(A, 22))))
# the new AP {0, a, 2a} together with the 19 smallest remaining points (the densest region)
subs.append(('newAP+19', sorted(set([A[0], A[1], A[-1]] + A[2:21]))))
res = []
t0 = time.time()
for name, S in subs:
    forb, census = R.forbidden_sets(S)
    ve, w, I = R.ve_max_independent(len(S), forb)
    bm, cnt = R.brute_max(len(S), forb)
    rec = dict(name=name, n=len(S), m=census.get(3, 0), four=census.get(4, 0), ve=ve, brute=bm, agree=ve == bm)
    res.append(rec)
    print(rec, flush=True)
print('all agree:', all(r['agree'] for r in res), f'({time.time()-t0:.1f}s)')
json.dump(res, open('/home/user/Erdos-757/experiments/referee/C004-round1/brute_subsets.json', 'w'), indent=1)
