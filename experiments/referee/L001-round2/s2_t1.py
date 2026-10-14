"""Step 2: Case T1 recomputed independently.
Coordinates scaled by 4 (all candidates lie in (1/4)Z, see review).  Candidate sets are found by a definitional SCAN:
v is a candidate for a point set Q iff for some a<b in Q the sorted triple of {v,a,b} has equal gaps.
 - P = candidates(A) \ A, P_ok = {x in P : A u {x} is (4,5)}  (full C(15,4) check)
 - h(A u {x}) for x in P_ok (brute force + ILP)
 - T1b: unordered pairs {x,y}, x in P_ok, y in candidates(A u {x}) \ (A u {x}); full C(16,4) (4,5) test; h brute+ILP
 - compare with the authors' results.json and witnesses.json
"""
import itertools, sys, time, json, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L001-round2')
from rc import *
import numpy as np

t0 = time.time()
SC = 4
A4 = [SC * a for a in ABASE]
A4set = set(A4)


def scan_candidates(Q):
    """definitional scan over all integers in [2min-max, 2max-min]; returns set of ints v not in Q
    such that {v,a,b} is a 3-AP for some a<b in Q."""
    Q = sorted(Q)
    lo, hi = Q[0], Q[-1]
    V = np.arange(2 * lo - hi - 2, 2 * hi - lo + 3, dtype=np.int64)
    hit = np.zeros(len(V), dtype=bool)
    for a, b in itertools.combinations(Q, 2):        # a < b
        hit |= (V < a) & (a - V == b - a)
        hit |= (V > a) & (V < b) & (V - a == b - V)
        hit |= (V > b) & (V - b == b - a)
    out = set(int(v) for v in V[hit]) - set(Q)
    # sanity: nothing outside the scanned range can be a candidate (|v-a| <= 2*(hi-lo) region); recheck by formula bound
    return out


P = scan_candidates(A4)
print('|P| =', len(P), ' (all in 2Z after scaling by 4, i.e. in (1/2)Z):', all(v % 2 == 0 for v in P))
Pok = sorted(v for v in P if is45(A4 + [v]))
print('|P_ok| =', len(Pok))
hAx = {}
for x in Pok:
    hb, w = hmax_brute(A4 + [x], 9)
    hi_ = hmax_ilp(A4 + [x])
    hAx[x] = (hb, hi_)
print('h(A u {x}) (brute, ilp) distribution:', {k: list(hAx.values()).count(k) for k in set(hAx.values())})

pairs = set()
for x in Pok:
    Qx = scan_candidates(A4 + [x])
    for y in Qx:
        assert y not in A4set and y != x
        pairs.add(frozenset((x, y)))
print('T1b unordered candidate pairs:', len(pairs), ' t=%.1f' % (time.time() - t0), flush=True)

good = []
for pr in sorted(pairs, key=lambda s: sorted(s)):
    x, y = sorted(pr)
    if is45(A4 + [x, y]):
        good.append((x, y))
print('(4,5) T1b pairs (full 1820-quadruple test):', len(good), ' t=%.1f' % (time.time() - t0), flush=True)

hb_dist, hi_dist = {}, {}
wit = {}
for x, y in good:
    B = A4 + [x, y]
    hb, w = hmax_brute(B, 10)
    hb_dist[hb] = hb_dist.get(hb, 0) + 1
    wit[(x, y)] = w
print('h brute-force distribution:', hb_dist, ' t=%.1f' % (time.time() - t0), flush=True)
for x, y in good:
    hi_ = hmax_ilp(A4 + [x, y])
    hi_dist[hi_] = hi_dist.get(hi_, 0) + 1
print('h ILP distribution:', hi_dist, ' t=%.1f' % (time.time() - t0), flush=True)

# both-in-P count
print('pairs with both points in P:', sum(1 for x, y in good if x in P and y in P))

# compare with authors
E = '/home/user/Erdos-757/experiments/20261014-0640-abase-extensions/'
R = json.load(open(E + 'results.json'))
st = {frozenset((int(F(a) * SC), int(F(b) * SC))) for a, b, h in R['stored']}
assert all((F(a) * SC).denominator == 1 and (F(b) * SC).denominator == 1 for a, b, h in R['stored'])
mine = {frozenset(p) for p in good}
print('stored', len(st), 'mine', len(mine), 'symmetric difference', len(st ^ mine),
      '| stored h values:', set(h for a, b, h in R['stored']))
W = json.load(open(E + 'witnesses.json'))
wp = {frozenset((int(F(w['x']) * SC), int(F(w['y']) * SC))) for w in W['pairs']}
print('witnesses.json pairs == my set:', wp == mine)
# P_ok vs witnesses generic_y list and the authors' count
wx = {int(F(w['x']) * SC) for w in W['generic_y']}
print('witnesses.json generic_y x-values == my P_ok:', wx == set(Pok))
json.dump({'scale': SC, 'P': sorted(P), 'Pok': Pok, 'good': [list(p) for p in good],
           'wit': {'%d,%d' % k: [str(v) for v in w] for k, w in wit.items()}},
          open('s2_t1_out.json', 'w'))

# T1a spot check: random generic y (large prime denominator) for each x in P_ok
rng = random.Random(20261014)
cnt = {}
for x in Pok:
    for _ in range(3):
        y = F(rng.randrange(-4000 * 1000003, 8000 * 1000003), 1000003) * SC
        B = [F(v) for v in A4] + [F(x), y]
        ok = is45(B)
        hb = hmax_brute(B, 10)[0] if ok else None
        cnt[(ok, hb)] = cnt.get((ok, hb), 0) + 1
print('T1a random generic y spot check (is45, h):', cnt)
print('time %.1fs' % (time.time() - t0))
