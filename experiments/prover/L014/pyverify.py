"""(L014) Pure-Python verifier, written from scratch for this certificate (shares no code with filt.c / ext_d.c).
Edges are triples of vertex labels.  Tests: linear; F7 (structural: a centre c, three edges {c,a_i,b_i} at c, and two further edges
{a_1,x_2,x_3}, {b_1,y_2,y_3} with {x_i,y_i} = {a_i,b_i}); (P3) e(S) <= |S|-2 for all |S| >= 2, in the Hall form (for every pair {x,y}
of vertices the edges have distinct representatives avoiding x and y; BFS augmenting paths); exact tau (branching on the first
uncovered edge); connectivity on a given vertex set; maximum degree."""
from collections import deque
from itertools import combinations
def linear(E):
    S = [frozenset(e) for e in E]
    return all(len(a & b) <= 1 for a, b in combinations(S, 2)) and all(len(a) == 3 for a in S) and len(set(S)) == len(S)
def has_f7(E):
    S = set(frozenset(e) for e in E); at = {}
    for e in E:
        for v in e: at.setdefault(v, []).append(e)
    for c, es in at.items():
        if len(es) < 3: continue
        for e1, e2, e3 in combinations(es, 3):
            p = [tuple(v for v in e if v != c) for e in (e1, e2, e3)]
            a1, b1 = p[0]
            for x2, y2 in (p[1], p[1][::-1]):
                for x3, y3 in (p[2], p[2][::-1]):
                    if frozenset((a1, x2, x3)) in S and frozenset((b1, y2, y3)) in S: return True
    return False
def _sdr_avoiding(E, x, y):
    owner = {}; match = {}
    for i in range(len(E)):
        # BFS for an augmenting path from edge i
        prev = {}; q = deque([i]); seen_v = set(); found = None
        while q and found is None:
            f = q.popleft()
            for v in E[f]:
                if v == x or v == y or v in seen_v: continue
                seen_v.add(v); prev[v] = f
                if v not in owner: found = v; break
                q.append(owner[v])
        if found is None: return False
        v = found
        while True:
            f = prev[v]; old = match.get(f); owner[v] = f; match[f] = v
            if f == i: break
            v = old
    return True
def p3(E, V=None):
    if V is None: V = sorted(set(v for e in E for v in e))
    V = sorted(set(V) | set(v for e in E for v in e))
    E = [tuple(e) for e in E]
    for x, y in combinations(V, 2):
        if not _sdr_avoiding(E, x, y): return False
    return True
def cover_le(E, k):
    """True iff some set of at most k vertices meets every edge."""
    def rec(rem, k):
        if not rem: return True
        if k == 0: return False
        e = rem[0]
        for v in e:
            if rec([f for f in rem if v not in f], k - 1): return True
        return False
    return rec([tuple(e) for e in E], k)
def tau(E):
    k = 0
    while not cover_le(E, k): k += 1
    return k
def all_covers_exact(E, k):
    """all vertex sets of size exactly k meeting every edge, PROVIDED tau(E) = k (then every k-cover is inclusion-minimal and is
    reached by branching on the first uncovered edge)."""
    out = set()
    def rec(rem, chosen):
        if not rem:
            if len(chosen) == k: out.add(frozenset(chosen))
            return
        if len(chosen) == k: return
        for v in rem[0]:
            rec([f for f in rem if v not in f], chosen | {v})
    rec([tuple(e) for e in E], frozenset())
    return out
def connected(E, V):
    V = set(V); adj = {v: set() for v in V}
    for e in E:
        for v in e:
            if v not in adj: return False
            adj[v] |= set(e) - {v}
    start = next(iter(V)); seen = {start}; q = [start]
    while q:
        v = q.pop()
        for u in adj[v]:
            if u not in seen: seen.add(u); q.append(u)
    return seen == V
def maxdeg(E):
    d = {}
    for e in E:
        for v in e: d[v] = d.get(v, 0) + 1
    return max(d.values()) if d else 0
def in_C(E):
    return linear(E) and not has_f7(E) and p3(E)
if __name__ == '__main__':
    F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
    fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    grid = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8)]
    abase = [(0,1,2)]
    print('F7: linear', linear(F7), 'has_f7', has_f7(F7), 'p3', p3(F7), 'tau', tau(F7))
    print('relabelled F7 + pendant edge: has_f7', has_f7([(6,5,4),(6,3,2),(6,1,0),(5,3,1),(4,2,0),(0,7,8)]))
    print('Fano: has_f7', has_f7(fano), 'p3', p3(fano))
    print('3x3 grid: in_C', in_C(grid), 'tau', tau(grid), 'connected', connected(grid, range(9)))
    print('two disjoint edges connected:', connected([(0,1,2),(3,4,5)], range(6)), 'nonlinear:', linear([(0,1,2),(0,1,3)]))
    AG = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(1,5,6),(2,3,7)]   # AG(2,3) minus one parallel class
    print('AG(2,3) minus a parallel class: p3', p3(AG), 'has_f7', has_f7(AG))
