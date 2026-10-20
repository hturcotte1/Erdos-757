"""Referee L011 round 3: the witness C22 from the definitions, exact integers only.  (1) C22 = B12 u (5000 + 15*B10) with B12, B10 from
data/small_records.json; (2) 22 distinct points; (3) every 4-subset has >= 5 distinct |differences|; (4) h(C22) = 13 by two methods:
(a) brute force over all 14-subsets and 13-subsets with the Sidon definition (all sums x+y, x<=y, distinct);
(b) maximum independent set of the 'conflict' hypergraph: forbidden sets {x,y,z,w} with x+y=z+w, {x,y}!={z,w} (3 or 4 points), by
branch and bound; (5) h/n vs 4/7 with Fraction."""
import itertools, json, sys
from fractions import Fraction
rec = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
B12 = rec['12']['set']; B10 = rec['10']['set']
C22 = sorted(B12 + [5000 + 15 * b for b in B10])
stated = [0,269,385,467,501,511,521,523,535,538,549,575,5000,5750,6095,6200,6305,6440,6500,6680,6905,7610]
print('C22 == stated set:', C22 == stated, '| distinct:', len(set(C22)) == 22 == len(C22))
bad4 = sum(1 for q in itertools.combinations(C22, 4) if len({abs(a - b) for a, b in itertools.combinations(q, 2)}) < 5)
print('4-subsets with < 5 distinct differences:', bad4, 'of', sum(1 for _ in itertools.combinations(C22, 4)))
def sidon(S):
    sums = [x + y for i, x in enumerate(S) for y in S[i:]]
    return len(sums) == len(set(sums))
n14 = sum(1 for S in itertools.combinations(C22, 14) if sidon(S))
n13 = sum(1 for S in itertools.combinations(C22, 13) if sidon(S))
print('Sidon 14-subsets:', n14, '| Sidon 13-subsets:', n13)
# conflict structure
idx = {x: i for i, x in enumerate(C22)}
forb = set()
pairs = list(itertools.combinations(range(22), 2))
bysum = {}
for i, j in pairs: bysum.setdefault(C22[i] + C22[j], []).append((i, j))
for s, L in bysum.items():
    for (a, b), (c, d) in itertools.combinations(L, 2): forb.add(frozenset((a, b, c, d)))
sizes = sorted(len(f) for f in forb)
print('forbidden sets (equal sums of distinct pairs):', len(forb), 'sizes:', dict((k, sizes.count(k)) for k in set(sizes)))
aps = [(a, b, c) for a, b, c in itertools.combinations(C22, 3) if a + c == 2 * b]
print('3-term APs:', len(aps), '| midpoints distinct:', len({b for _, b, _ in aps}) == len(aps))
forbm = [sum(1 << v for v in f) for f in forb]
best = [0]
def bb(i, chosen, cnt):
    if cnt + (22 - i) <= best[0]: return
    if i == 22: best[0] = max(best[0], cnt); return
    c2 = chosen | (1 << i)
    if all((f & c2) != f for f in forbm): bb(i + 1, c2, cnt + 1)
    bb(i + 1, chosen, cnt)
bb(0, 0, 0)
print('max independent set of the conflict structure (branch and bound):', best[0])
S13 = [0, 269, 385, 467, 511, 521, 523, 5000, 5750, 6095, 6200, 6680, 6905]
print("certificate's 13-subset is Sidon and inside C22:", sidon(S13) and set(S13) <= set(C22))
h = 13
print('h/n =', Fraction(h, 22), '>= 4/7:', Fraction(h, 22) >= Fraction(4, 7), '| ceil(4n/7) =', -(-88 // 7))
print('(n,m,tau) = (22,%d,%d), slack 3n+2m-11tau =' % (len(aps), 22 - h), 66 + 2 * len(aps) - 11 * (22 - h))
json.dump({'id': 'L011R3-witness-c22', 'type': 'construction', 'set': C22, 'claimed_h': 13, 'witness_sidon_subset': S13,
           'notes': 'referee round 3 scratch copy of the L011 witness; not a record claim'}, open('out/L011R3-witness-c22.json', 'w'))
