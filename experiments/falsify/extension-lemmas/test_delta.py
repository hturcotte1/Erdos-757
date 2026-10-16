"""Lemma Delta checks: (a) arithmetic, (b) k=1 exclusion: for sets A in the 14-point census,
all one-point extensions A+{x} with exactly one new AP (x in role mid / left end / right end with partner a,b in A),
compute m, h; HY says h>=9 whenever A+{x} is (4,5) with m=13. (c) the 'other' k=1 case: new edge {a,x,y} with x middle,
y=2x-a (x generic): h(C) vs universal-ness of a."""
import sys, json, gzip, random, itertools
from fractions import Fraction
sys.path.insert(0, '/home/user/Erdos-757'); sys.path.insert(0, '.')
from falsify import HG, ROOT, pr
from e757.core import ap_edges, is_45_set
rng = random.Random(5)
# (a) arithmetic
assert 17*7 == 119 and 5*16+3*13 == 119 and 5*16+3*14 == 122   # HY on C: tau=7 => m>=13  (3m >= 39)
assert 17*7 > 5*16 + 3*12 and 17*7 <= 5*16 + 3*13
assert 17*6 == 102 and 5*15 == 75 and 3*(13-4) + 75 >= 102 and 3*(13-5)+75 < 102 and 3*(14-5)+75 >= 102 and 3*(14-6)+75 < 102
assert 5*14 + 3*(13-1) == 106 and 17*7 == 119 > 106          # text's inequality (U for x, deg x = 1)
assert 5*15 + 3*13 == 114 < 119                                # HY applied directly to A+{x}: tau=7 impossible
assert 5*13 + 3*12 == 101 < 102                                # U1
assert 5*16 + 3*14 - 17*7 == 3                                 # slack 3 for k=2
pr('arithmetic ok')
L = [json.loads(l) for l in gzip.open(ROOT + 'data/census_n14_m12_classes.jsonl.gz', 'rt')]
sample = [r['set'] for r in rng.sample(L, 60)] + [json.load(open(ROOT+'data/small_records.json'))['sets']['14']['set']]
stats = dict(cand=0, is45=0, m13=0, h_by={}, h8=0, ext_total=0)
univ_edge_case = dict(total=0, bad=[])
for S in sample:
    A = sorted(S); H = HG(A); assert H.alpha == 8 and H.m == 12
    U = H.universal(); pr('set', A[:3], 'universal vertices', U)
    As = set(A); seen = set()
    for a, b in itertools.permutations(A, 2):
        for x in (2*a - b, Fraction(a+b, 2)):     # a midpoint of (x,b);  x midpoint of (a,b)
            x = Fraction(x)
            if x in As or x in seen: continue
            seen.add(x); stats['cand'] += 1
            C = sorted(A + [x])
            if not is_45_set(C): continue
            stats['is45'] += 1
            Hc = HG(C)
            if Hc.m != 13: continue
            stats['m13'] += 1
            stats['h_by'][Hc.alpha] = stats['h_by'].get(Hc.alpha, 0) + 1
            if Hc.alpha <= 8: stats['h8'] += 1; pr('H(A+x) has h<=8 !', C)
    # (c) edge {a,x,y} with x middle: y = 2x - a, x generic
    for ai in range(14):
        a = A[ai]
        for x in (Fraction(a) + Fraction(rng.randrange(10**7, 10**9), 7) , Fraction(a) - Fraction(rng.randrange(10**7, 10**9), 11)):
            y = 2*x - a
            C = sorted([Fraction(v) for v in A] + [x, y])
            if len(set(C)) != 16: continue
            if not is_45_set(C): univ_edge_case.setdefault('not45', 0); univ_edge_case['not45'] += 1; continue
            Hc = HG(C)
            exp = 8 + (1 if ai in U else 2)
            univ_edge_case['total'] += 1
            if Hc.alpha != exp or Hc.m != 13: univ_edge_case['bad'].append((A, ai, x, Hc.alpha, Hc.m))
pr('extension stats', stats)
pr('edge {a,x,y}(x middle) case', {k: (v if k != 'bad' else len(v)) for k, v in univ_edge_case.items()})
json.dump(dict(stats=stats, univ_edge_case={k: (v if k != 'bad' else str(v)) for k, v in univ_edge_case.items()}), open('results_delta.json', 'w'), default=str)
