"""(L013, prover) Independent audit of a cell directory produced by engine.py (pure Python, written from scratch).
For every cell file cell_n_m_t_D<D>.txt with an INFO line:
 (1) every representative is re-verified from the definitions: labels in 0..n-1, exactly m distinct 3-sets, connected on all n vertices,
     linear, F7-free (structural test: a centre c, three edges at c, one vertex from each of the three pairs forming an edge whose
     complement in the six vertices is also an edge), (P3) (for every pair {x,y} of vertices the edges have distinct representatives
     avoiding x and y, by augmenting paths), exact tau (branching on an uncovered edge), maximum degree <= D;
 (2) for recursion cells: the set of branches is exactly {(d, t') : ceil(3m/n) <= d <= D, t' in {t-1, t}, S' >= 0}; in each branch the
     decomposition list equals decomp_bf.bf_decomps(n-1, m-d, S') (independent generator); the number of inputs equals
     sum over decompositions of prod_types C(|cell(type, d)| + k - 1, k), computed from THIS directory's cell files; and the ext_d counters
     satisfy graphs = searched = inputs, bad_tau = 0, tg_too_small = 0 (whenever there are inputs);
 (3) for direct cells: the route is direct only if m <= MD.
Usage: python3 check_cells.py CELLDIR [MD] [--skipverify]   (prints a summary and writes CELLDIR/../check_cells_summary.json)"""
import os, re, sys, json, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decomp_bf import bf_decomps
def parse_edges(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def tau_exact(edges):
    E = [frozenset(e) for e in edges]
    def cov(k, rem):
        if not rem: return True
        if k == 0: return False
        e = rem[0]
        for v in e:
            if cov(k - 1, [f for f in rem if v not in f]): return True
        return False
    k = 0
    while not cov(k, E): k += 1
    return k
def linear(edges):
    S = [set(e) for e in edges]
    return all(len(S[i] & S[j]) <= 1 for i in range(len(S)) for j in range(i + 1, len(S)))
def has_f7(edges):
    E = set(frozenset(e) for e in edges); at = {}
    for e in edges:
        for v in e: at.setdefault(v, []).append(e)
    for c, es in at.items():
        for tri in itertools.combinations(es, 3):
            pairs = [tuple(x for x in e if x != c) for e in tri]
            for choice in itertools.product((0, 1), repeat=3):
                T1 = frozenset(p[ch] for p, ch in zip(pairs, choice)); T2 = frozenset(p[1 - ch] for p, ch in zip(pairs, choice))
                if T1 in E and T2 in E: return True
    return False
def p3(edges, n):
    used = sorted(set(v for e in edges for v in e))
    for x, y in itertools.combinations(used, 2):
        owner = {}
        def aug(i, seen):
            for v in edges[i]:
                if v in (x, y) or v in seen: continue
                seen.add(v)
                if v not in owner or aug(owner[v], seen): owner[v] = i; return True
            return False
        for i in range(len(edges)):
            if not aug(i, set()): return False
    return True
def connected(edges, n):
    comp = {0}; ch = True
    while ch:
        ch = False
        for e in edges:
            if comp & set(e) and not set(e) <= comp: comp |= set(e); ch = True
    return len(comp) == n
def verify(edges, n, m, t, D):
    if any(not (0 <= v < n) for e in edges for v in e) or any(len(set(e)) != 3 for e in edges): return 'labels'
    if len(set(frozenset(e) for e in edges)) != m or len(edges) != m: return 'm'
    if n > 1 and not connected(edges, n): return 'disconnected'
    if not linear(edges): return 'nonlinear'
    if has_f7(edges): return 'F7'
    if not p3(edges, n): return 'P3'
    deg = [0] * n
    for e in edges:
        for v in e: deg[v] += 1
    if max(deg + [0]) > D: return 'degree'
    if tau_exact(edges) != t: return 'tau'
    return None
def load_dir(cd):
    cells = {}
    for fn in os.listdir(cd):
        mm = re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', fn)
        if not mm: continue
        key = tuple(map(int, mm.groups())); reps = []; info = None
        for l in open(os.path.join(cd, fn)):
            if l.startswith('FOUND:'): reps.append(parse_edges(l))
            elif l.startswith('INFO '): info = json.loads(l[5:])
        cells[key] = (reps, info)
    return cells
def main():
    cd = sys.argv[1]; MD = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 10; skip = '--skipverify' in sys.argv
    cells = load_dir(cd); problems = []; nrep = 0; nbranch = 0; ndec = 0; nonempty = {}
    def count(key):
        n, m, t, D = key
        if (n, m) == (1, 0): return 1
        if m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1: return 0
        if key not in cells: problems.append(('missing subcell', key)); return None
        return len(cells[key][0])
    for key in sorted(cells):
        n, m, t, D = key; reps, info = cells[key]
        if info is None: problems.append(('no INFO', key)); continue
        if reps: nonempty[key] = len(reps)
        if not skip:
            for es in reps:
                nrep += 1; r = verify(es, n, m, t, D)
                if r: problems.append(('rep fails ' + r, key, es))
        if info['route'] == 'direct':
            if m > MD: problems.append(('direct route with m > MD', key))
            continue
        if m <= MD: problems.append(('recursion with m <= MD', key))
        exp = [(d, tp) for d in range(max(1, math.ceil(3 * m / n)), D + 1) for tp in (t - 1, t)
               if tp >= 0 and 3 * (n - 1) + 2 * (m - d) - 11 * tp >= 0]
        got = [(b['d'], b['tp']) for b in info['branches']]
        if exp != got: problems.append(('branch set', key, exp, got))
        for b in info['branches']:
            nbranch += 1; d, tp, Sp = b['d'], b['tp'], b['Sp']
            if Sp != 3 * (n - 1) + 2 * (m - d) - 11 * tp: problems.append(('Sp', key, b['d'], b['tp']))
            eng = set(tuple(sorted(tuple(x) for x in dec)) for dec, size in b['dec']); bf = bf_decomps(n - 1, m - d, Sp); ndec += len(bf)
            if eng != bf or len(b['dec']) != b['decompositions']: problems.append(('decompositions differ', key, d, tp, len(eng), len(bf)))
            tot = 0
            for dec, size in b['dec']:
                g = {}
                for c in dec: g[tuple(c)] = g.get(tuple(c), 0) + 1
                pr = 1
                for typ, k in g.items():
                    c = count((typ[0], typ[1], typ[2], d))
                    if c is None: pr = None; break
                    pr *= math.comb(c + k - 1, k)
                if pr is not None and pr != size: problems.append(('product size', key, d, tp, dec, size, pr))
                tot += size
            if tot != b['inputs']: problems.append(('inputs sum', key, d, tp, tot, b['inputs']))
            if b['inputs']:
                e = b.get('ext')
                if not e or e.get('graphs') != b['inputs'] or e.get('searched') != b['inputs'] or e.get('bad_tau') != 0 or e.get('tg_too_small') != 0:
                    problems.append(('ext counters', key, d, tp, e))
    nrec = sum(1 for k in cells if cells[k][1] and cells[k][1]['route'] == 'recurse')
    summ = dict(celldir=cd, cells=len(cells), recursion_cells=nrec, direct_cells=len(cells) - nrec, representatives_verified=nrep,
                branches=nbranch, decompositions_checked=ndec, problems=len(problems), nonempty_cells=len(nonempty))
    print('SUMMARY', json.dumps(summ))
    for p in problems[:50]: print('PROBLEM', p)
    json.dump(dict(summary=summ, problems=[str(p) for p in problems],
                   cells={'%d_%d_%d_D%d' % k: dict(classes=len(cells[k][0]), route=cells[k][1]['route'] if cells[k][1] else None,
                                                   secs=cells[k][1].get('secs') if cells[k][1] else None) for k in sorted(cells)}),
              open(os.path.join(os.path.dirname(os.path.abspath(cd.rstrip('/'))), 'check_cells_summary_%s.json' % os.path.basename(cd.rstrip('/'))), 'w'), indent=0)
if __name__ == '__main__': main()
