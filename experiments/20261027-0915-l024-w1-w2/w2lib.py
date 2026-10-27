"""Shared helpers for W2: components of P - x, isomorphisms of induced sub-hypergraphs, structure checks, P computation."""
import sys, itertools, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L024')
from hyp24 import *

def comps_minus(n, edges, x):
    """connected components (frozensets of vertices, isolated vertices included) of the hypergraph P - x
    (delete vertex x and every edge containing x)."""
    par = list(range(n))
    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for e in edges:
        if x in e: continue
        for y in e[1:]: par[f(y)] = f(e[0])
    cs = {}
    for a in range(n):
        if a == x: continue
        cs.setdefault(f(a), set()).add(a)
    return sorted((frozenset(c) for c in cs.values()), key=lambda c: min(c))

def comps_of(n, edges, removed):
    """components of H - removed (set of vertices), as frozensets."""
    par = list(range(n))
    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for e in edges:
        if any(y in removed for y in e): continue
        for y in e[1:]: par[f(y)] = f(e[0])
    cs = {}
    for a in range(n):
        if a in removed: continue
        cs.setdefault(f(a), set()).add(a)
    return [frozenset(c) for c in cs.values()]

def inner_edges(edges, S):
    return [e for e in edges if all(x in S for x in e)]

def isos(edgesA, SA, edgesB, SB):
    """all bijections phi: SA -> SB (dicts) with phi(E(A)[SA]) = E(B)[SB]."""
    SA = sorted(SA)
    EA = inner_edges(edgesA, set(SA)); EB = inner_edges(edgesB, set(SB))
    if len(SA) != len(SB) or len(EA) != len(EB): return
    eB = set(tuple(sorted(e)) for e in EB)
    dA = {x: 0 for x in SA}; dB = {x: 0 for x in SB}
    for e in EA:
        for x in e: dA[x] += 1
    for e in EB:
        for x in e: dB[x] += 1
    if sorted(dA.values()) != sorted(dB.values()): return
    adjA = {x: set() for x in SA}
    for e in EA:
        for x in e:
            for y in e:
                if x != y: adjA[x].add(y)
    # order: BFS-ish, highest degree first
    order = []; seen = set()
    for s in sorted(SA, key=lambda x: -dA[x]):
        if s in seen: continue
        stack = [s]; seen.add(s)
        while stack:
            u = stack.pop(0); order.append(u)
            for y in sorted(adjA[u]):
                if y not in seen: seen.add(y); stack.append(y)
    pos = {x: i for i, x in enumerate(order)}
    check_at = [[] for _ in order]
    for e in EA:
        last = max(e, key=lambda x: pos[x]); check_at[pos[last]].append(e)
    phi = {}; used = set()
    def rec(i):
        if i == len(order):
            yield dict(phi); return
        x = order[i]
        for u in SB:
            if u in used or dB[u] != dA[x]: continue
            phi[x] = u; used.add(u)
            if all(tuple(sorted(phi[y] for y in e)) in eB for e in check_at[i]):
                yield from rec(i + 1)
            del phi[x]; used.discard(u)
    yield from rec(0)

def connected_all(n, edges):
    return len(comps_of(n, edges, set())) == 1

def evaluate(n, E, pieces, stats, tag, rec, bf=False):
    """in C_3? tau, A, DEF, P.  Updates stats; returns P or None."""
    if not in_C3(n, E):
        return None
    stats['inC3'] += 1
    t = tau(n, E)
    A = CN * n + CM * len(E) - CT * t
    rec.update(n=n, m=len(E), tau=t, A=A)
    if A >= 0:
        stats['A_nonneg'] += 1
        return A
    stats['A_neg'] += 1
    D, fam, ncop = def_certificate(n, E, pieces, -A)
    if fam: assert family_def(n, E, [(S, w) for (S, w, nm) in fam]) == D
    rec.update(DEF=D, P=A + D, family=[(nm, [x for x in range(n) if S >> x & 1]) for (S, w, nm) in fam])
    if A + D < 0: stats['Pneg'] += 1
    return A + D
