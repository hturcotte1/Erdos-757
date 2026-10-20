"""Referee library (round 2, claim C003): own implementations, no project imports.

All constraints are generated from the DEFINITION of a Sidon set (all positive differences
distinct): for every two distinct 2-subsets {a,b},{c,d} with b-a = d-c, the union cannot lie in
a Sidon subset.  Nothing assumes the 3-AP reduction.
"""
import itertools
import json
from fractions import Fraction

CLAIM = "/home/user/Erdos-757/results/claims/C003-reader-5-9-K6.json"


def load_claim_set():
    raw = json.load(open(CLAIM))
    A = sorted(raw["set"])
    assert all(type(x) is int for x in A) and len(set(A)) == len(A)
    return A, raw


def is_sidon(S):
    S = sorted(S)
    d = [y - x for x, y in itertools.combinations(S, 2)]
    return len(d) == len(set(d))


def conflicts_from_definition(A):
    """Minimal forbidden vertex sets (as sorted tuples of indices into sorted A)."""
    n = len(A)
    bydiff = {}
    for i in range(n):
        for j in range(i + 1, n):
            bydiff.setdefault(A[j] - A[i], []).append((i, j))
    conf = set()
    for prs in bydiff.values():
        if len(prs) > 1:
            for p, q in itertools.combinations(prs, 2):
                conf.add(tuple(sorted(set(p) | set(q))))
    # remove non-minimal ones (a superset of another forbidden set is redundant)
    conf = sorted(conf, key=len)
    minimal = []
    for c in conf:
        cs = set(c)
        if not any(set(m) <= cs for m in minimal):
            minimal.append(c)
    return minimal


def frontier_dp(nv, conflicts, order, max_states=None):
    """Exact maximum of |T| over T avoiding every conflict, by a path DP along `order`.
    Returns (best, witness_bitmask, max_number_of_states).  Exact for ANY order."""
    pos = {v: i for i, v in enumerate(order)}
    last = [max(pos[v] for v in c) for c in conflicts]
    by_last = [[] for _ in range(nv)]
    for ci, c in enumerate(conflicts):
        by_last[last[ci]].append(c)
    deadline = {v: -1 for v in order}
    for ci, c in enumerate(conflicts):
        for v in c:
            deadline[v] = max(deadline[v], last[ci])
    states = {frozenset(): (0, 0)}   # active chosen set -> (count, chosen bitmask)
    peak = 1
    for i, v in enumerate(order):
        new = {}
        for st, (cnt, mask) in states.items():
            ok = True
            for c in by_last[i]:
                if all((u == v) or (u in st) for u in c):
                    ok = False
                    break
            for take in (0, 1):
                if take and not ok:
                    continue
                s2 = set(st)
                if take:
                    s2.add(v)
                s2 = frozenset(u for u in s2 if deadline[u] > i)
                c2 = cnt + take
                m2 = mask | (1 << v) if take else mask
                if s2 not in new or new[s2][0] < c2:
                    new[s2] = (c2, m2)
        states = new
        peak = max(peak, len(states))
        if max_states is not None and peak > max_states:
            return None, None, peak
    best, mask = max(states.values())
    return best, mask, peak


def sat_atleast(nv, conflicts, k, solver_name="cadical195", enc="totalizer"):
    """Is there a conflict-free subset of size >= k?  Returns (sat, model_subset or None)."""
    from pysat.card import CardEnc, EncType
    from pysat.formula import CNF
    from pysat.solvers import Solver
    if k > nv:
        return False, None          # no subset larger than the ground set
    if k <= 0:
        return True, []
    cnf = CNF()
    for c in conflicts:
        cnf.append([-(v + 1) for v in c])
    encmap = {"totalizer": EncType.totalizer, "seqcounter": EncType.seqcounter,
              "sortnetwrk": EncType.sortnetwrk, "cardnetwrk": EncType.cardnetwrk,
              "kmtotalizer": EncType.kmtotalizer, "mtotalizer": EncType.mtotalizer}
    card = CardEnc.atleast(lits=list(range(1, nv + 1)), bound=k, top_id=nv, encoding=encmap[enc])
    cnf.extend(card.clauses)
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as s:
        if s.solve():
            model = s.get_model()
            chosen = [v for v in range(nv) if model[v] > 0]
            return True, chosen
        return False, None


def brute_force_h(A):
    """h(A) straight from the definition: the largest s such that some s-subset is Sidon
    (Sidon is hereditary, so it suffices to find the largest s with a Sidon s-subset)."""
    n = len(A)
    for s in range(n, 0, -1):
        for T in itertools.combinations(A, s):
            if is_sidon(T):
                return s, T
    return 0, ()


def rebuild_family(K):
    """S_K from the stated definition, as integers scaled by 269^K, with minimal levels."""
    O = [0, 49, 75, 83, 98, 101, 117, 119, 121, 159, 269]

    def phi(x):
        return Fraction(101) + Fraction(18, 269) * x
    S = {}
    anchors = set()
    for j in range(K + 1):
        for x in O:
            p = Fraction(x)
            for _ in range(j):
                p = phi(p)
            S.setdefault(p, j)
            if x in (101, 119):
                anchors.add((p, j))   # phi^j(101)=phi^{j+1}(0), phi^j(119)=phi^{j+1}(269)
    pts = sorted(S)
    scale = 269 ** K
    ints = [p * scale for p in pts]
    assert all(v.denominator == 1 for v in ints)
    ints = [int(v) for v in ints]
    levels = [S[p] for p in pts]
    # copy order: by minimal level, the two points shared with the next copy last within a level
    is_anchor = [(p, S[p]) in anchors for p in pts]
    return ints, levels, is_anchor
