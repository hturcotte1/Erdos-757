"""Spot check of the input KT^{L*} (L021; L024 relies on L021 Theorem 7(ii): KT for n <= 24, so a minimal counterexample
has n >= 25) on the AP hypergraphs of the stored record sets, all their induced subsets, and the Fibonacci set
{F_3..F_15}: P = A + DEF >= 0, DEF computed exactly over L*-families (own code), and A > 0 for the full sets.
Also: none of these hypergraphs is a minimal-counterexample candidate (A >= 0 on every connected induced subgraph with
a degree-3 vertex would already be enough); we just report min P."""
import json, sys
from itertools import combinations
import pattern_a_ref as R
from rlib import degs, min_transversals, isomorphic, connected

D = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
bases = {k: sorted(v['set']) for k, v in D.items()}
fib = [2, 3]
while len(fib) < 13:
    fib.append(fib[-1] + fib[-2])
bases['fib13'] = fib
PIECES = [(nm, n, E, R.W[nm]) for nm, (n, E) in R.P.items()]
bysize = {}
for nm, n, E, w in PIECES:
    bysize.setdefault((n, len(E)), []).append((nm, n, E, w))


def ap_edges(S):
    S = sorted(S)
    idx = {x: i for i, x in enumerate(S)}
    E = []
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            c = 2 * S[j] - S[i]
            if c in idx and idx[c] > j:
                E.append((i, j, idx[c]))
    return E


def induced(E, Vs):
    Vs = set(Vs)
    return [e for e in E if set(e) <= Vs]


def DEF(n, E):
    """exact max over L*-families of sum W - 35 |E*| (own branch over induced copies)."""
    copies = []  # (vertex mask, W)
    for (pn, pm), lst in bysize.items():
        if pn > n:
            continue
        for Vs in combinations(range(n), pn):
            Ei = induced(E, Vs)
            if len(Ei) != pm:
                continue
            loc = {x: i for i, x in enumerate(Vs)}
            Eloc = [tuple(sorted(loc[x] for x in e)) for e in Ei]
            for nm, n2, E2, w in lst:
                if isomorphic(pn, Eloc, n2, E2):
                    copies.append((sum(1 << x for x in Vs), w))
                    break
    em = [sum(1 << x for x in e) for e in E]
    best = 0

    def val(mask_list):
        Vm = 0
        for m in mask_list:
            Vm |= m
        estar = 0
        for e in em:
            if e & Vm and not any((e & m) == e for m in mask_list):
                estar += 1
        return estar

    # brute force over disjoint subfamilies (copies are few for these small graphs)
    def rec(i, chosen, used, wsum):
        nonlocal best
        if chosen:
            v = wsum - 35 * val(chosen)
            if v > best:
                best = v
        for j in range(i, len(copies)):
            m, w = copies[j]
            if m & used:
                continue
            rec(j + 1, chosen + [m], used | m, wsum + w)

    rec(0, [], 0, 0)
    return best, len(copies)


report = {}
for name, S in bases.items():
    n0 = len(S)
    Eall = ap_edges(S)
    t0, _ = min_transversals(n0, Eall)
    A0 = 27 * n0 + 35 * len(Eall) - 132 * t0
    minP = None; negA = 0; checked = 0; d4 = 0
    for k in range(1, n0 + 1):
        for Vs in combinations(range(n0), k):
            Ei = induced(Eall, Vs)
            loc = {x: i for i, x in enumerate(Vs)}
            El = [tuple(sorted(loc[x] for x in e)) for e in Ei]
            if El and max(degs(k, El)) > 3:
                d4 += 1
                continue  # KT^{L*} is a statement about C_3 only
            t, _ = min_transversals(k, El)
            A = 27 * k + 35 * len(El) - 132 * t
            checked += 1
            if A < 0:
                negA += 1
                d, nc = DEF(k, El)
                P = A + d
            else:
                P = A  # DEF >= 0
            if minP is None or P < minP:
                minP = P
    report[name] = dict(n=n0, m=len(Eall), tau=t0, A=A0, subsets_in_C3=checked, skipped_Delta4=d4, subsets_with_A_neg=negA, min_P_lower=minP)
    print(name, report[name], flush=True)
print('ALL min P >= 0:', all(r['min_P_lower'] >= 0 for r in report.values()))
