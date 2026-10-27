# Referee checks of L022 Theorem 1 (b), (b'), (c), (d) and the clause of (e) on <=4-edge configurations.
import json, glob, random, sys, time
from fractions import Fraction
from itertools import combinations, product
from math import lcm
from rlib import rank, nullspace, is_45_fast, is_45_bruteforce, ap_triples

P = (1 << 61) - 1


def rank_modp(rows, ncols):
    M = [[x % P for x in r] for r in rows]
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(M)):
            if M[i][c]:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], P - 2, P)
        M[r] = [x * inv % P for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        r += 1
    return r


def form(n, a, b, c):
    v = [0] * n
    v[a] += 1
    v[c] += 1
    v[b] -= 2
    return v


def aps_of(vals):
    """vals: list sorted ascending; return list of rank triples (i,j,k) with x_j midpoint."""
    n = len(vals)
    pos = {v: i for i, v in enumerate(vals)}
    out = []
    for i in range(n):
        for k in range(i + 2, n):
            s = vals[i] + vals[k]
            mid = Fraction(s) / 2
            if mid in pos:
                out.append((i, pos[mid], k))
    return out


def part_b_exhaustive(nmax):
    """All ordered injective-midpoint patterns on n points (each b gets 0 or 1 AP (a,b,c), a<b<c).
    Full row rank mod p certifies rank over Q = m."""
    tot = 0
    bad = 0
    for n in range(3, nmax + 1):
        choices = []
        for b in range(1, n - 1):
            ch = [None] + [(a, b, c) for a in range(b) for c in range(b + 1, n)]
            choices.append(ch)
        cnt = 0
        for pat in product(*choices):
            E = [t for t in pat if t is not None]
            if not E:
                continue
            cnt += 1
            rows = [form(n, *t) for t in E]
            if rank_modp(rows, n) != len(E):
                if rank(rows, n) != len(E):
                    bad += 1
                    print('DEPENDENT', n, E)
        print('  n=%d patterns=%d' % (n, cnt), flush=True)
        tot += cnt
    return tot, bad


def part_b_random(trials, rng):
    bad = 0
    for _ in range(trials):
        n = rng.randint(5, 45)
        E = []
        for b in range(1, n - 1):
            if rng.random() < 0.8:
                E.append((rng.randrange(b), b, rng.randrange(b + 1, n)))
        rows = [form(n, *t) for t in E]
        if rank_modp(rows, n) != len(E) and rank(rows, n) != len(E):
            bad += 1
    return bad


def load_sets():
    S = {}
    d = json.load(open('/home/user/Erdos-757/data/small_records.json'))
    for k, v in d['sets'].items():
        S['small_' + k] = sorted(Fraction(x) for x in v['set'])
    for f in sorted(glob.glob('/home/user/Erdos-757/results/claims/C*.json')):
        c = json.load(open(f))
        S[f.split('/')[-1][:4]] = sorted(Fraction(x) for x in c['set'])
    return S


def realize_deletion(vals, E, D, rng):
    """Theorem 1(c): find rational y in V' near x, same order, AP set exactly E\\D."""
    n = len(vals)
    Ep = [e for e in E if e not in D]
    rows = [form(n, *t) for t in Ep]
    B = nullspace(rows, n) if rows else [[Fraction(int(i == j)) for i in range(n)] for j in range(n)]
    gaps = min(vals[i + 1] - vals[i] for i in range(n - 1))
    for attempt in range(40):
        coef = [Fraction(rng.randint(-1000, 1000)) for _ in B]
        w = [sum(coef[t] * B[t][i] for t in range(len(B))) for i in range(n)]
        W = max(abs(x) for x in w) or Fraction(1)
        for K in (4, 64, 1024, 2 ** 20):
            eps = gaps / (W * K)
            y = [vals[i] + eps * w[i] for i in range(n)]
            if any(y[i] >= y[i + 1] for i in range(n - 1)):
                continue
            L = 1
            for v in y:
                L = lcm(L, v.denominator)
            yi = [int(v * L) for v in y]
            if not is_45_fast(yi):
                continue
            got = aps_of(sorted(yi))
            if sorted(got) == sorted(Ep):
                return True, yi
    return False, None


def main():
    rng = random.Random(20261027)
    t0 = time.time()
    print('Part (b) exhaustive ordered injective-midpoint patterns, n<=7:')
    tot, bad = part_b_exhaustive(7)
    print('  total patterns', tot, 'dependent', bad)
    print('Part (b) random patterns (n in 5..45), 4000 trials: dependent', part_b_random(4000, rng))
    S = load_sets()
    print('Part (b), (b\'), (c) on stored sets:')
    summary = {'sets': 0, 'rank_eq_m': 0, 'saturated': 0, 'saturated_rigid': 0, 'deletions': 0, 'deletions_ok': 0}
    for name, vals in S.items():
        n = len(vals)
        E = aps_of(vals)
        m = len(E)
        assert is_45_fast(vals), name
        if n <= 30:
            assert is_45_bruteforce(vals), name
        rows = [form(n, *t) for t in E]
        rk = rank(rows, n)
        summary['sets'] += 1
        summary['rank_eq_m'] += (rk == m)
        line = '  %-6s n=%d m=%d rank=%d' % (name, n, m, rk)
        if m == n - 2:
            summary['saturated'] += 1
            B = nullspace(rows, n)
            ok = (len(B) == 2)
            summary['saturated_rigid'] += ok
            line += ' saturated: dim V = %d' % len(B)
        # deletions: every single AP (if m <= 30) and 6 random subsets
        Ds = [[e] for e in E] if m <= 30 else [[e] for e in rng.sample(E, 10)]
        for _ in range(6):
            k = rng.randint(1, max(1, m))
            Ds.append(rng.sample(E, k))
        okc = 0
        for D in Ds:
            ok, yi = realize_deletion(vals, E, D, rng)
            summary['deletions'] += 1
            summary['deletions_ok'] += ok
            okc += ok
            if not ok:
                print('    DELETION FAILED', name, D)
        line += ' deletions ok %d/%d' % (okc, len(Ds))
        print(line, flush=True)
    print(summary)
    print('time %.1fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
