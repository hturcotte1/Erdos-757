"""Referee: Theorem 1 / Corollary 3 / Theorem 2 on 16-point subsets of a generic gluing C = A_base U (q*B + t), B a 12-point
record set, exact Fractions; q chosen to avoid every ratio (a-a')/(b-b') (checked), t large.  For a random sample of 16-subsets
(and all 16-subsets made of 14 + 2, 13 + 3, 12 + 4, 4 + 12 points ... sampled): H(S) in O+, I11, tau <= 6, h = 16 - tau (brute force)."""
import itertools, json, random
from fractions import Fraction as Fr
import importlib.util, sys
spec = importlib.util.spec_from_file_location('rt', '/home/user/Erdos-757/experiments/referee/L008-round1/scripts/realizable_tests_lib.py')
rt = importlib.util.module_from_spec(spec); spec.loader.exec_module(rt)
ABASE = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
B = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']['12']['set']
ratios = set(Fr(a - a2, b - b2) for a, a2 in itertools.permutations(ABASE, 2) for b, b2 in itertools.permutations(B, 2))
q = Fr(1, 7919)
while q in ratios: q += Fr(1, 10**6)
t = Fr(10**7)
C = sorted([Fr(x) for x in ABASE] + [q * b + t for b in B])
def is45(A):
    for qd in itertools.combinations(A, 4):
        if len({abs(a - b) for a, b in itertools.combinations(qd, 2)}) < 5: return False
    return True
print('glued set: n =', len(C), '| (4,5):', is45(C), '| q =', q)
def aps(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [(idx[a], idx[(a + c) / 2], idx[c]) for a, c in itertools.combinations(A, 2) if (a + c) / 2 in idx]
E = aps(C); print('3-APs in glued set:', len(E), '(A_base 12 + B 10 = 22 expected)')
rng = random.Random(1); bad = 0; tested = 0; hs = {}
for _ in range(400):
    k1 = rng.randint(4, 14); S = sorted(rng.sample(range(14), k1) + [14 + i for i in rng.sample(range(12), 16 - k1)]) if 16 - k1 <= 12 else None
    if S is None: continue
    Ss = set(S); ed = [e for e in E if set(e) <= Ss]
    t_ = rt.tau(ed, S); m = len(ed)
    ok = rt.linear(ed) and not rt.has_f7(ed) and rt.p3(ed, S) and 11 * t_ <= 48 + 2 * m and t_ <= 6
    pts = [C[i] for i in S]
    if tested < 60:
        hb = rt.h_brute(pts); ok = ok and hb == 16 - t_; hs[hb] = hs.get(hb, 0) + 1
    tested += 1; bad += not ok
print('random 16-subsets of the gluing tested:', tested, '| failures:', bad, '| h histogram (first 60):', hs)
