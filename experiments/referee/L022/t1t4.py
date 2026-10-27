"""Referee (L022, referee #2): Theorem 1(b) (AP rank = m), Theorem 1(b') (rigidity when m = n-2), Theorem 1(c)
(edge deletion realized exactly) and Theorem 4 (O1-O7) on all stored realizable sets, with my own code; random
ordered midpoint patterns for Theorem 1(b); Corollary 3' cell arithmetic.  No import of e757 / judge / L0xx code."""
import json, glob, itertools, random, sys
from fractions import Fraction as Fr
from math import lcm
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L022')
from rz import is45, generic_point, forced, explicit_integer_point

def aps_sorted(A):
    """A sorted; APs as rank triples (i,j,k), i<j<k, x_j midpoint."""
    idx = {x: i for i, x in enumerate(A)}; out = []
    for i in range(len(A)):
        for k in range(i + 2, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 and s // 2 in idx:
                out.append((i, idx[s // 2], k))
    return out

def rank_rows(E, n):
    R, rk = generic_point([(i, j, k) for (i, j, k) in E], n)
    return rk, R

def weak_sidon(A):
    sums = set()
    for x, y in itertools.combinations(A, 2):
        if x + y in sums: return False
        sums.add(x + y)
    return True

def order_facts(A):
    """returns dict of booleans for O1..O7 on sorted A."""
    n = len(A); E = aps_sorted(A); m = len(E)
    L = [0] * n; M = [0] * n; Rr = [0] * n
    for (i, j, k) in E: L[i] += 1; M[j] += 1; Rr[k] += 1
    res = {}
    res['O1'] = M[0] == 0 and M[n - 1] == 0 and Rr[0] == 0 and L[n - 1] == 0
    res['O2'] = Rr[1] == 0 and L[n - 2] == 0 and (M[1] == 1) == ((2 * A[1] - A[0]) in set(A)) and (M[n - 2] == 1) == ((2 * A[n - 2] - A[n - 1]) in set(A))
    steps = [A[j] - A[i] for (i, j, k) in E]
    res['O3'] = len(set(steps)) == m
    # O3 reformulation: every positive difference occurs at most twice; exactly the steps occur twice
    cnt = {}
    for x, y in itertools.combinations(A, 2): cnt[y - x] = cnt.get(y - x, 0) + 1
    res['O3b'] = max(cnt.values()) <= 2 and {d for d, c in cnt.items() if c == 2} == set(steps)
    # O4 (K30 with common endpoint) and full K30
    ok = True
    for (i, j, k), (a, b, c) in itertools.permutations(E, 2):
        if i <= a and k <= c and (i, k) != (a, c) and not j < b: ok = False
    res['O4'] = ok
    # O5
    ok = True
    for (i, j, k) in E:
        if k == n - 1 and not (2 * A[j] >= A[0] + A[n - 1] and ((2 * A[j] == A[0] + A[n - 1]) == (i == 0))): ok = False
        if i == 0 and not (2 * A[j] <= A[0] + A[n - 1] and ((2 * A[j] == A[0] + A[n - 1]) == (k == n - 1))): ok = False
    res['O5'] = ok and sum(1 for (i, j, k) in E if i == 0 and k == n - 1) <= 1
    # O6: midpoint of at most one AP; reflection relations at degree-3 vertices; dimension drop 2
    ok = max(M) <= 1
    deg = [L[v] + M[v] + Rr[v] for v in range(n)]
    rk, _ = rank_rows(E, n)
    for v in range(n):
        if deg[v] != 3: continue
        vals = set()
        for (i, j, k) in E:
            if v == j: vals.add(Fr(A[i] + A[k], 2))
            elif v == i: vals.add(Fr(2 * A[j] - A[k]))
            elif v == k: vals.add(Fr(2 * A[j] - A[i]))
        if vals != {Fr(A[v])}: ok = False
        B = [x for x in A if x != A[v]]; EB = aps_sorted(B)
        rkB, _ = rank_rows(EB, n - 1)
        if not (len(EB) == m - 3 and (n - 1 - rkB) == (n - rk) + 2): ok = False
    res['O6'] = ok
    # O7 (K31): no three APs pairwise meeting in distinct vertices with all three private vertices midpoints
    ok = True
    for e1, e2, e3 in itertools.combinations(E, 3):
        s12 = set(e1) & set(e2); s13 = set(e1) & set(e3); s23 = set(e2) & set(e3)
        if len(s12) == 1 and len(s13) == 1 and len(s23) == 1 and len(s12 | s13 | s23) == 3:
            shared = s12 | s13 | s23
            priv = [[x for x in e if x not in shared][0] for e in (e1, e2, e3)]
            if all(p == e[1] for p, e in zip(priv, (e1, e2, e3))): ok = False
    res['O7'] = ok
    res['rank'] = rk; res['m'] = m; res['n'] = n
    return res, E

def realize_deletion(A, E, D, rnd):
    """Theorem 1(c): realize E \\ D exactly, same order, by perturbing A inside the solution space of E \\ D."""
    n = len(A); Ep = [e for e in E if e not in D]
    R, rk = generic_point(Ep, n)
    k = len(R[0])
    # A itself has parameter vector = coordinates of A at the free columns; perturb those parameters
    # Simpler: pick y = A + eps * w, w a random rational combination of a nullspace basis.
    basis = []
    for i in range(k):
        basis.append([R[v][i] for v in range(n)])
    for _ in range(50):
        coef = [rnd.randint(-100, 100) for _ in range(k)]
        w = [sum(c * b[v] for c, b in zip(coef, basis)) for v in range(n)]
        mx = max(abs(x) for x in w) or 1
        eps = Fr(A[-1] - A[0], 10 ** 5) / mx
        y = [A[v] + eps * w[v] for v in range(n)]
        den = 1
        for t in y: den = lcm(den, t.denominator)
        yi = [int(t * den) for t in y]
        if sorted(yi) != yi or len(set(yi)) < n: continue
        if is45(yi) and set(aps_sorted(yi)) == set(Ep): return yi
    return None

def main():
    rnd = random.Random(7)
    sets = []
    d = json.load(open('/home/user/Erdos-757/data/small_records.json'))
    for k, v in d['sets'].items(): sets.append(('small_records:' + k, sorted(v['set'])))
    for f in sorted(glob.glob('/home/user/Erdos-757/results/claims/C00*.json')):
        sets.append(('claim:' + f.split('/')[-1][:4], sorted(json.load(open(f))['set'])))
    print('== Theorem 1(b), Theorem 4 on record sets and judged claims (own code)')
    allok = True
    for name, A in sets:
        assert is45(A), name
        res, E = order_facts(A)
        bad = [k for k in ('O1', 'O2', 'O3', 'O3b', 'O4', 'O5', 'O6', 'O7') if not res[k]]
        rk_ok = res['rank'] == res['m']
        allok &= (not bad) and rk_ok
        print('  %-22s n=%2d m=%2d rank=%2d %s %s' % (name, res['n'], res['m'], res['rank'], 'rank=m' if rk_ok else 'RANK<m!', 'O1-O7 ok' if not bad else 'FAILED ' + str(bad)))
    # realized pieces from the prover's jsonl (explicit sets; already verified in rz.py as (4,5)-sets)
    cnt = dict(sets=0, fails=0, rank_full=0)
    for f in glob.glob('/home/user/Erdos-757/experiments/prover/L022/out/realize_*.jsonl'):
        for l in open(f):
            r = json.loads(l)
            if r.get('explicit'):
                A = sorted(r['explicit'])
                if not is45(A): cnt['fails'] += 1; continue
                res, E = order_facts(A); cnt['sets'] += 1
                bad = [k for k in ('O1', 'O2', 'O3', 'O3b', 'O4', 'O5', 'O6', 'O7') if not res[k]]
                if bad: cnt['fails'] += 1; print('  FAIL', f, r['cls'], bad)
                if res['rank'] == res['m']: cnt['rank_full'] += 1
    print('  realized pieces:', cnt)
    print('all record/claim sets pass:', allok)

    print('== Theorem 1(b\'): rigidity of saturated sets (m = n-2): solution space = span(x, 1)')
    for name, A in sets:
        E = aps_sorted(A); n = len(A)
        if len(E) == n - 2:
            R, rk = generic_point(E, n)
            print('  %-22s m=n-2, rank=%d, dim solution space=%d' % (name, rk, n - rk))

    print('== Theorem 1(c): delete each single AP and random AP sets of A_base and the 12-point sets; realize exactly')
    tot = dict(cases=0, ok=0)
    for name, A in sets:
        if len(A) > 16: continue
        E = aps_sorted(A)
        cases = [[e] for e in E] + [rnd.sample(E, rnd.randint(2, len(E))) for _ in range(8)] + [list(E)]
        good = 0
        for D in cases:
            tot['cases'] += 1
            if realize_deletion(A, E, D, rnd) is not None: tot['ok'] += 1; good += 1
        print('  %-22s deletions realized %d/%d' % (name, good, len(cases)))
    print('  ', tot)

    print('== Theorem 1(b) on random ordered midpoint patterns (injective midpoints, a<b<c; NOT linear in general)')
    bad = 0; T = 4000
    for t in range(T):
        n = rnd.randint(4, 40)
        mids = rnd.sample(range(1, n - 1), rnd.randint(1, n - 2))
        E = []
        for b in mids:
            E.append((rnd.randrange(0, b), b, rnd.randrange(b + 1, n)))
        R, rk = generic_point(E, n)
        if rk != len(E): bad += 1
    print('  patterns', T, 'dependent', bad)
    # control: non-injective midpoints can be dependent? (two APs with the same midpoint are independent as forms unless equal)
    # a genuinely dependent example without injectivity: parallelogram-type? Just report that injectivity was used.

    print('== Corollary 3\' arithmetic: violator cells at n=29,30 and the connected-component bound')
    def cells(N):
        out = []
        for s in (-1, -2):
            for m in range((N - 1 + 1) // 2, N - 1):
                num = 3 * N + 2 * m - s
                if num % 11: continue
                t = num // 11
                if 17 * t <= 5 * N + 3 * m and t <= m and 3 * m >= N:
                    out.append((N, m, t, s))
        return out
    for N in (28, 29, 30):
        print('  n=%d cells (n,m,tau,s):' % N, cells(N))
    for (N, m, t, s) in cells(30):
        n1, m1, t1 = N - 1, m - 3, t - 1
        print('  (30,%d,%d) -> H-v in cell (29,%d,%d); connected needs 29 <= 2*%d+1=%d: %s' % (m, t, m1, t1, m1, 2 * m1 + 1, 'possible' if n1 <= 2 * m1 + 1 else 'IMPOSSIBLE'))
    # component size bounds used in 3.4: n >= n(F) + 1 + 3 when the other component has >= 3 vertices
    print('  pattern (b)/(f) with a component of >= 27 vertices and another of >= 3: n >= 27+3+1 =', 27 + 3 + 1)

main()
