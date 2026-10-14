"""Referee L003: independent exact realizability decision for ordered midpoint patterns (any m), no e757/judge imports.
Pattern P (edges (i,j,k), j the midpoint) on ranks 0..n-1 is realizable iff some strictly increasing x satisfies the AP
equations of P, has exactly the 3-APs of P, and is a (4,5)-set.  With V = solution space of the AP equations and
C = {x in V strictly increasing} (relatively open in V), every failure condition is a finite union of proper linear
subspaces unless it holds identically on V, so:
  realizable  <=>  C nonempty  and  no extra-AP form vanishes on V  and  every 4-subset has >= 5 distinct distance
                   forms modulo V-annihilator.
Certificates: C nonempty -> exact rational strictly increasing point (from a float LP, rationalised and checked exactly);
C empty -> exact Gordan vector y >= 0, y != 0 with sum_i y_i (x_{i+1}-x_i) == 0 on V; forced coincidences are exact.
Every 'realizable' verdict is additionally confirmed by an explicit exact witness set (generic perturbation inside C)
checked from the definitions: (4,5) on all 4-subsets, 3-AP set == P, h = largest Sidon subset (brute force).
usage: python3 realdec.py n T  < patenum output   -> prints a JSON summary; writes witnesses to realdec_n<n>_m<m>.txt.gz"""
import sys, json, gzip, itertools, random, math
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog

def canon(n, E):
    t = tuple(sorted(E)); r = tuple(sorted((n - 1 - k, n - 1 - j, n - 1 - i) for i, j, k in E))
    return min(t, r)

def has_f7(E):
    S = set(frozenset(e) for e in E)
    inc = {}
    for e in E:
        for v in e: inc.setdefault(v, []).append(frozenset(e) - {v})
    for c, arms in inc.items():
        for a1, a2, a3 in itertools.combinations(arms, 3):
            if a1 & a2 or a1 & a3 or a2 & a3: continue
            for u1 in a1:
                for u2 in a2:
                    for u3 in a3:
                        t1 = frozenset((u1, u2, u3)); t2 = (a1 | a2 | a3) - t1
                        if t1 in S and t2 in S: return True
    return False

def basis_V(n, E):
    rows = []
    for (i, j, k) in E:
        r = [Fr(0)] * n; r[i] += 1; r[k] += 1; r[j] -= 2; rows.append(r)
    M = rows; piv = []; rr = 0
    for c in range(n):
        p = next((q for q in range(rr, len(M)) if M[q][c] != 0), None)
        if p is None: continue
        M[rr], M[p] = M[p], M[rr]; inv = 1 / M[rr][c]; M[rr] = [x * inv for x in M[rr]]
        for q in range(len(M)):
            if q != rr and M[q][c] != 0:
                f = M[q][c]; M[q] = [a - f * b for a, b in zip(M[q], M[rr])]
        piv.append(c); rr += 1
        if rr == len(M): break
    B = []
    for fc in [c for c in range(n) if c not in piv]:
        v = [Fr(0)] * n; v[fc] = Fr(1)
        for q, pc in enumerate(piv): v[pc] = -M[q][fc]
        B.append(v)
    return B

def exact_kernel_vector_on_support(G, S, d):
    """exact y on support S with G_S^T y = 0, sum y = 1 (RREF, free vars = 0); returns list or None"""
    rows = [[G[i][t] for i in S] + [Fr(0)] for t in range(d)] + [[Fr(1)] * len(S) + [Fr(1)]]
    M = rows; piv = []; rr = 0; ncol = len(S)
    for c in range(ncol):
        p = next((q for q in range(rr, len(M)) if M[q][c] != 0), None)
        if p is None: continue
        M[rr], M[p] = M[p], M[rr]; inv = 1 / M[rr][c]; M[rr] = [x * inv for x in M[rr]]
        for q in range(len(M)):
            if q != rr and M[q][c] != 0:
                f = M[q][c]; M[q] = [a - f * b for a, b in zip(M[q], M[rr])]
        piv.append(c); rr += 1
    for q in range(rr, len(M)):
        if M[q][ncol] != 0: return None
    y = [Fr(0)] * ncol
    for q, pc in enumerate(piv): y[pc] = M[q][ncol]
    return y

def order_decide(n, B):
    d = len(B)
    G = [[B[t][i + 1] - B[t][i] for t in range(d)] for i in range(n - 1)]
    Gf = np.array([[float(g) for g in row] for row in G])
    A_ub = np.hstack([-Gf, np.ones((n - 1, 1))])
    res = linprog(np.r_[np.zeros(d), -1.0], A_ub=A_ub, b_ub=np.zeros(n - 1), bounds=[(-1, 1)] * d + [(None, 1)], method='highs')
    if res.status == 0 and -res.fun > 1e-9:
        for den in (10 ** 2, 10 ** 4, 10 ** 6, 10 ** 9, 10 ** 12):
            cq = [Fr(float(v)).limit_denominator(den) for v in res.x[:d]]
            if all(sum(G[i][t] * cq[t] for t in range(d)) > 0 for i in range(n - 1)):
                return True, cq, G
        return None, 'feasible-but-no-rational-point', G
    res2 = linprog(np.zeros(n - 1), A_eq=np.vstack([Gf.T, np.ones((1, n - 1))]), b_eq=np.r_[np.zeros(d), 1.0], bounds=[(0, None)] * (n - 1), method='highs')
    if res2.status != 0: return None, 'both-LPs-failed', G
    y = res2.x
    S = [i for i in range(n - 1) if y[i] > 1e-9]
    for den in (10 ** 2, 10 ** 4, 10 ** 6, 10 ** 9):
        yq = [Fr(float(y[i])).limit_denominator(den) if i in S else Fr(0) for i in range(n - 1)]
        if sum(yq) > 0 and all(v >= 0 for v in yq) and all(sum(G[i][t] * yq[i] for i in range(n - 1)) == 0 for t in range(d)):
            return False, yq, G
    ys = exact_kernel_vector_on_support(G, S, d)
    if ys is not None and all(v >= 0 for v in ys) and sum(ys) > 0:
        return False, ys, G
    return None, 'no-gordan-certificate', G

def forced(n, E, B):
    d = len(B); P = set(E)
    for i in range(n):
        for k in range(i + 2, n):
            for j in range(i + 1, k):
                if (i, j, k) in P: continue
                if all(B[t][i] + B[t][k] - 2 * B[t][j] == 0 for t in range(d)): return 'forced extra AP'
    for Q in itertools.combinations(range(n), 4):
        forms = {tuple(B[t][v] - B[t][u] for t in range(d)) for u, v in itertools.combinations(Q, 2)}
        if len(forms) < 5: return 'forced repeated difference'
    return None

def is45(A):
    return all(len({b - a for a, b in itertools.combinations(q, 2)}) >= 5 for q in itertools.combinations(A, 4))
def aps(A):
    S = {v: i for i, v in enumerate(A)}; out = []
    for i in range(len(A)):
        for k in range(i + 2, len(A)):
            mid = (A[i] + A[k]) / 2
            if mid in S: out.append((i, S[mid], k))
    return sorted(out)
def sidon_max(A):
    best = 0; n = len(A)
    def rec(idx, chosen, diffs):
        nonlocal best
        if len(chosen) > best: best = len(chosen)
        for t in range(idx, n):
            if len(chosen) + (n - t) <= best: return
            nd = [A[t] - a for a in chosen]
            if any(x in diffs for x in nd): continue
            rec(t + 1, chosen + [A[t]], diffs | set(nd))
    rec(0, [], frozenset())
    return best

def witness(n, E, B, c, T, rng):
    d = len(B)
    x0 = [sum(c[t] * B[t][i] for t in range(d)) for i in range(n)]
    for attempt in range(60):
        eps = Fr(1, 10 ** (3 + attempt // 10))
        r = [Fr(rng.randint(-1000, 1000), 1000) for _ in range(d)]
        x = [x0[i] + eps * sum(r[t] * B[t][i] for t in range(d)) for i in range(n)]
        if any(x[i] >= x[i + 1] for i in range(n - 1)): continue
        den = 1
        for v in x: den = den * v.denominator // math.gcd(den, v.denominator)
        A = [int(v * den) for v in x]; lo = A[0]; A = [a - lo for a in A]
        g = 0
        for a in A: g = math.gcd(g, a)
        A = [a // g for a in A]
        if is45(A) and aps(A) == sorted(E):
            return A
    return None

if __name__ == '__main__':
    n, T = int(sys.argv[1]), int(sys.argv[2])
    hcheck = len(sys.argv) > 3 and sys.argv[3] == 'h'
    rng = random.Random(12345)
    labelled = {}; seen = {}
    for line in sys.stdin:
        if not line.startswith('PAT'): continue
        parts = line.split(); E = [tuple(int(v) for v in p.split(',')) for p in parts[2:]]
        m = len(E)
        labelled[m] = labelled.get(m, 0) + 1
        seen.setdefault(m, set()).add(canon(n, E))
    summary = {}
    for m in sorted(seen):
        cs = sorted(seen[m]); res = {'labelled': labelled[m], 'up_to_reflection': len(cs), 'f7': 0, 'f7_free': 0,
                                     'realizable': 0, 'reasons': {}, 'undecided': 0, 'f7_realizable': 0, 'h_hist': {},
                                     'witness_missing': 0}
        wout = gzip.open('realdec_n%d_m%d.txt.gz' % (n, m), 'wt')
        for E in cs:
            f7 = has_f7(E)
            res['f7' if f7 else 'f7_free'] += 1
            B = basis_V(n, list(E))
            ok, cert, G = order_decide(n, B)
            if ok is None: res['undecided'] += 1; wout.write('UNDECIDED %s %s\n' % (cert, E)); continue
            if not ok:
                reason = 'order-infeasible'
            else:
                reason = forced(n, list(E), B)
            if reason:
                key = reason + (' [F7]' if f7 else '')
                res['reasons'][key] = res['reasons'].get(key, 0) + 1
                continue
            A = witness(n, list(E), B, cert, T, rng)
            if A is None: res['witness_missing'] += 1; wout.write('NOWITNESS %s\n' % (E,)); continue
            res['realizable'] += 1
            if f7: res['f7_realizable'] += 1
            if hcheck:
                h = sidon_max(A); res['h_hist'][h] = res['h_hist'].get(h, 0) + 1
            wout.write('REAL %s | %s\n' % (' '.join(map(str, A)), ' '.join('%d,%d,%d' % e for e in E)))
        wout.close()
        summary['n%d_m%d' % (n, m)] = res
        print(json.dumps({'n': n, 'm': m, **res}), flush=True)
