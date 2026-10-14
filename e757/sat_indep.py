"""Independent SAT (python-sat) encoding of the abstract decision problem for class O'.

Written from the definitions below; it deliberately does NOT import e757.cpsat_model, e757.ordered_dfs
or any other e757 module, so that it can serve as a cross-check of certificates produced by them.

Definitions
-----------
Vertices are 0..n-1 in rank (sorted) order.  A labeled edge (i,j,k) with i<j<k is the arithmetic
progression i,j,k with midpoint j (2 x_j = x_i + x_k).  Because the midpoint of a sorted triple is its
middle element, an edge is just a 3-subset; the SAT variable x[i,j,k] says "this triple is an edge".
A pattern is a set E of edges.  It is in class O' iff

 (a) midpoint injective: every vertex j is the midpoint of at most one edge in E;
 (b) linear: two distinct edges of E share at most one vertex;
 (c) F7-free as an unlabeled hypergraph: no five edges of E form a copy of
     F7 = {012, 034, 056, 135, 246} (a subhypergraph, not necessarily induced);
 (d) monotone midpoints (kb/known_results.md K30): for edges (i,j,k), (i',j',k') in E with
     i <= i', k <= k' and (i,k) != (i',k') we have j < j'  (since x_j = (x_i+x_k)/2 < x_j');
 (e) no medial triangle (K31): E contains no (a,b,c), (a,p,e), (c,q,e) with a<b<c, a<p<e, c<q<e;
 (f) no forbidden core: data/forbidden_ordered_n7.json and data/forbidden_ordered_n8.json list ordered
     patterns on v vertices 0..v-1 (all vertices used) by their edge lists, deduplicated under the
     reflection j -> v-1-j.  For every strictly increasing map phi: {0..v-1} -> {0..n-1} (and for the
     reflected core too) the image edge set must not be entirely contained in E.

Decision problem  decide(n, T, m): is there E in O' on n vertices with exactly m edges and
alpha(E) <= T, where alpha <= T means every (T+1)-subset of the vertices contains an edge of E.

Encoding
--------
* variables x[i,j,k], one per triple;
* (a), (b), (d), (e): eager binary / ternary clauses;
* alpha <= T: eager, one clause per (T+1)-subset (OR of the triples inside it);
* exactly m edges: pysat.card CardEnc.equals (sequential counter);
* (f): eager for cores with <= `eager_max_v` vertices, lazy (counterexample guided) for the larger ones;
* (c) F7: lazy.  After every model all copies of F7 inside the model's edge set are searched by
  backtracking and the corresponding "not all five" no-good clauses are added, then we re-solve.
  The same lazy loop handles the lazy cores.  Lazy no-goods are consequences of the definition, so
  UNSAT answers are sound, and every SAT model returned has passed all checks.

API
---
decide(n, T, m, cores='hybrid', forbid_f7=True, extra_unit=None, time_limit=None, vertex1=None, ...)
    -> ('SAT', sorted edge list) | ('UNSAT', stats) | ('TIMEOUT', stats).
    m=None means "any number of edges" (decision only).
enumerate_all(n, T, m, ...) -> list of frozenset-like sorted edge tuples (all solutions, m fixed).
vertex1: None (no assumption), 0 (vertex 1 is not a midpoint) or k>=2 (edge (0,1,k) is present and is
    the edge of vertex 1).  extra_unit: iterable of ((i,j,k), bool) forcing variables.
"""
import itertools
import json
import os
import threading
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
_CORE_FILES = ("forbidden_ordered_n7.json", "forbidden_ordered_n8.json")

F7_EDGES = ((0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6))


# ----------------------------------------------------------------------------------------------
# cores
# ----------------------------------------------------------------------------------------------
def load_cores(files=_CORE_FILES):
    """List of (v, edges) cores from the JSON files, each followed by... (reflections added later)."""
    out = []
    for f in files:
        with open(os.path.join(_DATA, f)) as fh:
            d = json.load(fh)
        for c in d["cores"]:
            out.append((int(c["n"]), tuple(sorted(tuple(e) for e in c["edges"]))))
    return out


def _reflect(v, edges):
    return tuple(sorted((v - 1 - k, v - 1 - j, v - 1 - i) for (i, j, k) in edges))


def core_family(cores):
    """Add the reflection of each core (the files are deduplicated under reflection); remove duplicates."""
    seen = set()
    res = []
    for v, e in cores:
        for ee in (tuple(sorted(e)), _reflect(v, e)):
            if (v, ee) not in seen:
                seen.add((v, ee))
                res.append((v, ee))
    return res


def _resolve_cores(cores, eager_max_v):
    """-> (eager_list, lazy_list) of (v, edges)."""
    if cores is None or cores == "none":
        return [], []
    if cores == "eager":
        eager_max_v = 10 ** 6
    elif cores == "lazy":
        eager_max_v = 0
    elif cores == "hybrid":
        pass
    else:
        cores = list(cores)  # explicit iterable of (v, edges) or dicts
        conv = []
        for c in cores:
            if isinstance(c, dict):
                conv.append((int(c["n"]), tuple(sorted(tuple(e) for e in c["edges"]))))
            else:
                conv.append((int(c[0]), tuple(sorted(tuple(e) for e in c[1]))))
        fam = core_family(conv)
        return ([c for c in fam if c[0] <= eager_max_v], [c for c in fam if c[0] > eager_max_v])
    fam = core_family(load_cores())
    return ([c for c in fam if c[0] <= eager_max_v], [c for c in fam if c[0] > eager_max_v])


def _core_images(core, n):
    """Yield the image edge tuples of `core` under all strictly increasing maps {0..v-1} -> {0..n-1}."""
    v, edges = core
    for S in itertools.combinations(range(n), v):
        yield tuple((S[a], S[b], S[c]) for (a, b, c) in edges)


def find_core_copies(edges, cores):
    """All images (as tuples of edges of `edges`) of each core inside the edge set `edges`.

    Backtracking over assignments of core edges to model edges, keeping a vertex map that is injective and
    order preserving (strictly increasing).  Full support of the cores makes the final map total.
    """
    E = sorted(edges)
    found = set()
    for (v, ce) in cores:
        ce = list(ce)
        L = len(ce)

        def rec(t, vmap, chosen):
            if t == L:
                found.add(tuple(sorted(chosen)))
                return
            for me in E:
                new = {}
                ok = True
                for a, p in zip(ce[t], me):
                    if a in vmap:
                        if vmap[a] != p:
                            ok = False
                            break
                    else:
                        new[a] = p
                if not ok:
                    continue
                vm2 = dict(vmap)
                vm2.update(new)
                # injective and strictly increasing on the assigned vertices
                items = sorted(vm2.items())
                if any(items[x][1] >= items[x + 1][1] for x in range(len(items) - 1)):
                    continue
                rec(t + 1, vm2, chosen + [me])

        rec(0, {}, [])
    return found


# ----------------------------------------------------------------------------------------------
# F7 (lazy)
# ----------------------------------------------------------------------------------------------
def find_f7_copies(edges):
    """All 5-subsets of `edges` that form a copy of F7 (as unlabeled hypergraphs, not necessarily induced)."""
    E = [tuple(e) for e in edges]
    found = set()
    pat = F7_EDGES

    def rec(t, vmap, used_pts, chosen):
        if t == len(pat):
            found.add(tuple(sorted(chosen)))
            return
        pe = pat[t]
        for me in E:
            if me in chosen:
                continue
            for perm in itertools.permutations(me):
                vm2 = dict(vmap)
                ok = True
                for a, p in zip(pe, perm):
                    if a in vm2:
                        if vm2[a] != p:
                            ok = False
                            break
                    else:
                        vm2[a] = p
                if not ok:
                    continue
                if len(set(vm2.values())) != len(vm2):
                    continue
                rec(t + 1, vm2, set(vm2.values()), chosen + [me])

    rec(0, {}, set(), [])
    return found


# ----------------------------------------------------------------------------------------------
# encoding
# ----------------------------------------------------------------------------------------------
class Encoding:
    def __init__(self, n, T, m, cores="hybrid", eager_max_v=7, forbid_f7=True, vertex1=None,
                 extra_unit=None, card_encoding=EncType.seqcounter):
        self.n, self.T, self.m = n, T, m
        self.triples = list(itertools.combinations(range(n), 3))
        self.var = {t: idx + 1 for idx, t in enumerate(self.triples)}
        self.nv = len(self.triples)
        self.forbid_f7 = forbid_f7
        cl = []
        var = self.var
        # (a) midpoint injective
        by_mid = {}
        for (i, j, k) in self.triples:
            by_mid.setdefault(j, []).append(var[(i, j, k)])
        for j, vs in by_mid.items():
            for a, b in itertools.combinations(vs, 2):
                cl.append([-a, -b])
        # (b) linear: two edges share at most one vertex => at most one edge through each pair
        by_pair = {}
        for t in self.triples:
            for pr in itertools.combinations(t, 2):
                by_pair.setdefault(pr, []).append(var[t])
        for pr, vs in by_pair.items():
            for a, b in itertools.combinations(vs, 2):
                cl.append([-a, -b])
        # (d) monotone midpoints
        for (i, j, k) in self.triples:
            for (i2, j2, k2) in self.triples:
                if i <= i2 and k <= k2 and (i, k) != (i2, k2) and not (j < j2):
                    cl.append([-var[(i, j, k)], -var[(i2, j2, k2)]])
        # (e) no medial triangle
        for a in range(n):
            for c in range(a + 2, n):
                for e in range(c + 1, n):
                    for b in range(a + 1, c):
                        for p in range(a + 1, e):
                            for q in range(c + 1, e):
                                cl.append([-var[(a, b, c)], -var[(a, p, e)], -var[(c, q, e)]])
        # alpha <= T : every (T+1)-subset contains an edge
        if T + 1 <= n:
            for S in itertools.combinations(range(n), T + 1):
                cl.append([var[t] for t in itertools.combinations(S, 3)])
        # (f) eager cores
        eager, lazy = _resolve_cores(cores, eager_max_v)
        self.lazy_cores = [c for c in lazy if c[0] <= n]
        seen = set()
        for core in eager:
            if core[0] > n:
                continue
            for img in _core_images(core, n):
                key = frozenset(img)
                if key in seen:
                    continue
                seen.add(key)
                cl.append([-var[t] for t in img])
        # case assumption on vertex 1
        if vertex1 is not None:
            if vertex1 == 0:
                for k in range(2, n):
                    cl.append([-var[(0, 1, k)]])
            else:
                if not (2 <= vertex1 < n):
                    cl.append([])  # impossible case
                else:
                    cl.append([var[(0, 1, vertex1)]])
        if extra_unit:
            for t, val in extra_unit:
                t = tuple(t)
                cl.append([var[t] if val else -var[t]])
        # exactly m edges
        self.nv_total = self.nv
        if m is not None:
            lits = list(range(1, self.nv + 1))
            if m < 0 or m > len(lits):
                cl.append([])
            elif len(lits) > 0:
                card = CardEnc.equals(lits=lits, bound=m, top_id=self.nv, encoding=card_encoding)
                cl.extend(card.clauses)
                self.nv_total = max(self.nv, card.nv)
        self.clauses = cl


def _edges_of_model(enc, model):
    pos = set(l for l in model if 0 < l <= enc.nv)
    return sorted(t for t in enc.triples if enc.var[t] in pos)


def _lazy_nogoods(enc, edges):
    ng = []
    if enc.forbid_f7:
        for cp in find_f7_copies(edges):
            ng.append(("f7", [-enc.var[t] for t in cp]))
    if enc.lazy_cores:
        for cp in find_core_copies(edges, enc.lazy_cores):
            ng.append(("core", [-enc.var[t] for t in cp]))
    return ng


class _Run:
    """Incremental solving loop shared by decide / enumerate_all."""

    def __init__(self, enc, solver, time_limit):
        self.enc = enc
        self.t0 = time.time()
        self.deadline = None if time_limit is None else self.t0 + time_limit
        self.s = Solver(name=solver, bootstrap_with=enc.clauses)
        self.solver = solver
        self.stats = dict(n=enc.n, T=enc.T, m=enc.m, nvars=enc.nv_total, nclauses=len(enc.clauses),
                          iterations=0, f7_nogoods=0, core_nogoods=0, solver=solver)
        self.stats["build_time"] = time.time() - self.t0

    def solve_once(self):
        """-> True / False / None (timeout)."""
        if self.deadline is None:
            return self.s.solve()
        rem = self.deadline - time.time()
        if rem <= 0:
            return None
        if self.solver in ("cadical153", "cadical195", "cadical103", "cadical300"):
            raise ValueError("time_limit needs an interruptible solver such as glucose4/maplechrono")
        timer = threading.Timer(rem, lambda: self.s.interrupt())
        timer.start()
        try:
            r = self.s.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
            try:
                self.s.clear_interrupt()
            except Exception:
                pass
        return r

    def next_valid_model(self):
        """Solve until a model passing all lazy checks is found. -> ('SAT', edges) | ('UNSAT', None) | ('TIMEOUT', None)."""
        enc = self.enc
        while True:
            self.stats["iterations"] += 1
            r = self.solve_once()
            if r is None:
                return "TIMEOUT", None
            if not r:
                return "UNSAT", None
            edges = _edges_of_model(enc, self.s.get_model())
            ng = _lazy_nogoods(enc, edges)
            if not ng:
                return "SAT", edges
            for kind, c in ng:
                self.s.add_clause(c)
                self.stats["f7_nogoods" if kind == "f7" else "core_nogoods"] += 1

    def finish(self, status):
        self.stats["status"] = status
        self.stats["time"] = time.time() - self.t0
        try:
            self.stats["accum_stats"] = self.s.accum_stats()
        except Exception:
            pass
        self.s.delete()
        return self.stats


def decide(n, T, m, cores="hybrid", forbid_f7=True, extra_unit=None, time_limit=None, vertex1=None,
           solver="glucose4", eager_max_v=7):
    """Is there a pattern of O' with n vertices, exactly m edges (any number if m is None), alpha <= T?"""
    enc = Encoding(n, T, m, cores=cores, eager_max_v=eager_max_v, forbid_f7=forbid_f7, vertex1=vertex1,
                   extra_unit=extra_unit)
    run = _Run(enc, solver, time_limit)
    status, edges = run.next_valid_model()
    stats = run.finish(status)
    if status == "SAT":
        return "SAT", [tuple(e) for e in edges]
    return status, stats


def enumerate_all(n, T, m, cores="hybrid", forbid_f7=True, extra_unit=None, time_limit=None, vertex1=None,
                  solver="glucose4", eager_max_v=7, return_stats=False, max_solutions=None):
    """All edge sets (sorted tuples of triples) of O' with n vertices, exactly m edges, alpha <= T.

    m must be an integer: the blocking clause (OR of the negations of the true edge variables) removes
    exactly the found solution because every solution has exactly m true edges.
    On timeout the partial list is returned (stats['status'] == 'TIMEOUT')."""
    if m is None:
        raise ValueError("enumerate_all needs a fixed m (blocking clauses are only sound for fixed m)")
    enc = Encoding(n, T, m, cores=cores, eager_max_v=eager_max_v, forbid_f7=forbid_f7, vertex1=vertex1,
                   extra_unit=extra_unit)
    run = _Run(enc, solver, time_limit)
    sols = []
    status = "UNSAT"
    while True:
        st, edges = run.next_valid_model()
        if st != "SAT":
            status = "COMPLETE" if st == "UNSAT" else "TIMEOUT"
            break
        sols.append(tuple(edges))
        if max_solutions is not None and len(sols) >= max_solutions:
            status = "TRUNCATED"
            break
        run.s.add_clause([-enc.var[t] for t in edges])
    stats = run.finish(status)
    stats["n_solutions"] = len(sols)
    return (sols, stats) if return_stats else sols
