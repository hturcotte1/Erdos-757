# Referee check of L022 Theorem 2 (i)-(vii) on linear vertex-critical violators.
# tau of every induced subgraph by the exact subset recursion
#   tau(S) = 0 if no edge inside S, else 1 + min_{x in e} tau(S - x)  (e any edge inside S),
# then: vertex-critical iff s(V) < 0 and s(S) >= 0 for every proper S.
# Co-transversality of X in an induced subgraph F: tau(F - X) == tau(F) - |X|.
import random, sys, json, time
from itertools import combinations
from rlib import tau as tau_bb, is_linear

def tau_table(n, edges):
    E = [sum(1 << x for x in e) for e in edges]
    N = 1 << n
    T = [0] * N
    for S in range(N):
        for e in E:
            if e & S == e:
                best = 99
                b = e
                while b:
                    lo = b & -b
                    b ^= lo
                    t = T[S ^ lo]
                    if t < best:
                        best = t
                T[S] = best + 1
                break
    return T, E

def popc(x):
    return bin(x).count('1')

def slack_of(S, T, E):
    return 3 * popc(S) + 2 * sum(1 for e in E if e & S == e) - 11 * T[S]

def vertex_critical(n, edges):
    T, E = tau_table(n, edges)
    full = (1 << n) - 1
    if slack_of(full, T, E) >= 0:
        return False, T, E
    for S in range(full):
        if slack_of(S, T, E) < 0:
            return False, T, E
    return True, T, E

def comps(mask, E, n):
    """components (as bitmasks) of the induced subgraph on mask."""
    left = mask
    out = []
    Ein = [e for e in E if e & mask == e]
    while left:
        b = left & -left
        comp = b
        changed = True
        while changed:
            changed = False
            for e in Ein:
                if e & comp and (e | comp) != comp:
                    comp |= e
                    changed = True
        out.append(comp)
        left &= ~comp
    return out

def analyse(n, edges, T, E, v, report):
    full = (1 << n) - 1
    sH = slack_of(full, T, E)
    at = [e for e in E if e >> v & 1]
    assert len(at) == 3
    pairs = [e & ~(1 << v) for e in at]
    G = full & ~(1 << v)
    F = comps(G, E, n)
    s = lambda S: slack_of(S, T, E)
    deg = lambda x, S: sum(1 for e in E if e & S == e and e >> x & 1)
    cot = lambda X, Fm: T[Fm & ~X] == T[Fm] - popc(X)
    bits = lambda m: [i for i in range(n) if m >> i & 1]
    fails = []
    # L017 Thm 4 basics
    if not (T[G] == T[full] - 1):
        fails.append('tau(G) != tau(H)-1')
    if any(popc(Fm) == 1 for Fm in F):
        fails.append('isolated vertex in G')
    r = len(F)
    comp_of = {}
    for i, Fm in enumerate(F):
        for x in bits(Fm):
            comp_of[x] = i
    loc = []
    for P in pairs:
        xs = bits(P)
        loc.append(tuple(comp_of[x] for x in xs))
    # pattern
    if r == 1:
        pat = 'a'
    elif r == 2:
        types = []
        for (c1, c2) in loc:
            types.append('s' if c1 != c2 else str(c1 + 1))
        ms = ''.join(sorted(types))
        # normalise 1<->2
        ms2 = ''.join(sorted(t if t == 's' else ('1' if t == '2' else '2') for t in types))
        key = min(ms, ms2)
        pat = {'sss': 'b', '11s': 'c1', '112': 'c2', '12s': 'e', '1ss': 'f'}.get(key, '?' + key)
    elif r == 3:
        pat = 'd?'
    else:
        pat = 'r%d' % r
    report['pat'][pat] = report['pat'].get(pat, 0) + 1
    # (i) no component contains two pairs when r>=2
    if r >= 2:
        for Fm in F:
            if sum(1 for P in pairs if P & Fm == P) >= 2:
                fails.append('(i) component contains two pairs')
    if pat == 'e':
        fails.append('(ii) pattern e occurs')
    if pat == 'f':
        # name: P1 inside F1; P2={c,d}, P3={e,f} split, c,e in F1
        inside = [P for P in pairs if any(P & Fm == P for Fm in F)][0]
        F1 = [Fm for Fm in F if inside & Fm == inside][0]
        F2 = [Fm for Fm in F if Fm != F1][0]
        split = [P for P in pairs if P != inside]
        d = [x for x in bits(split[0]) if F2 >> x & 1][0]
        f = [x for x in bits(split[1]) if F2 >> x & 1][0]
        if not (s(F1) == 1 and s(F2) == 0 and sH == -1):
            fails.append('(iii) slacks %d %d %d' % (s(F1), s(F2), sH))
        for y in (d, f):
            if s(F1 | 1 << v | 1 << y) != 0:
                fails.append('(iii) sub-extension not tight')
        e_f2 = [e for e in E if e & F2 == e]
        single = len(e_f2) == 1 and (e_f2[0] >> d & 1) and (e_f2[0] >> f & 1)
        sig = any((e >> d & 1) and (e >> f & 1) for e in e_f2)
        if not (single or (deg(d, F2) == 1 and deg(f, F2) == 1 and not sig)):
            fails.append('(iv)')
        report['f_cases'] += 1
    if pat == 'b':
        for Fm in F:
            att = [x for P in pairs for x in bits(P) if Fm >> x & 1]
            am = sum(1 << x for x in att)
            e_in = [e for e in E if e & Fm == e]
            if am in e_in and len(e_in) != 1:
                fails.append('(v) attachment triple is an edge but component not single edge')
            if s(Fm) == 0 and len(e_in) > 1:
                if sum(1 for x in att if deg(x, Fm) == 1) < 2:
                    fails.append('(vi)')
            if am in e_in:
                report['v_cases'] += 1
    # (vii)
    for P in pairs:
        for w in bits(P):
            if sum(1 for e in E if e >> w & 1) == 2:
                Fm = F[comp_of[w]]
                ew = [e for e in E if e & Fm == e and e >> w & 1]
                assert len(ew) == 1
                for p in bits(ew[0] & ~(1 << w)):
                    report['vii_pairs'] += 1
                    if cot((1 << w) | (1 << p), Fm):
                        fails.append('(vii)')
    return pat, fails

def random_linear(n, rng, maxdeg=3, tries=400):
    E = []
    pairs = set()
    deg = [0] * n
    for _ in range(tries):
        e = tuple(sorted(rng.sample(range(n), 3)))
        if any(deg[x] >= maxdeg for x in e):
            continue
        ps = list(combinations(e, 2))
        if any(p in pairs for p in ps):
            continue
        E.append(e)
        pairs.update(ps)
        for x in e:
            deg[x] += 1
    return E


def random_connected(n, rng, maxdeg=3, extra_tries=200):
    """Grow a connected linear 3-graph with max degree <= maxdeg covering n vertices."""
    E = [(0, 1, 2)]
    pairs = set([(0, 1), (0, 2), (1, 2)])
    deg = [0] * n
    for x in (0, 1, 2):
        deg[x] = 1
    k = 3
    fails = 0
    while k < n and fails < 500:
        old = [x for x in range(k) if deg[x] < maxdeg]
        if not old:
            return None
        a = rng.choice(old)
        if k + 2 <= n and rng.random() < 0.6:
            e = (a, k, k + 1)
        else:
            others = [x for x in range(k) if x != a and deg[x] < maxdeg and (min(a, x), max(a, x)) not in pairs]
            if not others or k + 1 > n:
                fails += 1
                continue
            b = rng.choice(others)
            e = tuple(sorted((a, b, k)))
        ps = [tuple(sorted(p)) for p in combinations(e, 2)]
        if any(p in pairs for p in ps):
            fails += 1
            continue
        E.append(tuple(sorted(e)))
        pairs.update(ps)
        for x in e:
            deg[x] += 1
        k = max(k, max(e) + 1)
    if k < n:
        return None
    for _ in range(extra_tries):
        e = tuple(sorted(rng.sample(range(n), 3)))
        if any(deg[x] >= maxdeg for x in e):
            continue
        ps = list(combinations(e, 2))
        if any(p in pairs for p in ps):
            continue
        if rng.random() < 0.5:
            E.append(e)
            pairs.update(ps)
            for x in e:
                deg[x] += 1
    return E

def run_graph(n, edges, report, name=None):
    vc, T, E = vertex_critical(n, edges)
    if not vc:
        return False
    report['violators'] += 1
    for v in range(n):
        if sum(1 for e in E if e >> v & 1) == 3:
            report['deg3'] += 1
            pat, fails = analyse(n, edges, T, E, v, report)
            if fails:
                report['fails'].append((name or edges, v, pat, fails))
            if name:
                print('   ', name, 'vertex', v, 'pattern', pat, 'fails', fails)
    return True

def main():
    report = {'violators': 0, 'deg3': 0, 'pat': {}, 'fails': [], 'f_cases': 0, 'v_cases': 0, 'vii_pairs': 0}
    F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
    V984a = [[0, 1, 2], [0, 3, 4], [1, 6, 7], [2, 5, 8], [3, 5, 7], [3, 6, 8], [4, 5, 6], [4, 7, 8]]
    V984b = [[0, 1, 4], [0, 2, 3], [1, 7, 8], [2, 5, 6], [3, 5, 8], [3, 6, 7], [4, 5, 7], [4, 6, 8]]
    for name, n, E in (('F7', 7, F7), ('(9,8,4)a', 9, V984a), ('(9,8,4)b', 9, V984b)):
        E = [tuple(e) for e in E]
        T, Em = tau_table(n, E)
        full = (1 << n) - 1
        print(name, 'n', n, 'm', len(E), 'tau', T[full], 'tau(bb)', tau_bb(E, list(range(n))),
              'slack', slack_of(full, T, Em), 'linear', is_linear(E), 'vertex-critical', vertex_critical(n, E)[0])
        run_graph(n, E, report, name)
    print('small violators:', json.dumps({k: v for k, v in report.items() if k != 'fails'}), 'fails', report['fails'])
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    nmin, nmax = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (7, 12)
    t0 = time.time()
    for it in range(trials):
        n = rng.randint(nmin, nmax)
        E = random_connected(n, rng) if rng.random() < 0.8 else random_linear(n, rng)
        if E is None:
            continue
        # keep the largest connected component as the graph
        if not E:
            continue
        run_graph(n, E, report)
    print('random: trials', trials, json.dumps({k: v for k, v in report.items() if k != 'fails'}),
          'nfails', len(report['fails']), 'time %.0fs' % (time.time() - t0))
    for f in report['fails'][:20]:
        print('FAIL', f)

if __name__ == '__main__':
    main()
