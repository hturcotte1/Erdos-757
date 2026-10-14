"""Referee L001, case T1: independent enumeration. Writes t1_out.json."""
import json, sys, time
from fractions import Fraction as Fr
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001')
from rcore import A_BASE, is45, three_aps, max_sidon, ap_partners

t0 = time.time()
A = [Fr(a) for a in A_BASE]
Aset = set(A)
P = ap_partners(A)
print('|P| =', len(P))
# each v in P really lies in a 3-AP of A u {v} (direct triple scan)
assert all(any(v in t for t in three_aps(A + [v])) for v in P)
P_ok = sorted(v for v in P if is45(A + [v]))
print('|P_ok| =', len(P_ok), 'time', round(time.time() - t0, 1))
# T1a: h(A u {x}) for each x in P_ok
hAx = {}
for x in P_ok:
    h, W = max_sidon(A + [x])
    hAx[x] = h
print('h(A u {x}) distribution:', {h: sum(1 for v in hAx.values() if v == h) for h in set(hAx.values())})
# T1b: unordered pairs {x,y}, x in P_ok, y in ap_partners(A u {x})
pairs = set()
for x in P_ok:
    for y in ap_partners(A + [x]):
        assert y not in Aset and y != x
        pairs.add(frozenset((x, y)))
print('T1b candidate unordered pairs:', len(pairs), 'time', round(time.time() - t0, 1), flush=True)
good = []
for k in sorted(pairs, key=lambda s: sorted(s)):
    x, y = sorted(k)
    if is45(A + [x, y]):
        good.append((x, y))
print('(4,5) pairs:', len(good), 'time', round(time.time() - t0, 1), flush=True)
hd = {}
out = []
for x, y in good:
    h, W = max_sidon(A + [x, y])
    hd[h] = hd.get(h, 0) + 1
    out.append([str(x), str(y), h, [str(w) for w in W]])
print('h distribution over (4,5) pairs:', hd, 'time', round(time.time() - t0, 1))
# compare with stored results.json
R = json.load(open('/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/results.json'))
stored = {frozenset((Fr(a), Fr(b))) for a, b, h in R['stored']}
mine = {frozenset((x, y)) for x, y in good}
print('stored', len(stored), 'mine', len(mine), 'stored-mine', len(stored - mine), 'mine-stored', len(mine - stored))
# how many (4,5) pairs have both points in P (i.e. reached from both sides)
both = sum(1 for x, y in good if x in P and y in P)
print('(4,5) pairs with both points in P:', both)
json.dump({'P': sorted(str(v) for v in P), 'P_ok': [str(v) for v in P_ok],
           'hAx': {str(k): v for k, v in hAx.items()}, 'n_pairs': len(pairs),
           'good': out}, open('/home/user/Erdos-757/experiments/referee/L001/t1_out.json', 'w'))
print('done', round(time.time() - t0, 1))
