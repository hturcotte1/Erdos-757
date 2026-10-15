"""Falsification of kb/notes/extension_lemmas.md (Lemma E, U/U1/U2, Delta). Exact integer arithmetic.
Usage: nice -n 15 python3 falsify.py [seed]"""
import sys, json, gzip, glob, random, itertools, time
from fractions import Fraction
sys.path.insert(0, '/home/user/Erdos-757')
from e757.core import ap_edges, is_45_set

ROOT = '/home/user/Erdos-757/'
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)

def hyper(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return A, [tuple(idx[v] for v in e) for e in ap_edges(A)]

def alpha_mask(n, emasks, allowed):
    """max independent set size within vertex bitmask `allowed`."""
    best = [0]
    by_v = [[] for _ in range(n)]
    for em in emasks:
        for v in range(n):
            if em >> v & 1: by_v[v].append(em)
    def rec(cand, cur, size):
        if size + bin(cand).count('1') <= best[0]: return
        if cand == 0:
            best[0] = max(best[0], size); return
        v = (cand & -cand).bit_length() - 1
        cand2 = cand & ~(1 << v)
        # include v if no edge becomes fully inside cur|v
        ncur = cur | (1 << v)
        ok = all((em & ~ncur) != 0 for em in by_v[v])
        if ok: rec(cand2, ncur, size + 1)
        rec(cand2, cur, size)
    rec(allowed, 0, 0)
    return best[0]

class HG:
    def __init__(self, A):
        self.A, self.E = hyper(A)
        self.n = len(self.A); self.m = len(self.E)
        self.em = [sum(1 << v for v in e) for e in self.E]
        full = (1 << self.n) - 1
        self.alpha = alpha_mask(self.n, self.em, full)
        self.tau = self.n - self.alpha
        self.deg = [sum(1 for e in self.E if v in e) for v in range(self.n)]
        self._univ = None
    def universal(self):
        if self._univ is None:
            full = (1 << self.n) - 1
            self._univ = [v for v in range(self.n)
                          if alpha_mask(self.n, self.em, full & ~(1 << v)) == self.alpha - 1]
        return self._univ

# ------------------------------------------------------------------ data
def load_sets():
    out = []  # (source, set)
    d = json.load(open(ROOT + 'data/small_records.json'))['sets']
    for k, v in d.items(): out.append(('records_' + k, v['set']))
    res = ROOT + 'experiments/20261014-1430-small-counts/results/'
    for f in sorted(glob.glob(res + 'n*_m*_real.json.gz')):
        L = json.load(gzip.open(f)); name = f.split('/')[-1][:-13]
        for r in (L if len(L) <= 1200 else rng.sample(L, 1200)):
            out.append((name, r['set']))
    L = json.load(gzip.open(ROOT + 'experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'))
    for r in rng.sample(L, 1500): out.append(('n12_census', r['set']))
    L = [json.loads(l) for l in gzip.open(ROOT + 'data/census_n14_m12_classes.jsonl.gz', 'rt')]
    for r in rng.sample(L, 150): out.append(('n14_census', r['set']))
    out.append(('A_base', json.load(open(ROOT + 'data/small_records.json'))['sets']['14']['set']))
    # Fibonacci sets
    F = [2, 3]
    while len(F) < 14: F.append(F[-1] + F[-2])
    for n in (8, 10, 12, 14): out.append(('fib%d' % n, F[:n]))
    return out

TS = [1, 3, 7, 101, 1009, 1000003] + [rng.randrange(10**6, 10**12) for _ in range(3)]

def pr(*a): print(*a, flush=True)

# ------------------------------------------------------------------ main
if __name__ == '__main__':
    t0 = time.time()
    sets = load_sets()
    pr('sets loaded', len(sets))
    stats = {'E_total': 0, 'E_bad_t': {}, 'E_formula_fail': [], 'E_univ_extreme': [], 'U_fail': [], 'U1_fail': [],
             'univ_any': [], 'U2_deg0': [], 'E_not45_generic': [], 'E_edge_fail': []}
    per_src_univ = {}
    for src, S in sets:
        A = sorted(S)
        if not is_45_set(A) and len(A) <= 14:
            pr('WARNING not 45', src); continue
        H = HG(A)
        U = H.universal()
        n, m, tau = H.n, H.m, H.tau
        # --- Lemma U: all universal vertices (extreme or not)
        for v in U:
            lhs = 17 * tau; rhs = 5 * (n - 1) + 3 * (m - H.deg[v])
            rec = dict(src=src, n=n, m=m, tau=tau, v=v, deg=H.deg[v], extreme=v in (0, n - 1), set=A)
            stats['univ_any'].append(rec)
            if lhs > rhs: stats['U_fail'].append(rec)
            slack = 5 * n + 3 * m - 17 * tau
            if H.deg[v] >= 1 and slack < 5 + 3 * H.deg[v]: stats['U_fail'].append(dict(rec, why='U2'))
            if H.deg[v] == 0 and slack < 5: stats['U_fail'].append(dict(rec, why='U2 deg0'))
        if n == 14 and m == 12 and tau == 6 and U: stats['U1_fail'].append((src, U, A))
        # --- Lemma E
        B = [2 * x for x in A]; HB = H
        for ai in (0, n - 1):
            a = B[ai]; univ = ai in U
            for t in TS:
                C = sorted(B + [a - t, a + t])
                if len(set(C)) != n + 2:
                    stats['E_bad_t'].setdefault(t, []).append((src, 'collision')); continue
                stats['E_total'] += 1
                ok45 = is_45_set(C)
                HC = HG(C)
                hexp = H.alpha + (1 if univ else 2)
                # expected edges: old edges + one
                xi, yi = C.index(a + t), C.index(a - t); ai2 = C.index(a)
                exp_edges = {tuple(sorted((C.index(B[u]) for u in e))) for e in H.E} | {tuple(sorted((xi, yi, ai2)))}
                got_edges = {tuple(sorted(e)) for e in HC.E}
                edge_ok = exp_edges == got_edges
                if not (ok45 and edge_ok and HC.alpha == hexp):
                    stats['E_bad_t'].setdefault(t, []).append((src, ai, ok45, edge_ok, HC.alpha, hexp))
                if ok45 and edge_ok and HC.alpha != hexp:
                    stats['E_formula_fail'].append((src, ai, t, HC.alpha, hexp))
                if edge_ok and not ok45:
                    stats['E_not45_generic'].append((src, ai, t))
    # summarise
    pr('time', time.time() - t0)
    s = stats
    out = {k: (v if not isinstance(v, list) else len(v)) for k, v in s.items() if k != 'E_bad_t'}
    out['E_bad_t'] = {str(t): len(v) for t, v in s['E_bad_t'].items()}
    out['E_bad_t_examples'] = {str(t): v[:3] for t, v in s['E_bad_t'].items()}
    out['universal_vertices_examples'] = s['univ_any'][:10]
    pr(json.dumps(out, indent=1, default=str)[:6000])
    json.dump({'summary': out, 'univ_any': s['univ_any'], 'E_formula_fail': s['E_formula_fail'],
               'U_fail': s['U_fail']}, open('results_testsE_U.json', 'w'), default=str)
