"""Referee L014 r1: classify 3-graphs (lines 'X <inp> <m> a b c ...' from myext, or 'FOUND: (a,b,c) ...') with explicit
witnesses, own code: (P1) linearity; (P2) an explicit F7 copy (5 edges, verified against the pattern 012,034,056,135,246);
(P3) an explicit set S with e(S) >= |S|-1 found by a Hall-deficiency (alternating-path) argument for each vertex pair {u,v},
re-verified by counting; connectivity on all NV vertices; max degree. Every witness is re-verified independently of how it was found.
Usage: python3 classify.py NV FILE [members_out]"""
import sys, re, itertools
from collections import Counter
NV = int(sys.argv[1]); FN = sys.argv[2]; MOUT = sys.argv[3] if len(sys.argv) > 3 else None
def parse(l):
    if l.startswith('X '):
        a = list(map(int, l.split()[1:])); m = a[1]; v = a[2:]; assert len(v) == 3 * m
        return [tuple(sorted(v[3*i:3*i+3])) for i in range(m)]
    if l.startswith('FOUND') or l.startswith('HIT') or l.startswith('SURVIVOR'):
        return [tuple(sorted(map(int, g))) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', l)]
    return None
def linear_viol(E):
    for e, f in itertools.combinations(E, 2):
        if len(set(e) & set(f)) >= 2: return (e, f)
    return None
def f7_copy(E):
    """search a copy of F7 = {x a1 b1, x a2 b2, x a3 b3, a1 a2 a3, b1 b2 b3} (up to swapping within pairs)."""
    S = set(E); inc = {}
    for e in E:
        for v in e: inc.setdefault(v, []).append(e)
    for x, es in inc.items():
        if len(es) < 3: continue
        for tri in itertools.combinations(es, 3):
            prs = [tuple(v for v in e if v != x) for e in tri]
            for c in itertools.product(*[(0, 1)] * 3):
                e1 = tuple(sorted(prs[i][c[i]] for i in range(3))); e2 = tuple(sorted(prs[i][1 - c[i]] for i in range(3)))
                if e1 in S and e2 in S: return list(tri) + [e1, e2]
    return None
def check_f7(c):
    """independent verification that 5 edges form F7: 7 distinct vertices, some labelling maps 012,034,056,135,246 onto them."""
    vs = sorted(set(v for e in c for v in e))
    if len(vs) != 7: return False
    F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
    target = set(tuple(sorted(e)) for e in c)
    for p in itertools.permutations(vs):
        if set(tuple(sorted(p[i] for i in e)) for e in F7) == target: return True
    return False
def p3_witness(E, nv):
    """for each pair {u,v}: max matching of edges into vertices outside {u,v} (each edge to one of its own vertices);
    if not all edges are matched, the edges reachable by alternating paths from an unmatched edge form F with
    |V(F) minus {u,v}| < |F|, so S = V(F) has e(S) >= |F| >= |S|-1.  Returns such an S (verified) or None."""
    m = len(E)
    verts = sorted(set(v for e in E for v in e))
    for u, v in itertools.combinations(range(nv), 2):
        match_v = {}; match_e = [None] * m
        def aug(i, seen):
            for x in E[i]:
                if x == u or x == v or x in seen: continue
                seen.add(x)
                if x not in match_v or aug(match_v[x], seen):
                    match_v[x] = i; match_e[i] = x; return True
            return False
        for i in range(m):
            if not aug(i, set()):
                # alternating-path closure from edge i
                F = {i}; stack = [i]; R = set()
                while stack:
                    j = stack.pop()
                    for x in E[j]:
                        if x == u or x == v or x in R: continue
                        R.add(x); k = match_v.get(x)
                        if k is not None and k not in F: F.add(k); stack.append(k)
                S = set(x for j in F for x in E[j])
                eS = sum(1 for e in E if set(e) <= S)
                assert eS >= len(S) - 1, ('witness failed', S, eS)
                return sorted(S)
    return None
def components(E, nv):
    par = list(range(nv))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in E:
        for y in e[1:]: par[f(y)] = f(e[0])
    return len(set(f(x) for x in range(nv)))
cnt = Counter(); members = []; nl = 0
for l in open(FN):
    E = parse(l)
    if E is None: continue
    nl += 1
    assert len(set(E)) == len(E) and all(len(set(e)) == 3 and max(e) < NV for e in E)
    lv = linear_viol(E)
    if lv: cnt['nonlinear'] += 1; continue
    c = f7_copy(E)
    hasF7 = c is not None
    if hasF7: assert check_f7(c) and all(e in set(E) for e in c); cnt['F7'] += 1
    S = p3_witness(E, NV)
    if S is not None:
        cnt['P3_violated'] += 1
        if not hasF7: cnt['F7free_P3_violated'] += 1
    conn = components(E, NV) == 1
    cnt['connected' if conn else 'disconnected'] += 1
    deg = Counter(v for e in E for v in e); cnt['maxdeg_%d' % max(deg.values())] += 1
    if not hasF7 and S is None:
        cnt['in_C'] += 1
        if conn: cnt['connected_in_C'] += 1; members.append(l)
print('FILE', FN, 'lines', nl, dict(sorted(cnt.items())))
if MOUT:
    open(MOUT, 'w').writelines(members)
