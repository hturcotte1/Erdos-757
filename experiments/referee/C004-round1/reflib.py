"""Independent referee library for claim C004 (written from scratch; imports nothing from e757/ or judge/).

All decisions use Python ints (exact).  numpy int64 tables are used only to hold small exact integers
(values in [-10^6, 10^3]); no floats are used anywhere in a decision.
"""
import itertools
import json
from collections import defaultdict

import numpy as np

NEG = -10 ** 6  # sentinel for an infeasible partial assignment (true values are in 0..n)


# ---------------------------------------------------------------- claim parsing
class DupKeyError(ValueError):
    pass


def _no_dup_hook(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise DupKeyError(f"duplicate JSON keys: {keys}")
    return dict(pairs)


def load_claim(path):
    with open(path) as fh:
        txt = fh.read()
    return json.loads(txt, object_pairs_hook=_no_dup_hook)


def as_int_list(raw):
    out = []
    for x in raw:
        if isinstance(x, bool) or not isinstance(x, int):
            raise TypeError(f"entry {x!r} is not a JSON integer")
        out.append(x)
    return out


# ---------------------------------------------------------------- (4,5) test, literal
def is45_literal(A):
    """Every 4-subset has >= 5 distinct absolute differences. Literal enumeration of all C(n,4) subsets.
    Returns (ok, min_distinct, number_of_4sets_with_exactly_5, first_bad, total_checked)."""
    mind = 7
    n5 = 0
    tot = 0
    bad = None
    for q in itertools.combinations(A, 4):
        a, b, c, d = q
        ds = {abs(a - b), abs(a - c), abs(a - d), abs(b - c), abs(b - d), abs(c - d)}
        k = len(ds)
        tot += 1
        if k < mind:
            mind = k
        if k == 5:
            n5 += 1
        if k < 5 and bad is None:
            bad = q
    return bad is None, mind, n5, bad, tot


# ---------------------------------------------------------------- Sidon, from the definition
def is_sidon_sums(S):
    """Definition: all sums x + y with x <= y in S are distinct."""
    S = sorted(S)
    sums = [S[i] + S[j] for i in range(len(S)) for j in range(i, len(S))]
    return len(sums) == len(set(sums))


def is_sidon_diffs(S):
    """Equivalent definition: all positive differences y - x (x < y) are distinct."""
    S = sorted(S)
    diffs = [S[j] - S[i] for i in range(len(S)) for j in range(i + 1, len(S))]
    return len(diffs) == len(set(diffs))


def forbidden_sets(A):
    """From the definition only: S is Sidon iff it contains no set {x,y} u {z,w} with x+y = z+w,
    x<=y, z<=w, {x,y} != {z,w}.  Returns the list of minimal-by-construction forbidden index sets
    (as sorted tuples, deduplicated) and a census by size.  Does NOT assume weak Sidon."""
    n = len(A)
    by_sum = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            by_sum[A[i] + A[j]].append((i, j))
    forb = set()
    for s, prs in by_sum.items():
        if len(prs) < 2:
            continue
        for p, q in itertools.combinations(prs, 2):
            forb.add(tuple(sorted(set(p) | set(q))))
    census = defaultdict(int)
    for F in forb:
        census[len(F)] += 1
    return sorted(forb), dict(census)


def ap_triples(A):
    """3-APs (i<j<k by value, A sorted) found directly: A[i] + A[k] == 2*A[j]."""
    pos = {x: i for i, x in enumerate(A)}
    out = []
    n = len(A)
    for i in range(n):
        for k in range(i + 2, n):
            s = A[i] + A[k]
            if s % 2 == 0 and s // 2 in pos:
                out.append((i, pos[s // 2], k))
    return out


# ---------------------------------------------------------------- exact max independent set
def greedy_order(nv, forb):
    """Min-degree (ties: min-fill, then index) elimination order on the primal graph. Returns (order, width)."""
    adj = {v: set() for v in range(nv)}
    for F in forb:
        for a in F:
            for b in F:
                if a != b:
                    adj[a].add(b)
    alive = set(range(nv))
    order = []
    width = 0
    while alive:
        best = None
        for v in alive:
            nb = adj[v]
            deg = len(nb)
            fill = 0
            nbl = list(nb)
            for i in range(len(nbl)):
                for j in range(i + 1, len(nbl)):
                    if nbl[j] not in adj[nbl[i]]:
                        fill += 1
            key = (deg, fill, v)
            if best is None or key < best[0]:
                best = (key, v)
        v = best[1]
        nb = list(adj[v])
        width = max(width, len(nb))
        for a in nb:
            for b in nb:
                if a != b:
                    adj[a].add(b)
            adj[a].discard(v)
        del adj[v]
        alive.discard(v)
        order.append(v)
    return order, width


def ve_max_independent(nv, forb, order=None):
    """Exact max |I| over I subset of range(nv) containing no forbidden set, by bucket (variable) elimination.
    Exact for ANY elimination order (the order only affects the running time).
    Returns (optimum, width, argmax_set)."""
    if order is None:
        order, width = greedy_order(nv, forb)
    else:
        width = None
    assert sorted(order) == list(range(nv))
    factors = []
    for v in range(nv):
        factors.append(((v,), np.array([0, 1], dtype=np.int64)))
    for F in forb:
        sc = tuple(sorted(F))
        t = np.zeros((2,) * len(sc), dtype=np.int64)
        t[(1,) * len(sc)] = NEG
        factors.append((sc, t))
    trace = []
    maxw = 0
    for v in order:
        bucket = [f for f in factors if v in f[0]]
        factors = [f for f in factors if v not in f[0]]
        W = sorted(set().union(*[set(f[0]) for f in bucket]))
        maxw = max(maxw, len(W) - 1)
        comb = np.zeros((2,) * len(W), dtype=np.int64)
        for sc, t in bucket:
            shape = [2 if w in sc else 1 for w in W]
            comb = comb + t.reshape(shape)
        comb = np.maximum(comb, NEG)  # clamp: keeps sentinels bounded, exact values (>= 0) untouched
        ax = W.index(v)
        new = comb.max(axis=ax)
        newsc = tuple(w for w in W if w != v)
        trace.append((v, W, comb))
        factors.append((newsc, new))
    total = 0
    for sc, t in factors:
        assert sc == ()
        total += int(t)
    # traceback
    assign = {}
    for v, W, comb in reversed(trace):
        idx = tuple(slice(None) if w == v else assign[w] for w in W)
        vals = comb[idx]
        assign[v] = 1 if int(vals[1]) >= int(vals[0]) else 0
    I = sorted(v for v in range(nv) if assign[v] == 1)
    return total, (width if width is not None else maxw), I


def check_independent(I, forb):
    s = set(I)
    return all(not set(F) <= s for F in forb)


# ---------------------------------------------------------------- brute force (n <= 22), from forbidden sets
def brute_max(nv, forb):
    assert nv <= 22
    N = 1 << nv
    masks = np.arange(N, dtype=np.int64)
    good = np.ones(N, dtype=bool)
    for F in forb:
        fm = 0
        for v in F:
            fm |= 1 << v
        good &= (masks & fm) != fm
    # popcount
    pc = np.zeros(N, dtype=np.int64)
    m = masks.copy()
    while True:
        nz = m != 0
        if not nz.any():
            break
        pc += (m & 1)
        m >>= 1
    best = int(pc[good].max())
    cnt = int((pc[good] == best).sum())
    return best, cnt


def brute_max_by_definition(A):
    """Brute force straight from the definition (no forbidden-set preprocessing): every subset, Sidon by sums.
    Only for small n (<= 16)."""
    n = len(A)
    best = 0
    for r in range(n, 0, -1):
        for S in itertools.combinations(A, r):
            if is_sidon_sums(S):
                return r
    return best


# ---------------------------------------------------------------- SAT with own sequential counter
def atmost_seqcounter(lits, K, top):
    """Sinz sequential counter for sum(lits) <= K. Returns (clauses, new_top)."""
    n = len(lits)
    cls = []
    if K >= n:
        return cls, top
    if K == 0:
        return [[-l] for l in lits], top
    s = {}
    for i in range(1, n):  # registers s[i][j] for i = 1..n-1, j = 1..K
        for j in range(1, K + 1):
            top += 1
            s[(i, j)] = top
    l = {i + 1: lits[i] for i in range(n)}
    cls.append([-l[1], s[(1, 1)]])
    for j in range(2, K + 1):
        cls.append([-s[(1, j)]])
    for i in range(2, n):
        cls.append([-l[i], s[(i, 1)]])
        cls.append([-s[(i - 1, 1)], s[(i, 1)]])
        for j in range(2, K + 1):
            cls.append([-l[i], -s[(i - 1, j - 1)], s[(i, j)]])
            cls.append([-s[(i - 1, j)], s[(i, j)]])
        cls.append([-l[i], -s[(i - 1, K)]])
    cls.append([-l[n], -s[(n - 1, K)]])
    return cls, top


def sidon_cnf(nv, forb, k):
    """CNF: variables 1..nv (x_v = vertex v chosen); no forbidden set fully chosen; at least k chosen
    (= at most nv - k unchosen, sequential counter over the negative literals)."""
    cls = [[-(v + 1) for v in F] for F in forb]
    card, top = atmost_seqcounter([-(v + 1) for v in range(nv)], nv - k, nv)
    return cls + card, top


# ---------------------------------------------------------------- forward RUP (DRUP) checker
def rup_check(clauses, proof_lines, nvars):
    """Forward check of a DRUP proof: every added lemma must be RUP w.r.t. all clauses so far
    (deletions are ignored: sound, only slower).  Returns (ok, n_lemmas, empty_clause_derived)."""
    db = [list(c) for c in clauses]
    watches = defaultdict(list)  # lit -> list of clause idx watching it
    units = []

    def add(c):
        idx = len(db) - 1
        if len(c) == 0:
            return
        if len(c) == 1:
            units.append(c[0])
        else:
            watches[c[0]].append(idx)
            watches[c[1]].append(idx)

    for i, c in enumerate(clauses):
        db[i] = list(c)
    db_len0 = len(db)
    for i in range(db_len0):
        c = db[i]
        if len(c) == 1:
            units.append(c[0])
        elif len(c) >= 2:
            watches[c[0]].append(i)
            watches[c[1]].append(i)

    def propagate(assumed):
        val = {}
        trail = []

        def setlit(x):
            v = val.get(abs(x))
            want = x > 0
            if v is None:
                val[abs(x)] = want
                trail.append(x)
                return True
            return v == want

        for x in units:
            if not setlit(x):
                return True
        for x in assumed:
            if not setlit(x):
                return True
        qi = 0
        while qi < len(trail):
            x = trail[qi]
            qi += 1
            fl = -x  # literal that became false
            wl = watches[fl]
            j = 0
            while j < len(wl):
                ci = wl[j]
                c = db[ci]
                if c[0] == fl:
                    c[0], c[1] = c[1], c[0]
                # c[1] == fl now
                o = c[0]
                vo = val.get(abs(o))
                if vo is not None and vo == (o > 0):
                    j += 1
                    continue
                found = False
                for k in range(2, len(c)):
                    lk = c[k]
                    vk = val.get(abs(lk))
                    if vk is None or vk == (lk > 0):
                        c[1], c[k] = c[k], c[1]
                        watches[c[1]].append(ci)
                        wl[j] = wl[-1]
                        wl.pop()
                        found = True
                        break
                if found:
                    continue
                if vo is None:
                    val[abs(o)] = o > 0
                    trail.append(o)
                    j += 1
                    continue
                return True  # conflict
        return False

    nl = 0
    empty = False
    for line in proof_lines:
        line = line.strip()
        if not line or line.startswith('c'):
            continue
        if line.startswith('d'):
            continue
        lits = [int(t) for t in line.split()]
        assert lits[-1] == 0
        lits = lits[:-1]
        nl += 1
        if not propagate([-x for x in lits]):
            return False, nl, empty
        if len(lits) == 0:
            empty = True
            break
        db.append(lits)
        if len(lits) == 1:
            units.append(lits[0])
        else:
            watches[lits[0]].append(len(db) - 1)
            watches[lits[1]].append(len(db) - 1)
    if not empty:
        # the empty clause may be implied by unit propagation at the end
        if propagate([]):
            empty = True
    return True, nl, empty
