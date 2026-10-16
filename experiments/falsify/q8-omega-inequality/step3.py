import json, sys, time, collections, itertools
from q8lib import *
from e757.anneal import is45_ints
d = json.load(open(os.path.join(HERE, '..', '..', '..', 'data', 'small_records.json')))['sets']
base = {'base': d['14']['set'], 'a12': d['12']['set'], 'b12': d['12b']['set'], 'c12': d['12c']['set']}
def build(A, B, x, y, q, t=None):
    """amalgam: identify A[x] with B[y] (t None), B scaled by q; or disjoint union with shift t."""
    if t is None:
        pts = set(A) | {A[x] + q * (b - B[y]) for b in B}
    else:
        pts = set(A) | {q * b + t for b in B}
    return sorted(pts)
cases = []; meta = []
def ok(C, A, B, qa=None):
    if len(C) != len(A) + len(B) - (1 if qa else 0): return False
    if len(C) > 31: return False
    return is45_ints(C)
cid = 0; stats = collections.Counter()
# disjoint unions
for (na, A), (nb, B) in itertools.product(base.items(), repeat=2):
    for q in (4099, -4099, 7919):
        C = build(A, B, 0, 0, q, t=10**6 + 17)
        stats['union_tried'] += 1
        if ok(C, A, B): cases.append((cid, len(C), masks_of(C), 1, 3, 0)); meta.append(('union', na, nb, q, C)); cid += 1; stats['union_ok'] += 1; break
        else: stats['union_fail_q'] += 1
# amalgams at one vertex
seen = set()
for (na, A), (nb, B) in itertools.product(base.items(), repeat=2):
    for x in range(len(A)):
        for y in range(len(B)):
            for q in (4099, -4099, 8209, -8209, 12007):
                C = build(A, B, x, y, q)
                stats['amal_tried'] += 1
                if tuple(C) in seen: break
                if ok(C, A, B, 1):
                    seen.add(tuple(C)); cases.append((cid, len(C), masks_of(C), 1, 3, 0)); meta.append(('amalgam', na, nb, (x, y, q), C)); cid += 1; stats['amal_ok'] += 1; break
            else: stats['amal_nofit'] += 1
print(dict(stats), 'cases', len(cases), flush=True)
t = time.time()
res = run_cases(cases, vcap=50)
tot = collections.Counter(); hist = collections.Counter(); bad = []
for i, r in res.items():
    for k in ('states','violQ','violAct','violD4','eqQ'): tot[k] += r[k]
    for s, c in r['hist']['Q'].items(): hist[s] += c
    if r['violQ'] or r['violAct']: bad.append((i, meta[i][:4], r['viol'][:5]))
print(dict(tot), 'min slack', min(hist), 'time', time.time() - t, flush=True)
# second pass: random larger D on amalgams
cases2 = [(c[0], c[1], c[2], 2, 5000, c[0] + 11) for c in cases]
res2 = run_cases(cases2, vcap=50); tot2 = collections.Counter(); hist2 = collections.Counter()
for i, r in res2.items():
    for k in ('states','violQ','violAct','violD4','eqQ'): tot2[k] += r[k]
    for s, c in r['hist']['Q'].items(): hist2[s] += c
    if r['violQ'] or r['violAct']: bad.append((i, meta[i][:4], r['viol'][:5]))
print(dict(tot2), 'min slack', min(hist2), flush=True)
json.dump(dict(stats=dict(stats), tot=dict(tot), tot_rand=dict(tot2), minslack=[min(hist), min(hist2)], bad=bad,
               hist_lowest=sorted(hist.items())[:8],
               cases=[(m[0], m[1], m[2], m[3], m[4]) for m in meta]), open(os.path.join(HERE, 'step3_results.json'), 'w'))
