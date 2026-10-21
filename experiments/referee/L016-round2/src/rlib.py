"""Referee (L016 round 2) helper library, written from scratch (no code of experiments/prover/* or of the worker's folder).
Cell files are read as data ("FOUND: (a,b,c) ..." lines, INFO json line)."""
import os, re, json, itertools, subprocess, gzip
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REXT = os.path.join(R, 'bin', 'rext')
LABELG = os.path.join(R, 'out', 'nauty', 'nauty2_8_8', 'labelg')
PAT = re.compile(r'\((\d+),(\d+),(\d+)\)')

def read_cell(path):
    """returns (list of edge lists, info dict or None)"""
    op = gzip.open if path.endswith('.gz') else open
    reps = []; info = None
    with op(path, 'rt') as f:
        for l in f:
            if l.startswith('FOUND:'):
                reps.append([tuple(map(int, t)) for t in PAT.findall(l)])
            elif l.startswith('INFO '):
                info = json.loads(l[5:])
    return reps, info

def cell_path(celldir, n, m, t, D):
    return os.path.join(celldir, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))

def types(N, S):
    """all component types (n,m,t) with slack 0..S: isolated vertex, and connected types allowed by
    n>=3, 1<=m<=n-2, n<=2m+1, 1<=t<=m, 17t<=5n+3m (K8)."""
    out = []
    if S >= 3: out.append((1, 0, 0))
    for n in range(3, N + 1):
        for m in range(1, n - 1):
            if n > 2 * m + 1: continue
            for t in range(1, m + 1):
                s = 3 * n + 2 * m - 11 * t
                if 0 <= s <= S and 17 * t <= 5 * n + 3 * m: out.append((n, m, t))
    return out

def slack(tp): return 3 * tp[0] + 2 * tp[1] - 11 * tp[2]

def my_decomps(N, M, S):
    """all multisets of component types with sum n = N, sum m = M, total slack = S (brute force over multiplicities)."""
    T = types(N, S); sols = []
    def rec(i, n, m, s, ch):
        if n == N and m == M and s == S: sols.append(tuple(sorted(ch))); return
        if i == len(T) or n >= N: return
        tp = T[i]; k = 0
        while n + k * tp[0] <= N and m + k * tp[1] <= M and s + k * slack(tp) <= S:
            rec(i + 1, n + k * tp[0], m + k * tp[1], s + k * slack(tp), ch + [tp] * k); k += 1
    rec(0, 0, 0, 0, [])
    return sorted(set(sols))

def branches(n, m, t, D, nprev=None):
    """(d, tp, S') with ceil(3m/n) <= d <= D, tp in {t-1, t}, S' >= 0."""
    out = []
    dmin = max(1, -(-3 * m // n))
    for d in range(dmin, D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp >= 0 and tp >= 0: out.append((d, tp, Sp))
    return out

_cache = {}
def lst(celldir, n, m, t, D):
    if (n, m) == (1, 0): return [[]]
    key = (celldir, n, m, t, D)
    if key not in _cache:
        p = cell_path(celldir, n, m, t, D)
        if not os.path.exists(p): raise FileNotFoundError(p)
        _cache[key] = read_cell(p)[0]
    return _cache[key]

def inputs_for(dec, celldir, d, nv):
    """disjoint unions: types in sorted order, multisets via combinations_with_replacement, product; consecutive blocks."""
    groups = {}
    for c in dec: groups[c] = groups.get(c, 0) + 1
    gl = []
    for tp in sorted(groups):
        cls = lst(celldir, tp[0], tp[1], tp[2], d)
        gl.append((tp, cls, list(itertools.combinations_with_replacement(range(len(cls)), groups[tp]))))
    for combo in itertools.product(*[g[2] for g in gl]):
        es = []; off = 0
        for (tp, cls, _), idxs in zip(gl, combo):
            for i in idxs:
                es += [(a + off, b + off, c + off) for (a, b, c) in cls[i]]; off += tp[0]
        assert off == nv, (off, nv)
        yield '%d ' % len(es) + ' '.join('%d %d %d' % e for e in es)

def count_inputs(dec, celldir, d):
    from math import comb
    groups = {}
    for c in dec: groups[c] = groups.get(c, 0) + 1
    tot = 1
    for tp, k in groups.items():
        L = len(lst(celldir, tp[0], tp[1], tp[2], d)); tot *= comb(L + k - 1, k)
    return tot

def labelg_set(g6lines):
    if not g6lines: return set()
    r = subprocess.run([LABELG, '-q'], input='\n'.join(g6lines) + '\n', capture_output=True, text=True, check=True)
    return set(r.stdout.split())

def found_to_g6(reps, n):
    lines = ['FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) for es in reps]
    if not lines: return []
    r = subprocess.run([REXT, 'g6', str(n)], input='\n'.join(lines) + '\n', capture_output=True, text=True, check=True)
    return r.stdout.split()

def canon_set_of_reps(reps, n):
    return labelg_set(found_to_g6(reps, n))

def run_ext(input_lines, NG, TG, d, EP, outfile=None):
    """runs rext ext; returns (set of canonical g6, summary line)"""
    r = subprocess.run(['nice', '-n', '10', REXT, 'ext', str(NG), str(TG), str(d), str(EP)], input='\n'.join(input_lines) + '\n',
                       capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError('rext failed rc=%d %s' % (r.returncode, r.stderr[-500:]))
    g6 = r.stdout.split()
    return labelg_set(g6), r.stderr.strip().splitlines()[-1], len(g6)
