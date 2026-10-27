"""Referee #2 (fable), L023: own re-check of the top level cell(25,23,11,4) / cell(25,23,11,3).
1. Build the inputs of both branches MYSELF from the archived component lists (topcell_cells.tar.gz; identical to the refereed lists
   or recomputed by the prover, see the review), as disjoint unions on consecutive blocks (multisets for repeated types).
2. Re-run the prover's `ext_d` (L016 ext_d_fast binary, md5-checked) in `noprune` mode: every extension by a new vertex with d edges
   (pairs disjoint, not inside an edge, endpoint degree <= d-1) and tau >= 11, WITHOUT F7 pruning and WITHOUT the (P3) test.
3. Classify every extension with OWN code (linear, F7-free, (P3) by matchings, connected, tau = 11 exactly), reduce the members of C to
   isomorphism classes with an OWN backtracking test, and compare with X_0..X_5 parsed from the certificate text."""
import os, re, sys, time, json, subprocess, math
from itertools import combinations, permutations, combinations_with_replacement, product
HERE = os.path.dirname(os.path.abspath(__file__))
LISTS = os.path.join(HERE, 'topcell_lists')
EXT_D = os.path.join(HERE, '..', 'engine', 'bin', 'ext_d')
CERT = '/home/user/Erdos-757/results/proofs/L023-f25-equals-15.md'
def verts(E): return sorted(set(v for e in E for v in e))
def degrees(E, V):
    d = {v: 0 for v in V}
    for e in E:
        for v in e: d[v] += 1
    return d
def is_linear(E):
    for e, f in combinations(E, 2):
        if len(set(e) & set(f)) >= 2: return False
    return True
def contains_F7(E):
    ES = set(frozenset(e) for e in E); at = {}
    for e in E:
        for v in e: at.setdefault(v, []).append(e)
    for v, es in at.items():
        if len(es) < 3: continue
        for e1, e2, e3 in permutations(es, 3):
            p1 = [u for u in e1 if u != v]; p2 = [u for u in e2 if u != v]; p3 = [u for u in e3 if u != v]
            for a1, a2 in (p1, p1[::-1]):
                for a3, a4 in (p2, p2[::-1]):
                    for a5, a6 in (p3, p3[::-1]):
                        if frozenset((a1, a3, a5)) in ES and frozenset((a2, a4, a6)) in ES: return True
    return False
def hall_sdr_avoiding(E, forbidden):
    match = {}
    def try_edge(i, seen):
        for v in E[i]:
            if v in forbidden or v in seen: continue
            seen.add(v)
            if v not in match or try_edge(match[v], seen): match[v] = i; return True
        return False
    for i in range(len(E)):
        if not try_edge(i, set()): return False
    return True
def P3(E, V):
    for u, w in combinations(V, 2):
        if not hall_sdr_avoiding(E, {u, w}): return False
    return True
def connected_on(E, V):
    adj = {v: set() for v in V}
    for e in E:
        for a in e:
            for b in e:
                if a != b: adj[a].add(b)
    seen = {V[0]}; st = [V[0]]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == len(V)
def has_cover(E, k):
    def rec(cov, k):
        for e in E:
            if not (cov & set(e)):
                if k == 0: return None
                for v in e:
                    r = rec(cov | {v}, k - 1)
                    if r is not None: return r
                return None
        return cov
    return rec(frozenset(), k)
def isomorphic(E1, E2):
    V1, V2 = verts(E1), verts(E2)
    if len(V1) != len(V2) or len(E1) != len(E2): return None
    d1, d2 = degrees(E1, V1), degrees(E2, V2)
    if sorted(d1.values()) != sorted(d2.values()): return None
    S2 = set(frozenset(e) for e in E2); at1 = {v: [e for e in E1 if v in e] for v in V1}
    order = []; seen = set()
    for s in sorted(V1, key=lambda v: -d1[v]):
        if s in seen: continue
        seen.add(s); q = [s]
        while q:
            x = q.pop(0); order.append(x)
            for e in at1[x]:
                for y in e:
                    if y not in seen: seen.add(y); q.append(y)
    f = {}; used = set()
    def ok(x, y):
        for e in at1[x]:
            if all(u in f or u == x for u in e):
                if frozenset(f[u] if u != x else y for u in e) not in S2: return False
        return True
    def rec(i):
        if i == len(order): return True
        x = order[i]
        for y in V2:
            if y in used or d2[y] != d1[x]: continue
            if ok(x, y):
                f[x] = y; used.add(y)
                if rec(i + 1): return True
                del f[x]; used.discard(y)
        return False
    if rec(0):
        assert set(frozenset(f[u] for u in e) for e in E1) == S2
        return dict(f)
    return None
def invariant(E):
    V = verts(E); d = degrees(E, V)
    return (tuple(sorted(d.values())), tuple(sorted(tuple(sorted(d[v] for v in e)) for e in E)))
def load_list(key):
    p = None
    for root, _, files in os.walk(LISTS):
        for fn in files:
            if fn == 'cell_%d_%d_%d_D%d.txt' % key: p = os.path.join(root, fn)
    assert p, key
    reps = []
    for l in open(p):
        if l.startswith('FOUND:'): reps.append([tuple(map(int, g)) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', l)])
    return reps
def build_inputs(decs, d):
    """decs: list of multisets of types (n,m,t); components from cell(n,m,t,d).  Returns ext_d input lines."""
    lines = []
    for dec in decs:
        groups = {}
        for c in dec: groups[c] = groups.get(c, 0) + 1
        gl = []
        for typ, k in sorted(groups.items()):
            cls = load_list((typ[0], typ[1], typ[2], d)) if typ != (1, 0, 0) else [[]]
            gl.append((typ, cls, list(combinations_with_replacement(range(len(cls)), k))))
        for combo in product(*[g[2] for g in gl]):
            es = []; off = 0
            for (typ, cls, _), idxs in zip(gl, combo):
                for i in idxs:
                    es += [tuple(v + off for v in e) for e in cls[i]]; off += typ[0]
            assert off == 24
            lines.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
    return lines
def main():
    txt = open(CERT).read(); X = []
    for line in txt.splitlines():
        m = re.match(r'^X_(\d) FOUND: (.*)$', line.strip())
        if m: X.append([tuple(map(int, g)) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', m.group(2))])
    assert len(X) == 6
    branches = {3: ([((24, 20, 10),), ((12, 10, 5), (12, 10, 5)), ((10, 8, 4), (14, 12, 6)), ((3, 1, 1), (21, 19, 9))], 15429, 2928),
                4: ([((24, 19, 10),), ((10, 7, 4), (14, 12, 6)), ((3, 1, 1), (21, 18, 9))], 67, 15032)}
    for d, (decs, n_expected, hits_expected) in sorted(branches.items(), reverse=True):
        lines = build_inputs(decs, d)
        print('branch d=%d: %d inputs built (expected %d)' % (d, len(lines), n_expected), flush=True)
        # sanity on inputs: 24 vertices, 23-d edges, linear
        for l in lines[:50] + lines[-50:]:
            nums = list(map(int, l.split())); m = nums[0]; es = [tuple(nums[1 + 3 * i:4 + 3 * i]) for i in range(m)]
            assert m == 23 - d and is_linear(es) and max(max(e) for e in es) <= 23
        fin = os.path.join(HERE, 'own_in_d%d.txt' % d); open(fin, 'w').write('\n'.join(lines) + '\n')
        t0 = time.time()
        res = subprocess.run('%s 24 10 11 %d %d noprune < %s' % (EXT_D, d, d - 1, fin), shell=True, capture_output=True, text=True, timeout=3000)
        assert res.returncode == 0, res.stderr[:500]
        out = res.stdout.splitlines()
        summ = [l for l in out if l.startswith('SUMMARY')]; hits = [l for l in out if l.startswith('HIT:')]
        print('   ext_d noprune: %s (%.0fs); hits %d (expected %d)' % (summ[-1] if summ else 'NO SUMMARY', time.time() - t0, len(hits), hits_expected), flush=True)
        cat = {'not25': 0, 'nonlinear': 0, 'F7': 0, 'P3_violated': 0, 'disconnected': 0, 'tau_not_11': 0, 'in_C': 0}
        members = []
        for h in hits:
            E = [tuple(map(int, g)) for g in re.findall(r'\((\d+),(\d+),(\d+)\)', h)]
            V = verts(E)
            if V != list(range(25)) or len(E) != 23: cat['not25'] += 1; continue
            if not is_linear(E): cat['nonlinear'] += 1; continue
            if contains_F7(E): cat['F7'] += 1; continue
            if not P3(E, V): cat['P3_violated'] += 1; continue
            if not connected_on(E, V): cat['disconnected'] += 1; continue
            if has_cover(E, 10) is not None or has_cover(E, 11) is None: cat['tau_not_11'] += 1; continue
            cat['in_C'] += 1; members.append(E)
        print('   own classification: %s' % cat, flush=True)
        # isomorphism reduction of the members (own)
        classes = []
        for E in members:
            inv = invariant(E)
            for c in classes:
                if c[0] == inv and isomorphic(E, c[1]) is not None: c[2] += 1; break
            else: classes.append([inv, E, 1])
        print('   members of C: %d, isomorphism classes: %d, sizes %s' % (len(members), len(classes), [c[2] for c in classes]), flush=True)
        if d == 4:
            match = []
            for c in classes:
                j = next((j for j in range(6) if isomorphic(c[1], X[j]) is not None), None); match.append(j)
            print('   each class isomorphic to X_j: %s; every X_j hit: %s' % (match, sorted(m for m in match if m is not None) == list(range(6))), flush=True)
            for j in range(6):
                assert any(isomorphic(X[j], c[1]) is not None for c in classes), 'X_%d NOT FOUND' % j
            print('   RESULT d=4: the members of C are exactly the six classes X_0..X_5: %s' % (len(classes) == 6 and sorted(match) == list(range(6))))
        else:
            print('   RESULT d=3: members of C with Delta<=3: %d (certificate: 0)' % len(members))
if __name__ == '__main__':
    main()
