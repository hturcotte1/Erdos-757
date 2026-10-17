"""Referee control for rreal at n=12 against the accepted census L002 (54,243 affine classes of 12-point (4,5)-sets with h=7).
(A) every census set's own AP pattern (labels = rank order) must be realized by rreal, with the census set itself among the
    printed realizations (comparison of the normalised values modulo p);
(B) rreal on the 221 classes of the prover's cell(12,10,5,4): every printed realization is reconstructed EXACTLY (rational
    reconstruction, heights <= H = 6^5, 2H^2 < p) and re-verified with Fractions (distinct, AP set == edges); those that are
    (4,5)-sets are normalised (min 0, max 1, up to reflection) and compared with the census as sets of affine classes."""
import sys, gzip, json, itertools, subprocess
from fractions import Fraction
P = 2147483647
def pattern(S):
    S = sorted(S); idx = {a: i for i, a in enumerate(S)}
    return sorted(tuple(sorted((idx[a], idx[(a + c) // 2], idx[c]))) for a, c in itertools.combinations(S, 2) if (a + c) % 2 == 0 and (a + c) // 2 in idx)
def is45(vals):
    for B in itertools.combinations(vals, 4):
        if len({abs(x - y) for x, y in itertools.combinations(B, 2)}) < 5: return False
    return True
def norm_class(vals):
    lo, hi = min(vals), max(vals); a = tuple(sorted((v - lo) / (hi - lo) for v in vals)); b = tuple(sorted(1 - t for t in a))
    return min(a, b)
def ratrec(a, p=P):
    # rational reconstruction: find r/s == a mod p with |r|, s <= sqrt(p/2)
    import math
    B = int(math.isqrt(p // 2))
    r0, r1, s0, s1 = p, a % p, 0, 1
    while r1 > B:
        q = r0 // r1; r0, r1 = r1, r0 - q * r1; s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > B: raise ValueError('no reconstruction')
    f = Fraction(r1, s1)
    assert (f.numerator - a * f.denominator) % p == 0
    return f
census = json.load(gzip.open(sys.argv[1]))
print('census entries', len(census), 'is_45 all', all(c['is_45'] for c in census), 'h=7 all', all(c['h'] == 7 for c in census))
cen_classes = {norm_class([Fraction(x) for x in c['set']]) for c in census}
print('census affine classes (up to reflection)', len(cen_classes))
# (A)
lines = []; targets = []
for c in census:
    S = sorted(c['set']); E = pattern(S); assert len(E) == 10
    t = [((a - S[0]) * pow(S[-1] - S[0], P - 2, P)) % P for a in S]
    lines.append('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in E) + ' | ' + ','.join(map(str, t)))
out = subprocess.run(['./out/bin/rreal', '12'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
gi = 0; okA = 0; nreal = 0
for l in out:
    if l.startswith('STAT'):
        kv = dict(x.split('=') for x in l.split()[1:]); nreal += int(kv['realizations'])
        if int(kv['target_found']) >= 1: okA += 1
        gi += 1
print('(A) census sets checked %d, own set found among rreal realizations: %d (total realizations printed %d)' % (gi, okA, nreal))
# (B)
cls = [l.strip() for l in open(sys.argv[2]) if l.startswith('FOUND')]
out = subprocess.run(['./out/bin/rreal', '12', 'print'], input='\n'.join(cls) + '\n', capture_output=True, text=True).stdout.splitlines()
import re
gi = 0; real_cls = set(); nreal = 0; n45 = 0; graphs_with_real = 0; graphs_with_45 = 0; cur = []; statlines = 0
def edges_of(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
for l in out:
    if l.startswith('REAL'): cur.append(l)
    elif l.startswith('STAT'):
        E = edges_of(cls[gi]); any45 = False
        for r in cur:
            xs = [ratrec(int(v)) for v in r.split('x=')[1].split(',')]
            assert len(set(xs)) == 12
            vals = sorted(xs); Sx = set(vals)
            apset = sorted(tuple(sorted((xs.index(a), xs.index((a + c) / 2), xs.index(c)))) for a, c in itertools.combinations(vals, 2) if (a + c) / 2 in Sx)
            assert apset == sorted(tuple(sorted(e)) for e in E), 'AP set != edges'
            nreal += 1
            if is45(xs): n45 += 1; any45 = True; real_cls.add(norm_class(xs))
        graphs_with_real += bool(cur); graphs_with_45 += any45; gi += 1; cur = []
print('(B) classes %d, with a realization %d, with a (4,5)-realization %d; realizations %d (all exactly re-verified), (4,5) %d' % (gi, graphs_with_real, graphs_with_45, nreal, n45))
print('(B) distinct (4,5) affine classes realized: %d; equal to census set: %s; census minus realized: %d; realized minus census: %d' % (len(real_cls), real_cls == cen_classes, len(cen_classes - real_cls), len(real_cls - cen_classes)))
