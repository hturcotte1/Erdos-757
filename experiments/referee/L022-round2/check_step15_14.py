"""Round-2 referee check for L022 Steps 1.4 and 1.5 (independent code; no e757/judge imports).

Part A (Step 1.5, delta-coefficient argument). For a (4,5)-set A, a point u in A and new points
p = x_u + delta, q = x_u + 2*delta, enumerate EVERY form of Phi (differences, parallelogram forms,
AP forms) on A u {p,q} that involves p or q, as (constant, delta-coefficient). Check:
  (A1) the forms with delta-coefficient 0 are exactly the AP forms X_a + X_q - 2X_p, a in A;
  (A2) among those, the value is x_a - x_u, vanishing only for a = u;
  (A3) a random integer delta outside the finitely many roots gives a (4,5)-set (brute force over
       all 4-subsets) whose AP set is exactly APs(A) + {(u,p,q)}.
Part B (hypertrees). All 3*5*7 = 105 attachment sequences of 4-edge linear hypertrees on 9 vertices
(plus the 2- and 3-edge ones), each realized by the Step 1.5 procedure starting from {0,1,2};
check (4,5) by brute force and the AP set exactly.
Part C (Step 1.4). For every form of Phi on an index set split into parts A (4 indices) and B
(4 indices) that involves both parts: phi_B(1) = 0 iff phi_B = X_p - X_q (p != q), and that only
arises from a parallelogram form split 2+2 with opposite signs in B.
Part D (midpoint counter-case). If u is the midpoint of (a,u,b) and p = x_u - delta, q = x_u + delta
then p + q = x_a + x_b for every delta.
"""
import itertools, json, random, sys
from fractions import Fraction

def diffs_ok_45(pts):
    pts = sorted(pts)
    assert len(set(pts)) == len(pts)
    for B in itertools.combinations(pts, 4):
        d = {abs(x - y) for x, y in itertools.combinations(B, 2)}
        if len(d) < 5:
            return False
    return True

def aps(pts):
    s = set(pts); P = sorted(pts); out = set()
    for i, a in enumerate(P):
        for c in P[i + 2:]:
            if (a + c) % 2 == 0 and (a + c) // 2 in s:
                out.add((a, (a + c) // 2, c))
    return out

def phi_forms(idx):
    """All forms of Phi over index list idx, as dicts index->coef (one sign per form)."""
    F = []
    for i, j in itertools.combinations(idx, 2):
        F.append(('diff', {i: 1, j: -1}))
    pairs = [pr for pr in itertools.combinations(idx, 2)]
    for P1, P2 in itertools.combinations(pairs, 2):
        if set(P1) & set(P2):
            continue  # overlapping index: reduces to a difference form (already listed)
        F.append(('par', {P1[0]: 1, P1[1]: 1, P2[0]: -1, P2[1]: -1}))
    for j in idx:
        rest = [k for k in idx if k != j]
        for i, k in itertools.combinations(rest, 2):
            F.append(('ap', {i: 1, k: 1, j: -2}))
    return F

def partA(A, u, rng):
    names = list(range(len(A))) + ['p', 'q']
    val = {i: (A[i], 0) for i in range(len(A))}
    val['p'] = (A[u], 1); val['q'] = (A[u], 2)
    zero_delta = []; roots = set(); bad_struct = 0
    # enumerate only forms involving p or q
    for kind, f in phi_forms(names):
        if 'p' not in f and 'q' not in f:
            continue
        c0 = sum(c * val[k][0] for k, c in f.items())
        c1 = sum(c * val[k][1] for k, c in f.items())
        if c1 == 0:
            zero_delta.append((kind, f, c0))
        else:
            roots.add(Fraction(-c0, c1))
    # (A1) structure of zero-delta forms
    for kind, f, c0 in zero_delta:
        ok = (kind == 'ap' and f.get('p') == -2 and f.get('q') == 1 and len(f) == 3)
        if not ok:
            bad_struct += 1
    # (A2) values
    vanish = [(f, c0) for kind, f, c0 in zero_delta if c0 == 0]
    a2_ok = (len(vanish) == 1 and set(vanish[0][0]) == {u, 'p', 'q'})
    a2_vals_ok = all(c0 == A[[k for k in f if k not in ('p', 'q')][0]] - A[u] for kind, f, c0 in zero_delta if kind == 'ap')
    # (A3) random delta avoiding roots
    while True:
        d = rng.randint(1, 10**6) * rng.choice([1, -1])
        if Fraction(d) not in roots:
            break
    newpts = list(A) + [A[u] + d, A[u] + 2 * d]
    ok45 = len(set(newpts)) == len(newpts) and diffs_ok_45(newpts)
    want = aps(A) | {tuple(sorted((A[u], A[u] + d, A[u] + 2 * d)))}
    want = {(min(t), sorted(t)[1], max(t)) for t in want}
    got = aps(newpts)
    return dict(n_zero_delta=len(zero_delta), bad_struct=bad_struct, a2_ok=a2_ok, a2_vals_ok=a2_vals_ok,
                ok45=ok45, ap_exact=(got == want), n_roots=len(roots))

def partB(rng):
    res = {'seqs': 0, 'ok': 0, 'retries': 0}
    for k in (2, 3, 4):
        choices = [range(3 + 2 * t) for t in range(k - 1)]
        for seq in itertools.product(*choices):
            res['seqs'] += 1
            for attempt in range(50):
                pts = [0, 1000003, 2000006]  # first AP, generic-ish step
                edges = [(0, 1, 2)]
                for t, u in enumerate(seq):
                    d = rng.randint(1, 10**9)
                    pts += [pts[u] + d, pts[u] + 2 * d]
                    m = len(pts)
                    edges.append((u, m - 2, m - 1))
                if len(set(pts)) != len(pts) or not diffs_ok_45(pts):
                    res['retries'] += 1; continue
                want = {tuple(sorted((pts[a], pts[b], pts[c]))) for a, b, c in edges}
                got = {tuple(sorted(t)) for t in aps(pts)}
                if got != want:
                    res['retries'] += 1; continue
                res['ok'] += 1
                break
    return res

def partC():
    idxA = ['a0', 'a1', 'a2', 'a3']; idxB = ['b0', 'b1', 'b2', 'b3']
    viol = 0; zero_cases = 0; zero_types = set()
    for kind, f in phi_forms(idxA + idxB):
        fa = {k: c for k, c in f.items() if k.startswith('a')}
        fb = {k: c for k, c in f.items() if k.startswith('b')}
        if not fa or not fb:
            continue
        s = sum(fb.values())
        if s == 0:
            zero_cases += 1
            vals = sorted(fb.values())
            if not (len(fb) == 2 and vals == [-1, 1]):
                viol += 1
            zero_types.add((kind, len(fa), len(fb)))
    return dict(zero_cases=zero_cases, violations=viol, zero_types=sorted(zero_types))

def main():
    rng = random.Random(20261027)
    sets = []
    rec = json.load(open('/home/user/Erdos-757/data/small_records.json'))
    def walk(o):
        if isinstance(o, list) and o and all(isinstance(x, int) for x in o) and len(o) >= 4:
            sets.append(sorted(o))
        elif isinstance(o, dict):
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(rec)
    sets = [s for s in sets if len(set(s)) == len(s) and diffs_ok_45(s)]
    # also random (4,5)-sets grown greedily from random integers
    for _ in range(20):
        S = []
        while len(S) < rng.randint(6, 12):
            x = rng.randint(0, 5000)
            if x not in S and diffs_ok_45(S + [x]) if len(S) >= 3 else x not in S:
                S.append(x)
        sets.append(sorted(S))
    tot = dict(cases=0, bad_struct=0, a2_fail=0, a2_vals_fail=0, not45=0, ap_mismatch=0, zero_delta_forms=0)
    for A in sets:
        for u in range(len(A)):
            r = partA(A, u, rng)
            tot['cases'] += 1
            tot['zero_delta_forms'] += r['n_zero_delta']
            tot['bad_struct'] += r['bad_struct']
            tot['a2_fail'] += (not r['a2_ok'])
            tot['a2_vals_fail'] += (not r['a2_vals_ok'])
            tot['not45'] += (not r['ok45'])
            tot['ap_mismatch'] += (not r['ap_exact'])
    print('Part A (Step 1.5 delta argument):', len(sets), 'base sets;', tot)
    print('Part B (hypertrees with 2-4 edges by Step 1.5 procedure):', partB(rng))
    print('Part C (Step 1.4 coefficient sums):', partC())
    # Part D
    dfail = 0
    for A in sets:
        for (a, b, c) in aps(A):
            for d in (1, 7, 1001):
                if (b - d) + (b + d) != a + c: dfail += 1
    print('Part D (midpoint counter-case p+q=a+b always):', 'fails', dfail)

main()
