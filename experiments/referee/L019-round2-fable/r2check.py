"""Round-2 referee check of L019 (fable). Imports nothing from e757/, judge/, hg.py or pyverify.py.
Tests, by independent code:
  Theorem 5 (folding lemma): (a) n-2, m-2, injectivity; (b) tau(K) <= tau(K°)+1; (c) tau(K°)=tau-1 and s(K°)=s+1 when x
     is co-transversal; (d) linearity iff no common neighbour of y,z in K-x; every F7 of K° contains zeta; (P3) fails iff a
     saturated S (x not in S, y,z in S) exists (brute force, n<=14) and such S has |S|>=6.
  Theorem 3 / Fact 0.7 (pair-pair coverage): for disjoint non-edge pairs (P,Q): tau(F+v(P,Q)) = tau(F) iff some minimum
     transversal meets both; s(F+v) = s(F)-4 when not met, s(F)+7 when met; if the gadget is in C and n_F<=26, 'met' holds.
  (23,21,10): every stored class has a vertex degree outside {2,3}.
usage: python3 r2check.py <inputs_dir>
"""
import sys, itertools, random
from collections import Counter

def read_cell(path, K=None):
    out = []
    with open(path) as fh:
        for line in fh:
            a = list(map(int, line.split()))
            if not a: continue
            n, m, t = a[:3]
            E = [tuple(sorted(a[3+3*i:6+3*i])) for i in range(m)]
            assert len(E) == m
            out.append((n, m, t, E))
            if K is not None and len(out) >= K: break
    return out

def linear(E):
    for g, h in itertools.combinations(E, 2):
        if len(set(g) & set(h)) >= 2: return False
    return True

def has_f7(E):
    """F7 = {012,034,056,135,246}: centre 0 (unique degree-3 vertex), pairs {1,2},{3,4},{5,6}; edges 135, 246 take one
    vertex from each pair and are complementary."""
    Es = set(E)
    at = {}
    for g in E:
        for x in g: at.setdefault(x, []).append(g)
    for c, L in at.items():
        if len(L) < 3: continue
        for tri in itertools.combinations(L, 3):
            pairs = [tuple(sorted(set(g) - {c})) for g in tri]
            W = set().union(*map(set, pairs))
            if len(W) != 6: continue
            for choice in itertools.product(*pairs):
                g1 = tuple(sorted(choice)); g2 = tuple(sorted(W - set(choice)))
                if g1 in Es and g2 in Es: return True
    return False

def p3_hall(n, E):
    """(P3) e(S)<=|S|-2 for all |S|>=2  <=>  for every pair {a,b} the edges have an SDR inside V\\{a,b}."""
    m = len(E)
    for a, b in itertools.combinations(range(n), 2):
        adj = [[t for t in g if t != a and t != b] for g in E]
        match = {}  # vertex -> edge index
        def try_edge(i, seen):
            for t in adj[i]:
                if t in seen: continue
                seen.add(t)
                if t not in match or try_edge(match[t], seen):
                    match[t] = i; return True
            return False
        for i in range(m):
            if not try_edge(i, set()): return False
    return True

def p3_brute(n, E):
    masks = [sum(1 << x for x in g) for g in E]
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k < 2: continue
        e = sum(1 for M in masks if M & S == M)
        if e > k - 2: return False
    return True

def saturated_sets(n, E):
    """all S with |S|>=3 and e(S)=|S|-2 (brute force)"""
    masks = [sum(1 << x for x in g) for g in E]
    out = []
    for S in range(1, 1 << n):
        k = bin(S).count('1')
        if k < 3: continue
        e = sum(1 for M in masks if M & S == M)
        if e == k - 2: out.append(S)
    return out

def in_C(n, E):
    return linear(E) and not has_f7(E) and p3_hall(n, E)

def tau(n, E):
    """branch and bound: branch on a vertex of an uncovered edge of maximum 'uncovered degree'; lower bound = greedy
    disjoint uncovered edges."""
    masks = [sum(1 << x for x in g) for g in E]
    best = [len(masks)]
    def lb(rem):
        used = 0; c = 0
        for M in rem:
            if not M & used: used |= M; c += 1
        return c
    def rec(rem, k):
        if not rem:
            best[0] = min(best[0], k); return
        if k + lb(rem) >= best[0]: return
        deg = Counter()
        for M in rem:
            x = M
            while x:
                b = x & -x; deg[b] += 1; x ^= b
        e = max(rem, key=lambda M: sum(deg[1 << t] for t in range(n) if M >> t & 1))
        vs = sorted([1 << t for t in range(n) if e >> t & 1], key=lambda b: -deg[b])
        for b in vs:
            rec([M for M in rem if not M & b], k + 1)
    rec(masks, 0)
    return best[0]

def min_transversals(n, E, t):
    """all transversals of size exactly t (bitmasks), t = tau(n,E); branch on the first uncovered edge."""
    masks = [sum(1 << x for x in g) for g in E]
    out = set()
    def rec(rem, chosen, k):
        if not rem:
            if bin(chosen).count('1') == t: out.add(chosen)
            return
        if k == 0: return
        e = rem[0]
        for x in range(n):
            if e >> x & 1:
                b = 1 << x
                rec([M for M in rem if not M & b], chosen | b, k - 1)
    rec(masks, 0, t)
    # pad: transversals found with < t vertices cannot exist when t = tau; keep exact-size ones
    return sorted(out)

def slack(n, m, t): return 3*n + 2*m - 11*t

def fold(n, E, x, y, z):
    """K° = (K-x) with y,z identified. Returns (n°, image edge list as set of sorted tuples, zeta, mult) where mult
    counts images (to detect non-injectivity) ; vertices relabelled 0..n-3."""
    keep = [v for v in range(n) if v != x and v != z]  # z is merged into y
    lab = {v: i for i, v in enumerate(keep)}
    lab[z] = lab[y]
    zeta = lab[y]
    imgs = []
    for g in E:
        if x in g: continue
        img = tuple(sorted(lab[v] for v in g))
        imgs.append(img)
    return n - 2, imgs, zeta

def adjacent(E, a, b):
    return any(a in g and b in g for g in E)

def check_fold_theorem5(n, m, t, E, stats, brute_ok):
    deg = Counter(v for g in E for v in g)
    s = slack(n, m, t)
    Ts = min_transversals(n, E, t)
    cotrans = set()
    for T in Ts:
        for v in range(n):
            if T >> v & 1: cotrans.add(v)
    inC = in_C(n, E)
    for x in range(n):
        if deg[x] != 2: continue
        gx = [g for g in E if x in g]
        U = [v for v in gx[0] if v != x]; W = [v for v in gx[1] if v != x]
        for y in U:
            for z in W:
                if adjacent(E, y, z): stats['adjacent'] += 1; continue
                stats['folds'] += 1
                n0, imgs, zeta = fold(n, E, x, y, z)
                if any(len(g) != 3 for g in imgs): stats['FAIL_degenerate'] += 1
                if len(set(imgs)) != m - 2 or len(imgs) != m - 2: stats['FAIL_m'] += 1
                E0 = sorted(set(imgs))
                t0 = tau(n0, E0)
                if not (t <= t0 + 1): stats['FAIL_b'] += 1
                dz = sum(1 for g in E0 if zeta in g)
                if dz != deg[y] + deg[z] - 2: stats['FAIL_degzeta'] += 1
                if x in cotrans:
                    stats['folds_cotrans'] += 1
                    if t0 != t - 1: stats['FAIL_c_tau'] += 1
                    if slack(n0, len(E0), t0) != s + 1: stats['FAIL_c_slack'] += 1
                else:
                    stats['folds_noncotrans'] += 1
                    if t0 not in (t - 1, t): stats['FAIL_tau_range'] += 1
                if inC:
                    # (d) linearity criterion
                    Ex = [g for g in E if x not in g]
                    nb_y = set(v for g in Ex if y in g for v in g) - {y}
                    nb_z = set(v for g in Ex if z in g for v in g) - {z}
                    common = nb_y & nb_z
                    if linear(E0) != (len(common) == 0): stats['FAIL_d_linear'] += 1
                    # every F7 of K° contains zeta
                    if has_f7([g for g in E0 if zeta not in g]): stats['FAIL_d_f7'] += 1
                    # (P3) criterion
                    p3 = p3_hall(n0, E0)
                    if brute_ok:
                        if p3 != p3_brute(n0, E0): stats['FAIL_p3_hall_vs_brute'] += 1
                        sat = [S for S in saturated_sets(n, E) if not (S >> x & 1) and (S >> y & 1) and (S >> z & 1)]
                        if p3 != (len(sat) == 0): stats['FAIL_d_p3'] += 1
                        if sat:
                            mn = min(bin(S).count('1') for S in sat)
                            stats['blockmin_%d' % mn] += 1
                            if mn < 6: stats['FAIL_d_size'] += 1
                    inC0 = linear(E0) and not has_f7(E0) and p3
                    if inC0:
                        stats['fold_inC'] += 1
                        if x in cotrans and n0 <= 27 and slack(n0, len(E0), t0) < 0: stats['FAIL_I11_small'] += 1

def check_theorem3(n, m, t, E, stats, maxpairs, rng):
    s = slack(n, m, t)
    Ts = min_transversals(n, E, t)
    inE = set()
    for g in E:
        for a, b in itertools.combinations(g, 2): inE.add((a, b))
    pairs = [(a, b) for a in range(n) for b in range(a+1, n) if (a, b) not in inE]
    pp = [(P, Q) for P, Q in itertools.combinations(pairs, 2) if not set(P) & set(Q)]
    if len(pp) > maxpairs: pp = rng.sample(pp, maxpairs)
    for P, Q in pp:
        met = any(((T >> P[0] & 1) or (T >> P[1] & 1)) and ((T >> Q[0] & 1) or (T >> Q[1] & 1)) for T in Ts)
        v = n
        Ep = E + [tuple(sorted((v,) + P)), tuple(sorted((v,) + Q))]
        tp = tau(n + 1, Ep)
        sp = slack(n + 1, m + 2, tp)
        stats['pairpairs'] += 1
        if met:
            if tp != t or sp != s + 7: stats['FAIL_07_met'] += 1
        else:
            stats['uncovered'] += 1
            if tp != t + 1 or sp != s - 4: stats['FAIL_07_unmet'] += 1
            if in_C(n + 1, Ep):
                stats['uncovered_gadget_inC'] += 1
                if n <= 26 and s <= 1: stats['FAIL_thm3'] += 1
            else:
                stats['uncovered_gadget_notC'] += 1

def random_linear(rng, n, m):
    E = []
    tries = 0
    while len(E) < m and tries < 500:
        tries += 1
        g = tuple(sorted(rng.sample(range(n), 3)))
        if g in E: continue
        if all(len(set(g) & set(h)) <= 1 for h in E): E.append(g)
    return E

if __name__ == '__main__':
    D = sys.argv[1]
    rng = random.Random(2)
    # --- Theorem 5 on stored cells (small ones with brute force) ---
    for cell, K, brute in [('10_7_4', 5, True), ('10_8_4', 62, True), ('14_12_6', 11, True), ('12_10_5', 60, True),
                           ('13_9_5', 40, True), ('15_11_6', 30, False), ('17_13_7', 6, False)]:
        st = Counter()
        for (n, m, t, E) in read_cell('%s/cell_%s.txt' % (D, cell), K):
            assert tau(n, E) == t, (cell, 'stored tau wrong')
            assert in_C(n, E), (cell, 'not in C')
            st['graphs'] += 1
            check_fold_theorem5(n, m, t, E, st, brute)
        print('THM5 cell', cell, dict(sorted(st.items())), flush=True)
    # --- Theorem 5 (a)-(c) on random linear 3-graphs (not necessarily in C); (d) when in C ---
    st = Counter()
    for _ in range(400):
        n = rng.randint(6, 9); m = rng.randint(3, min(12, n*(n-1)//6))
        E = random_linear(rng, n, m)
        if not E: continue
        t = tau(n, E); st['graphs'] += 1
        check_fold_theorem5(n, len(E), t, E, st, True)
    print('THM5 random', dict(sorted(st.items())), flush=True)
    # --- Theorem 3 / 0.7 ---
    for cell, K, mx in [('10_7_4', 5, 2000), ('14_12_6', 11, 2000), ('17_13_7', 6, 1500), ('12_10_5', 40, 150),
                        ('15_11_6', 30, 150), ('6_3_2', 1, 2000), ('9_4_3', 1, 2000), ('13_9_5', 20, 100), ('8_5_3', 2, 2000)]:
        st = Counter()
        for (n, m, t, E) in read_cell('%s/cell_%s.txt' % (D, cell), K):
            st['graphs'] += 1; st['slack'] = slack(n, m, t)
            check_theorem3(n, m, t, E, st, mx, rng)
        print('THM3 cell', cell, dict(sorted(st.items())), flush=True)
    # --- (23,21,10): degrees ---
    bad = 0; tot = 0
    for (n, m, t, E) in read_cell('%s/cell_23_21_10.txt' % D):
        tot += 1
        deg = Counter(v for g in E for v in g)
        if all(deg[v] in (2, 3) for v in range(n)): bad += 1
    print('CELL 23_21_10: classes', tot, 'with all degrees in {2,3}:', bad)
