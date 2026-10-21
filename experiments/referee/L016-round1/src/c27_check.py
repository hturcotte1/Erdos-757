#!/usr/bin/env python3
"""Referee L016 round 1 (own code): exact checks of the witness C27 = A_base u (10^9 + 7919 * (A_base minus {1056})).
(1) distinct integers; (2) every 4-subset has >= 5 distinct absolute differences (all C(27,4)); (3) the largest Sidon subset
(all sums x+y, x<=y, distinct) by CP-SAT over ALL additive conflicts a+b=c+d ({a,b} != {c,d}, repetitions allowed), and
independently by an exhaustive branch and bound over the same conflicts; (4) an explicit Sidon subset of size h, checked
directly; (5) the same for A_base and B13; (6) the 3-AP hypergraph: count, and whether an AP uses both parts."""
import itertools, sys
from collections import defaultdict
from fractions import Fraction

ABASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
B13 = [x for x in ABASE if x != 1056]
C27 = sorted(ABASE + [10**9 + 7919 * x for x in B13])
STATED = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056,1000000000,1001076984,1001583800,1001924317,1001948074,
          1001971831,1002153968,1002264834,1002359862,1002557837,1003167600,1004181232,1004719724]

def is45(A):
    for Q in itertools.combinations(A, 4):
        if len({abs(x - y) for x, y in itertools.combinations(Q, 2)}) < 5:
            return False
    return True

def conflicts(A):
    """all minimal Sidon violations as index sets: pairs {i<=j},{k<=l} with equal sums and different pairs."""
    n = len(A); bysum = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            bysum[A[i] + A[j]].append((i, j))
    conf = set()
    for s, lst in bysum.items():
        for p, q in itertools.combinations(lst, 2):
            conf.add(frozenset(p) | frozenset(q))
    return [sorted(c) for c in conf]

def is_sidon(S):
    sums = [x + y for x, y in itertools.combinations_with_replacement(sorted(S), 2)]
    return len(sums) == len(set(sums))

def h_cpsat(A, conf):
    from ortools.sat.python import cp_model
    md = cp_model.CpModel(); x = [md.NewBoolVar('x%d' % i) for i in range(len(A))]
    for c in conf:
        md.Add(sum(x[i] for i in c) <= len(c) - 1)
    md.Maximize(sum(x))
    sv = cp_model.CpSolver(); sv.parameters.num_workers = 1; sv.parameters.max_time_in_seconds = 120
    st = sv.Solve(md)
    assert st == cp_model.OPTIMAL, st
    return int(round(sv.ObjectiveValue())), [A[i] for i in range(len(A)) if sv.Value(x[i])]

def h_bb(A, conf):
    n = len(A); byv = defaultdict(list)
    for c in conf:
        byv[max(c)].append(c)        # check a conflict when its largest index is decided
    best = [0, None]
    chosen = []
    def rec(i, cnt):
        if cnt + (n - i) <= best[0]:
            return
        if i == n:
            best[0] = cnt; best[1] = list(chosen); return
        # take i
        chosen.append(i); s = set(chosen)
        if all(not all(v in s for v in c) for c in byv[i]):
            rec(i + 1, cnt + 1)
        chosen.pop()
        rec(i + 1, cnt)
    rec(0, 0)
    return best[0], [A[i] for i in best[1]]

def aps(A):
    S = set(A); res = []
    for a, c in itertools.combinations(sorted(A), 2):
        if (a + c) % 2 == 0 and (a + c) // 2 in S:
            res.append((a, (a + c) // 2, c))
    return res

for name, A in (('A_base', ABASE), ('B13', B13), ('C27', C27)):
    assert len(set(A)) == len(A)
    conf = conflicts(A)
    four = sum(1 for c in conf if len(c) == 4)
    h1, S1 = h_cpsat(A, conf)
    h2, S2 = h_bb(A, conf)
    assert is_sidon(S1) and is_sidon(S2) and len(S1) == h1 and len(S2) == h2
    print('%s: n=%d distinct=%s (4,5)=%s conflicts=%d (4-element %d, 3-AP %d) h_cpsat=%d h_bb=%d ratio=%s <4/7? %s' % (
        name, len(A), len(set(A)) == len(A), is45(A), len(conf), four, len(conf) - four, h1, h2, Fraction(h1, len(A)),
        Fraction(h1, len(A)) < Fraction(4, 7)))
    if name == 'C27':
        print('  C27 equals the stated list:', C27 == STATED)
        ap = aps(A); cross = [t for t in ap if not (all(x < 10**9 for x in t) or all(x >= 10**9 for x in t))]
        print('  3-APs: %d, crossing both parts: %d' % (len(ap), len(cross)))
        print('  a maximum Sidon subset (CP-SAT):', sorted(S1))
