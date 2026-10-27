"""Round-2 re-check of the W7 update in L022 commit 4c32ca5 (independent; no e757/judge/prover imports).
(1) Q_8 = {a c1 c2, a c3 c4, a c5 c6, b c2 c3, b c4 c5, b c6 c1} occurs as a sub-hypergraph of each of
    the 6 classes of cell(25,23,11,4) (two vertices a,b with three edges each whose link pairs cover
    the same 6 vertices; linearity makes the two link matchings a hexagon).
(2) Q_8 is not contained in the AP hypergraph of any (4,5)-set: for every injective midpoint labelling,
    the solution space V of the 6 AP equations (exact RREF over Q) makes some forbidden form of Phi
    (X_i-X_j, X_i+X_j-X_k-X_l, or an extra AP form X_i+X_k-2X_j) vanish identically on V.
"""
import itertools, re
from fractions import Fraction

def nullspace(rows, n):
    M = [list(map(Fraction, r)) for r in rows]
    piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        inv = 1 / M[r][c]; M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * n; v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -M[i][f]
        basis.append(v)
    return basis

def forms(n):
    for i, j in itertools.combinations(range(n), 2):
        yield ('eq', {i: 1, j: -1})
    prs = list(itertools.combinations(range(n), 2))
    for P, Q in itertools.combinations(prs, 2):
        if set(P) & set(Q): continue
        yield ('par', {P[0]: 1, P[1]: 1, Q[0]: -1, Q[1]: -1})
    for j in range(n):
        for i, k in itertools.combinations([x for x in range(n) if x != j], 2):
            yield ('ap', {i: 1, k: 1, j: -2})

# (2) non-realizability of Q_8: vertices a=0, b=1, c1..c6 = 2..7
a, b = 0, 1; c = {i: i + 1 for i in range(1, 7)}
Q8 = [(a, c[1], c[2]), (a, c[3], c[4]), (a, c[5], c[6]), (b, c[2], c[3]), (b, c[4], c[5]), (b, c[6], c[1])]
n = 8
tot = inj = dead = 0; reasons = {}
FORMS = list(forms(n))
for mids in itertools.product(*[e for e in Q8]):
    tot += 1
    if len(set(mids)) < len(mids): continue
    inj += 1
    rows = []
    apset = set()
    for e, mu in zip(Q8, mids):
        ends = [x for x in e if x != mu]
        r = [0] * n; r[ends[0]] += 1; r[ends[1]] += 1; r[mu] -= 2; rows.append(r)
        apset.add((mu, frozenset(ends)))
    B = nullspace(rows, n)
    killed = None
    for kind, f in FORMS:
        if kind == 'ap':
            j = [k for k, v in f.items() if v == -2][0]
            ends = frozenset(k for k, v in f.items() if v == 1)
            if (j, ends) in apset: continue
        if all(sum(cf * v[k] for k, cf in f.items()) == 0 for v in B):
            killed = kind; break
    if killed:
        dead += 1; reasons[killed] = reasons.get(killed, 0) + 1
print('Q8: labellings', tot, 'injective', inj, 'dead', dead, reasons)

# (1) containment in the 6 classes
lines = [l for l in open('/home/user/Erdos-757/experiments/20261027-0340-induction-n28-n29-f25/lists/cell_25_23_11_D4.txt') if l.startswith('FOUND')]
for idx, l in enumerate(lines):
    E = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
    inc = {}
    for e in E:
        for v in e: inc.setdefault(v, []).append(e)
    occ = 0
    for u, w in itertools.permutations([v for v in inc if len(inc[v]) >= 3], 2):
        if any(u in e and w in e for e in E):
            continue  # a, b are not adjacent in Q_8
        for Ea in itertools.combinations(inc[u], 3):
            La = [frozenset(set(e) - {u}) for e in Ea]
            Sa = set().union(*La)
            if len(Sa) != 6: continue
            for Eb in itertools.combinations(inc[w], 3):
                Lb = [frozenset(set(e) - {w}) for e in Eb]
                if set().union(*Lb) == Sa and not (set(La) & set(Lb)):
                    occ += 1
    print('class', idx, 'Q8 occurrences (ordered a,b; edge choices):', occ)
