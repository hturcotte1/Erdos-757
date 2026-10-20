"""Referee: build the route-4 / route-20 inputs G = disjoint union of one representative per component type (all products), from
the prover's cell lists, after re-checking every representative independently (connected, linear, F7-free, P3, exact tau, degrees)."""
import sys, re, itertools, os
CD = '/home/user/Erdos-757/experiments/prover/L012/out/cells'
def load(n, m, t, D):
    fn = os.path.join(CD, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))
    L = [l for l in open(fn)]
    assert L[-1].startswith('INFO'), fn
    return [[tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)] for l in L if l.startswith('FOUND')]
def tau(E, n):
    def rec(k, S, i):
        while i < len(E) and (E[i][0] in S or E[i][1] in S or E[i][2] in S): i += 1
        if i == len(E): return True
        if k == 0: return False
        return any(rec(k - 1, S | {v}, i + 1) for v in E[i])
    k = 0
    while not rec(k, frozenset(), 0): k += 1
    return k
def connected(E, n):
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a, b, c in E: par[f(a)] = f(b); par[f(b)] = f(c)
    return len({f(v) for v in range(n)}) == 1
def linear(E): return all(len(set(e) & set(g)) <= 1 for e, g in itertools.combinations(E, 2))
def has_f7(E):
    at = {}
    for e in E:
        for v in e: at.setdefault(v, []).append(e)
    Es = {frozenset(e) for e in E}
    for p, L in at.items():
        for e1, e2, e3 in itertools.combinations(L, 3):
            a1, b1 = [v for v in e1 if v != p]; r2 = [v for v in e2 if v != p]; r3 = [v for v in e3 if v != p]
            for x2, y2 in (r2, r2[::-1]):
                for x3, y3 in (r3, r3[::-1]):
                    if frozenset((a1, x2, x3)) in Es and frozenset((b1, y2, y3)) in Es: return True
    return False
def p3(E, n):
    # e(S) <= |S|-2 for all |S|>=2  <=>  for all pairs {x,y}: a matching of the edges into V\{x,y} (each edge -> own vertex)
    for x, y in itertools.combinations(range(n), 2):
        own = {}
        def aug(e, seen):
            for v in E[e]:
                if v in (x, y) or v in seen: continue
                seen.add(v)
                if v not in own or aug(own[v], seen): own[v] = e; return True
            return False
        for e in range(len(E)):
            if not aug(e, set()): return False
    return True
def check(E, n, m, t, D):
    deg = [0] * n
    for e in E:
        for v in e: deg[v] += 1
    return (len(E) == m and all(0 <= v < n for e in E for v in e) and connected(E, n) and linear(E) and not has_f7(E)
            and max(deg) <= D and tau(E, n) == t and p3(E, n))
if __name__ == '__main__':
    route = sys.argv[1]
    D = {'4': 4, '20': 3}[route]
    decs = [[(22, 17, 9)], [(3, 1, 1), (19, 16, 8)], [(10, 7, 4), (12, 10, 5)], [(8, 5, 3), (14, 12, 6)]]
    inputs = []
    for dec in decs:
        lists = []
        for typ in dec:
            L = load(*typ, D)
            bad = [i for i, E in enumerate(L) if not check(E, *typ, D)]
            print('type', typ, 'D', D, 'representatives', len(L), 'failing my checks:', len(bad), file=sys.stderr)
            lists.append((typ, L))
        for combo in itertools.product(*[L for _, L in lists]):
            es = []; off = 0
            for (typ, _), E in zip(lists, combo):
                es += [tuple(v + off for v in e) for e in E]; off += typ[0]
            assert off == 22 and len(es) == 17
            inputs.append('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es))
    print('inputs', len(inputs), file=sys.stderr)
    print('\n'.join(inputs))
