"""Referee numerical tests on genuine (4,5)-sets (exact integers, own code, no e757/judge imports):
 (1) witness C16: distinct, (4,5) from the definition, number of 3-APs, h by brute force over all 2^16 subsets (Sidon = all sums
     x+y, x<=y, distinct) and by CP-SAT (different method); h/n vs 4/7 with Fractions;
 (2) for every induced subset S of A_base (2^14), both 12-point omega sets and the third 12-point set, C16 (2^16) and the
     Fibonacci set {F3..F18} (2^16): H(S) is linear, F7-free and satisfies (P3) [membership in O+], I11 11 tau <= 3|S|+2m
     (Corollary 3 range |S|<=16), tau(H(S)) <= 6 when |S| = 16 (Theorem 1), and h(S) = |S| - tau(H(S)) on a random sample;
 (3) 16-point (4,5)-sets obtained by two-point extensions of census 14-point classes (points in new 3-APs), the same checks,
     and h >= 10 (Theorem 2)."""
import itertools, json, gzip, random, sys
from fractions import Fraction
def is45(A):
    for q in itertools.combinations(A, 4):
        if len({abs(a - b) for a, b in itertools.combinations(q, 2)}) < 5: return False
    return True
def aps(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [(idx[a], idx[(a + c) // 2], idx[c]) for a, c in itertools.combinations(A, 2) if (a + c) % 2 == 0 and (a + c) // 2 in idx]
def is_sidon(S):
    s = set()
    for i in range(len(S)):
        for j in range(i, len(S)):
            t = S[i] + S[j]
            if t in s: return False
            s.add(t)
    return True
def h_brute(A):
    A = sorted(A); n = len(A); best = 0
    # iterate subsets by decreasing size would be faster; simple: check all subsets of size k from high to low
    for k in range(n, 0, -1):
        for S in itertools.combinations(A, k):
            if is_sidon(S): return k
    return 0
def h_cpsat(A):
    from ortools.sat.python import cp_model
    A = sorted(A); n = len(A); M = cp_model.CpModel(); x = [M.NewBoolVar('x%d' % i) for i in range(n)]
    # forbid every pair of distinct multisets {a,b} != {c,d} with a+b = c+d
    sums = {}
    for i in range(n):
        for j in range(i, n): sums.setdefault(A[i] + A[j], []).append((i, j))
    for s, prs in sums.items():
        for (i, j), (k, l) in itertools.combinations(prs, 2):
            inv = sorted({i, j, k, l}); M.Add(sum(x[t] for t in inv) <= len(inv) - 1)
    M.Maximize(sum(x)); S = cp_model.CpSolver(); S.parameters.num_workers = 1; st = S.Solve(M)
    assert st == cp_model.OPTIMAL; return int(S.ObjectiveValue())
def tau(edges, verts):
    edges = [frozenset(e) for e in edges]
    def rec(es, k):
        if not es: return True
        if k == 0: return False
        e = next(iter(es))
        return any(rec([f for f in es if v not in f], k - 1) for v in e)
    for k in range(0, len(verts) + 1):
        if rec(edges, k): return k
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
def has_f7(edges):
    es = set(frozenset(e) for e in edges)
    for five in itertools.combinations(list(es), 5):
        U = sorted(set().union(*five))
        if len(U) != 7: continue
        for p in itertools.permutations(U):
            if all(frozenset((p[a], p[b], p[c])) in es for a, b, c in F7): return True
    return False
def linear(edges): return all(len(set(a) & set(b)) <= 1 for a, b in itertools.combinations(edges, 2))
def p3(edges, verts):
    verts = list(verts)
    for k in range(2, len(verts) + 1):
        pass
    vs = sorted(verts); pos = {v: i for i, v in enumerate(vs)}; ms = [sum(1 << pos[v] for v in e) for e in edges]
    for S in range(1 << len(vs)):
        c = bin(S).count('1')
        if c < 2: continue
        if sum(1 for m in ms if m & S == m) > c - 2: return False
    return True
stats = {'subsets_checked': 0, 'not_in_Oplus': 0, 'I11_viol': 0, 'thm1_viol': 0, 'h_mismatch': 0, 'h_checked': 0}
def check_family(name, A, rng, sample_h=40, f7_full=True):
    A = sorted(A); n = len(A); E = aps(A)
    Hfull = [tuple(e) for e in E]
    lin = linear(Hfull); f7 = has_f7(Hfull); P = p3(Hfull, range(n))
    print('%s: n=%d m=%d linear=%s F7=%s P3=%s' % (name, n, len(E), lin, f7, P))
    cnt = 0
    for mask in range(1, 1 << n):
        S = [i for i in range(n) if mask >> i & 1]; Sset = set(S)
        ed = [e for e in Hfull if set(e) <= Sset]
        t = tau(ed, S); k = len(S); m = len(ed)
        stats['subsets_checked'] += 1
        if 11 * t > 3 * k + 2 * m: stats['I11_viol'] += 1; print('  I11 violation', S)
        if k == 16 and t > 6: stats['thm1_viol'] += 1; print('  Theorem 1 violation', S)
        cnt += 1
    # O+ membership is hereditary; check it on the full set (done above) -> all subsets are in O+ iff full set is
    if not (lin and not f7 and P): stats['not_in_Oplus'] += 1
    # h = |S| - tau on a sample of subsets (brute-force Sidon)
    for _ in range(sample_h):
        k = rng.randint(4, n); S = sorted(rng.sample(range(n), k)); Sset = set(S)
        ed = [e for e in Hfull if set(e) <= Sset]
        hb = h_brute([A[i] for i in S]); t = tau(ed, S)
        stats['h_checked'] += 1
        if hb != k - t: stats['h_mismatch'] += 1; print('  h mismatch', S, hb, k - t)
rng = random.Random(16)
C16 = [-323,0,136,200,243,246,249,272,286,298,323,400,528,596,1056,5000]
print('C16 distinct:', len(set(C16)) == 16, '| (4,5):', is45(C16), '| 3-APs:', len(aps(C16)))
hb = h_brute(C16); hc = h_cpsat(C16)
print('C16 h brute force =', hb, '| h CP-SAT =', hc, '| h/n =', Fraction(hb, 16), '| < 4/7 ?', Fraction(hb, 16) < Fraction(4, 7), '| tau(H) =', tau(aps(C16), range(16)))
ABASE = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
recs = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
FIB = [2, 3]
while len(FIB) < 16: FIB.append(FIB[-1] + FIB[-2])
fams = [('A_base', ABASE), ('12-pt record "12"', recs['12']['set']), ('12-pt "12b"', recs['12b']['set']), ('12-pt "12c"', recs['12c']['set']), ('C16', C16), ('Fibonacci F3..F18', FIB)]
for name, A in fams:
    assert is45(A), name
    check_family(name, A, rng, sample_h=25)
# (3) two-point extensions of census 14-point classes
cls = [json.loads(l) for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt')]
rng2 = random.Random(2026); made = 0; minh = 99; hist = {}
for c in rng2.sample(cls, 12):
    A = [2 * x for x in c['set']]; As = set(A)
    cand = set()
    for a, b in itertools.permutations(A, 2):
        cand.add(2 * a - b)
        if (a + b) % 2 == 0: cand.add((a + b) // 2)
    cand -= As
    good = [x for x in sorted(cand) if is45(A + [x])]
    pairs = [(x, y) for x, y in itertools.combinations(good, 2)]
    rng2.shuffle(pairs); got = 0
    for x, y in pairs:
        B = sorted(A + [x, y])
        if not is45(B): continue
        E = aps(B); t = tau(E, range(16)); hb = h_brute(B)
        ok = linear(E) and not has_f7(E) and p3(E, range(16))
        stats['subsets_checked'] += 1; stats['h_checked'] += 1
        if not ok: stats['not_in_Oplus'] += 1
        if hb != 16 - t: stats['h_mismatch'] += 1
        if 11 * t > 48 + 2 * len(E): stats['I11_viol'] += 1
        if t > 6: stats['thm1_viol'] += 1
        minh = min(minh, hb); hist[(len(E), hb)] = hist.get((len(E), hb), 0) + 1
        got += 1; made += 1
        if got >= 6: break
print('two-point extensions of census classes: 16-point (4,5)-sets tested =', made, '| min h =', minh, '| (m,h) histogram:', sorted(hist.items()))
print('STATS', stats)
