"""
Hypergraph-first simulated annealing over (near-)saturated midpoint maps (Track U1).

State  = Map(n, lo, hi, free, mid, pv)
  mid[j] = (i, k)   x_j = (x_i + x_k)/2 for every j not in {lo, hi} U free   (i<k, both != j)
  free   = vertices with no equation; their values pv[v] (Fractions in (0,1)) are generic parameters
  The labeled edges (i, j, k) must form a LINEAR hypergraph (every pair of vertices in <= 1 edge).
Values: boundary x_lo = 0, x_hi = 1, x_free = pv; interior = harmonic (hitting probabilities).

Exact quantities (`evaluate`, exact=True):
  alpha     independence number of the ACTUAL AP hypergraph of the value set (= h for weak Sidon sets)
  extra_ap  actual APs that are not listed edges
  repeated  number of colliding pairs of pair-sums x+y (x<y)  (weak-Sidon violations = parallelograms)
  coincide  number of equal value pairs;  singular flag
  is45      exact (4,5) check (only computed when no penalty above)
Floats (`fast_eval`) are used only inside the annealer; every hit is re-checked exactly.
"""
from __future__ import annotations

import itertools
import json
import math
import random
import time
from fractions import Fraction

import numpy as np

from .core import ap_edges, is_45_set
from .saturated import alpha_of_edges, map_of_set, to_integers


# ------------------------------------------------------------------ state
class Map:
    __slots__ = ("n", "lo", "hi", "free", "mid", "pv")

    def __init__(self, n, lo, hi, mid, free=(), pv=None):
        self.n, self.lo, self.hi = n, lo, hi
        self.mid = {j: tuple(sorted(e)) for j, e in mid.items()}
        self.free = tuple(free)
        self.pv = dict(pv or {})

    def copy(self):
        return Map(self.n, self.lo, self.hi, self.mid, self.free, self.pv)

    def edges(self):
        return [(i, j, k) for j, (i, k) in self.mid.items()]

    def key(self):
        return (tuple(sorted(self.mid.items())), self.free)

    def to_json(self):
        return {"n": self.n, "lo": self.lo, "hi": self.hi, "mid": {str(j): list(e) for j, e in self.mid.items()},
                "free": list(self.free), "pv": {str(v): str(x) for v, x in self.pv.items()}}


def map_from_set(A):
    """Saturated map of a (4,5)-set (uses `map_of_set`)."""
    lo, hi, mid = map_of_set(A)
    return Map(len(A), lo, hi, mid)


def is_linear_map(mid):
    used = set()
    for j, (i, k) in mid.items():
        for p in ((i, j), (j, k), (i, k)):
            p = frozenset(p)
            if p in used:
                return False
            used.add(p)
    return True


def _pairs(i, j, k):
    return (frozenset((i, j)), frozenset((j, k)), frozenset((i, k)))


def _used_pairs(mid, skip=()):
    used = set()
    for j, (i, k) in mid.items():
        if j in skip:
            continue
        used.update(_pairs(i, j, k))
    return used


def random_linear_map(n, rng, nfree=0, lo=0, hi=None, tries=200):
    """Random saturated linear map built edge by edge (constraint propagation)."""
    hi = n - 1 if hi is None else hi
    inner = [v for v in range(n) if v not in (lo, hi)]
    for _ in range(tries):
        free = tuple(rng.sample(inner, nfree)) if nfree else ()
        order = [v for v in inner if v not in free]
        rng.shuffle(order)
        mid, used, ok = {}, set(), True
        for j in order:
            cand = [v for v in range(n) if v != j]
            for _a in range(60):
                i, k = rng.sample(cand, 2)
                ps = _pairs(i, j, k)
                if not any(p in used for p in ps):
                    mid[j] = (i, k)
                    used.update(ps)
                    break
            else:
                ok = False
                break
        if ok:
            pv = {v: Fraction(rng.randint(1, 996), 997) for v in free}
            return Map(n, lo, hi, mid, free, pv)
    raise RuntimeError("could not build a random linear map")


def extend_map(m, extra, rng, nfree=0):
    """Add `extra` new vertices to a saturated map. New vertices are renumbered after the old interior so
    that hi stays the last label; new vertices get random linear-compatible equations."""
    old_n = m.n
    n = old_n + extra
    # relabel: old hi -> n-1 ; new vertices take old_n-1 .. n-2
    rl = {v: v for v in range(old_n)}
    rl[m.hi] = n - 1
    newv = list(range(old_n - 1, n - 1)) if m.hi == old_n - 1 else list(range(old_n, n))
    if m.hi != old_n - 1:
        rl[m.hi] = n - 1
        # old vertex old_n-1 stays ; new vertices old_n .. n-2 and also the freed label m.hi
        newv = [m.hi] + list(range(old_n, n - 1))
    mid = {rl[j]: (rl[a], rl[b]) for j, (a, b) in m.mid.items()}
    for _ in range(500):
        mid2, used = dict(mid), _used_pairs(mid)
        ok = True
        for j in newv:
            cand = [v for v in range(n) if v != j]
            for _a in range(80):
                i, k = rng.sample(cand, 2)
                ps = _pairs(i, j, k)
                if not any(p in used for p in ps):
                    mid2[j] = (i, k)
                    used.update(ps)
                    break
            else:
                ok = False
                break
        if ok:
            return Map(n, rl[m.lo], n - 1, mid2)
    raise RuntimeError("extend failed")


# ------------------------------------------------------------------ exact evaluation
_QUADS = {}


def is45_ints(ints):
    """Exact (4,5) test for integers (numpy, vectorised over all 4-subsets). Agrees with core.is_45_set."""
    n = len(ints)
    if n not in _QUADS:
        q = np.array(list(itertools.combinations(range(n), 4)))
        pr = np.array(list(itertools.combinations(range(4), 2)))
        _QUADS[n] = (q, pr)
    q, pr = _QUADS[n]
    big = max(abs(x) for x in ints) >= 2 ** 60
    a = np.array(ints, dtype=object if big else np.int64)
    pts = a[q]                                   # (Q,4)
    d = np.abs(pts[:, pr[:, 0]] - pts[:, pr[:, 1]])   # (Q,6)
    d = np.sort(d, axis=1)
    distinct = 1 + np.count_nonzero(d[:, 1:] != d[:, :-1], axis=1)
    return bool(np.all(distinct >= 5))


def solve_exact(m):
    """Exact Fraction solution (list) of the state, or None if singular. Integer (fraction-free) elimination."""
    n = m.n
    Q = 1
    for v in m.free:
        Q = Q * Fraction(m.pv[v]).denominator // math.gcd(Q, Fraction(m.pv[v]).denominator)
    bval = {m.lo: 0, m.hi: Q}
    for v in m.free:
        f = Fraction(m.pv[v])
        bval[v] = int(f * Q)
    unknown = [v for v in range(n) if v not in bval]
    if set(m.mid) != set(unknown):
        raise ValueError("map must have one equation per non-boundary non-free vertex")
    col = {v: c for c, v in enumerate(unknown)}
    size = len(unknown)
    rows = []
    for j in unknown:
        i, k = m.mid[j]
        row = [0] * (size + 1)
        row[col[j]] += 2
        for v in (i, k):
            if v in bval:
                row[size] += bval[v]
            else:
                row[col[v]] -= 1
        rows.append(row)
    for c in range(size):
        piv = next((t for t in range(c, size) if rows[t][c] != 0), None)
        if piv is None:
            return None
        rows[c], rows[piv] = rows[piv], rows[c]
        pr = rows[c]
        p = pr[c]
        for t in range(size):
            if t != c and rows[t][c] != 0:
                f = rows[t][c]
                r = [p * a - f * b for a, b in zip(rows[t], pr)]
                g = 0
                for x in r:
                    g = math.gcd(g, x)
                if g > 1:
                    r = [x // g for x in r]
                rows[t] = r
    vals = [None] * n
    for v, x in bval.items():
        vals[v] = Fraction(x, Q)
    for v in unknown:
        vals[v] = Fraction(rows[col[v]][size], rows[col[v]][col[v]] * Q)
    return vals


def evaluate(m, exact=True):
    """Exact evaluation. Returns dict with alpha, extra_ap, repeated, coincide, singular, is45, vals."""
    vals = solve_exact(m)
    if vals is None:
        return {"singular": True, "alpha": None, "extra_ap": None, "repeated": None, "coincide": None,
                "is45": False, "vals": None, "score": 1e9}
    n = m.n
    coincide = n - len(set(vals))
    sums = {}
    for a, b in itertools.combinations(range(n), 2):
        sums.setdefault(vals[a] + vals[b], []).append((a, b))
    repeated = sum(len(g) * (len(g) - 1) // 2 for g in sums.values())
    if coincide:
        return {"singular": False, "alpha": None, "extra_ap": None, "repeated": repeated, "coincide": coincide,
                "is45": False, "vals": vals, "score": 1e6}
    pos = {v: t for t, v in enumerate(vals)}
    got = {frozenset((pos[a], pos[b], pos[c])) for a, b, c in ap_edges(vals)}
    want = {frozenset(e) for e in m.edges()}
    extra = len(got - want)
    alpha = alpha_of_edges(n, [tuple(e) for e in got])
    is45 = False
    if extra == 0 and repeated == 0:
        is45 = is45_ints(to_integers(vals))
    return {"singular": False, "alpha": alpha, "extra_ap": extra, "repeated": repeated, "coincide": 0,
            "is45": is45, "vals": vals, "missing_edges": len(want - got), "score": alpha + extra + repeated}


# ------------------------------------------------------------------ fast float evaluation
class FastEval:
    def __init__(self, n):
        self.n = n
        self.iu = np.triu_indices(n, 1)
        self.alpha_cache = {}

    def solve(self, m):
        n = m.n
        bval = {m.lo: 0.0, m.hi: 1.0}
        for v in m.free:
            bval[v] = float(m.pv[v])
        unknown = [v for v in range(n) if v not in bval]
        col = {v: c for c, v in enumerate(unknown)}
        u = len(unknown)
        M = np.zeros((u, u))
        b = np.zeros(u)
        for r, j in enumerate(unknown):
            M[r, r] += 2.0
            for v in m.mid[j]:
                if v in bval:
                    b[r] += bval[v]
                else:
                    M[r, col[v]] -= 1.0
        try:
            x = np.linalg.solve(M, b)
        except np.linalg.LinAlgError:
            return None
        if not np.all(np.isfinite(x)) or x.min() < -1e-9 or x.max() > 1 + 1e-9:
            return None
        if np.abs(M @ x - b).max() > 1e-9:
            return None
        vals = np.empty(n)
        for v, t in bval.items():
            vals[v] = t
        for v, c in col.items():
            vals[v] = x[c]
        return vals

    def collisions(self, vals):
        s = np.sort(vals[self.iu[0]] + vals[self.iu[1]])
        return int(np.count_nonzero(np.diff(s) < 1e-9))

    def alpha(self, m):
        k = m.key()
        a = self.alpha_cache.get(k)
        if a is None:
            if len(self.alpha_cache) > 200000:
                self.alpha_cache.clear()
            a = alpha_of_edges(m.n, m.edges())
            self.alpha_cache[k] = a
        return a

    def score(self, m, w=1.0, singular_pen=40.0):
        """Returns (score, alpha, collisions); alpha of the intended hypergraph (equals h when coll==0)."""
        a = self.alpha(m)
        vals = self.solve(m)
        if vals is None:
            return a + singular_pen, a, -1
        c = self.collisions(vals)
        return a + w * c, a, c


# ------------------------------------------------------------------ moves
def propose(m, rng):
    """Return a new Map differing by one local move, or None if the random move is illegal."""
    n = m.n
    js = list(m.mid)
    r = rng.random()
    new = m.copy()
    if r < 0.40:  # rewire one midpoint to a fresh pair
        j = rng.choice(js)
        used = _used_pairs(m.mid, skip=(j,))
        for _ in range(30):
            i, k = rng.sample([v for v in range(n) if v != j], 2)
            if not any(p in used for p in _pairs(i, j, k)):
                new.mid[j] = (min(i, k), max(i, k))
                return new
        return None
    if r < 0.75:  # replace one endpoint
        j = rng.choice(js)
        i, k = m.mid[j]
        if rng.random() < 0.5:
            i, k = k, i
        used = _used_pairs(m.mid, skip=(j,))
        for _ in range(30):
            i2 = rng.randrange(n)
            if i2 in (i, j, k):
                continue
            if not any(p in used for p in _pairs(i2, j, k)):
                new.mid[j] = (min(i2, k), max(i2, k))
                return new
        return None
    if r < 0.93 or not m.free:  # swap pairs of two midpoints
        j1, j2 = rng.sample(js, 2)
        (a1, b1), (a2, b2) = m.mid[j1], m.mid[j2]
        if j1 in (a2, b2) or j2 in (a1, b1):
            return None
        new.mid[j1], new.mid[j2] = (a2, b2), (a1, b1)
        if not is_linear_map(new.mid):
            return None
        return new
    # free vertex handling: transfer role, or re-draw its generic value
    f = rng.choice(m.free)
    if rng.random() < 0.4:
        new.pv[f] = Fraction(rng.randint(1, 996), 997)
        return new
    j = rng.choice(js)  # j becomes free, f gets j's old pair (re-pointing allowed)
    if j in (m.lo, m.hi):
        return None
    pair = m.mid[j]
    if f in pair:
        return None
    del new.mid[j]
    new.mid[f] = pair
    new.free = tuple(j if v == f else v for v in m.free)
    new.pv = {(j if v == f else v): x for v, x in m.pv.items()}
    if not is_linear_map(new.mid):
        return None
    return new


# ------------------------------------------------------------------ hit handling
def exact_hit_check(m, target_h=None):
    """Exact verification of a candidate. Returns (is_valid_45_set, h, ints, info)."""
    ev = evaluate(m)
    if ev["singular"] or ev["coincide"] or ev["is45"] is False:
        return False, None, None, ev
    vals = ev["vals"]
    return True, ev["alpha"], sorted(to_integers(vals)), ev


# ------------------------------------------------------------------ the annealer
class Runner:
    def __init__(self, n, target, seed, nfree=0, w=1.0, seeds_from=None, log=None, ckpt=None, T0=0.7, T1=0.12,
                 cycle=6000):
        self.n, self.target, self.seed, self.nfree = n, target, seed, nfree
        self.rng = random.Random(seed)
        self.fe = FastEval(n)
        self.w = w
        self.seeds_from = seeds_from or []  # list of (name, set)
        self.log = log or (lambda s: None)
        self.ckpt = ckpt
        self.T0, self.T1, self.cycle = T0, T1, cycle
        self.stats = {"evaluated": 0, "singular": 0, "coll0": 0, "valid45": 0, "hits": 0}
        self.valid_alpha = {}   # alpha -> number of DISTINCT exactly verified (4,5)-states
        self.seen_valid = set()
        self.coll0_alpha = {}   # float-level: alpha(E) of every evaluated state with no sum collision
        self.best = None        # dict
        self.hits = []
        self.best_score_seen = {"alpha": 99}
        self.cycles = 0

    # ---- helpers
    def initial(self):
        r = self.rng.random()
        if self.seeds_from and r < 0.5:
            name, A = self.rng.choice(self.seeds_from)
            m0 = map_from_set(A)
            extra = self.n - m0.n
            if extra >= 0:
                m = extend_map(m0, extra, self.rng) if extra else m0
                if self.nfree:
                    # make a random interior vertex free (drop its equation)
                    inner = [v for v in m.mid]
                    for v in self.rng.sample(inner, self.nfree):
                        del m.mid[v]
                        m.free += (v,)
                        m.pv[v] = Fraction(self.rng.randint(1, 996), 997)
                for _ in range(self.rng.randint(0, 6)):
                    q = propose(m, self.rng)
                    if q is not None:
                        m = q
                return m
        return random_linear_map(self.n, self.rng, self.nfree)

    def record(self, m, a, c):
        """Called for each evaluated state: bookkeeping, and exact verification of promising ones."""
        st = self.stats
        st["evaluated"] += 1
        if c == -1:
            st["singular"] += 1
        if c == 0:
            st["coll0"] += 1
            self.coll0_alpha[a] = self.coll0_alpha.get(a, 0) + 1
            if a * 7 < 4 * self.n or a <= self.target or self.rng.random() < 0.01:
                k = m.key() if not m.free else (m.key(), tuple(sorted(m.pv.items())))
                if k not in self.seen_valid:
                    ok, h, ints, ev = exact_hit_check(m)
                    if ok:
                        self.seen_valid.add(k)
                        st["valid45"] += 1
                        self.valid_alpha[h] = self.valid_alpha.get(h, 0) + 1
                        if self.best is None or h < self.best["h"]:
                            self.best = {"h": h, "n": self.n, "set": ints, "penalties": {"extra_ap": ev["extra_ap"], "repeated": ev["repeated"]},
                                         "map": m.to_json(), "seed": self.seed}
                            self.log(f"new best valid h={h} n={self.n} set={ints}")
                            self.dump()
                        if h * 7 < 4 * self.n:
                            self.hits.append((m.copy(), h, ints))
                            st["hits"] += 1
                            self.log(f"HIT h={h} n={self.n} set={ints}")
                            self.dump()
                    else:
                        self.seen_valid.add(k)  # avoid re-checking (counted as unrealizable)
                        st.setdefault("coll0_not45", 0)
                        st["coll0_not45"] += 1
        if a < self.best_score_seen["alpha"] and c == 0:
            self.best_score_seen["alpha"] = a

    def dump(self, path=None):
        path = path or self.ckpt
        if not path:
            return
        out = {"seed": self.seed, "n": self.n, "nfree": self.nfree, "stats": self.stats,
               "valid_alpha_distribution": self.valid_alpha, "coll0_alpha_distribution": self.coll0_alpha, "best": self.best,
               "hits": [{"h": h, "set": s} for _, h, s in self.hits], "time": time.time()}
        tmp = str(path) + ".tmp"
        with open(tmp, "w") as f:
            json.dump(out, f)
        import os
        os.replace(tmp, path)

    # ---- main loop
    def run(self, iters=None, seconds=None, on_hit=None):
        t0 = time.time()
        done = 0
        while True:
            cur = self.initial()
            s, a, c = self.fe.score(cur, self.w)
            self.record(cur, a, c)
            self.cycles += 1
            for it in range(self.cycle):
                T = self.T0 * (self.T1 / self.T0) ** (it / self.cycle)
                q = propose(cur, self.rng)
                if q is None:
                    continue
                s2, a2, c2 = self.fe.score(q, self.w)
                self.record(q, a2, c2)
                done += 1
                if s2 <= s or self.rng.random() < math.exp((s - s2) / T):
                    cur, s, a, c = q, s2, a2, c2
                if self.ckpt and done % 20000 == 0:
                    self.dump()
                if (iters is not None and done >= iters) or (seconds is not None and time.time() - t0 > seconds):
                    self.dump()
                    return self.stats
            if (iters is not None and done >= iters) or (seconds is not None and time.time() - t0 > seconds):
                self.dump()
                return self.stats


# ------------------------------------------------------------------ smooth hypergraph cost
class IndepCounter:
    """Counts independent sets of size k of the intended hypergraph (all 2^n subsets, vectorised).
    N_k == 0  <=>  alpha < k.  Smooth surrogate for alpha (independent subsets of a big independent set count)."""

    def __init__(self, n):
        self.n = n
        S = np.arange(1 << n, dtype=np.uint32)
        self.S = S
        pop = np.zeros(1 << n, dtype=np.int8)
        for b in range(n):
            pop += ((S >> b) & 1).astype(np.int8)
        self.pop = pop

    def counts(self, edges):
        """Return (alpha, popcount histogram of independent sets)."""
        bad = np.zeros(1 << self.n, dtype=bool)
        for (i, j, k) in edges:
            e = np.uint32((1 << i) | (1 << j) | (1 << k))
            bad |= (self.S & e) == e
        good = self.pop[~bad]
        return np.bincount(good, minlength=self.n + 1)
