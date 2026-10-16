"""Two-point extensions of 12-point extremal (4,5)-sets (h=7, target: h(B)<=8). Adapted from experiments/20261015-2340-ext14-all/extend_all.py.
Exact: integers (set scaled by 4 so every T1 candidate is an integer) and Fractions (T2 intersections).
Case analysis exactly as results/proofs/L001-abase-two-point-extensions.md (T0/T1a/T1b/T2).
Usage: python3 extend12_all.py INPUT.json.gz OUTDIR NPROCS [--known] [--limit N] [--start K]
"""
import gzip, itertools, json, os, sys, time, random
from fractions import Fraction as F
from math import lcm
from multiprocessing import Pool

C2 = None

def ndist(q):
    return len({abs(u - v) for u, v in itertools.combinations(q, 2)})

def ap_triples(P):
    """index triples (i,j,k) i<k with P[i]+P[k]=2P[j]; P sorted ints"""
    pos = {v: i for i, v in enumerate(P)}
    out = []
    for i in range(len(P)):
        for k in range(i + 2, len(P)):
            s = P[i] + P[k]
            if s % 2 == 0 and s // 2 in pos:
                out.append((i, pos[s // 2], k))
    return out

def masks_of(P):
    return [(1 << i) | (1 << j) | (1 << k) for i, j, k in ap_triples(P)]

def has_indep(n, masks, target):
    """exists vertex subset of size target of 0..n-1 containing no mask? returns bitmask or None"""
    by_last = [[] for _ in range(n)]
    for m in masks:
        by_last[m.bit_length() - 1].append(m)
    res = []
    def rec(i, cur, size):
        if res: return
        if size + n - i < target: return
        if size == target:
            res.append(cur); return
        if i == n: return
        nxt = cur | (1 << i)
        if all(m & nxt != m for m in by_last[i]): rec(i + 1, nxt, size + 1)
        rec(i + 1, cur, size)
    rec(0, 0, 0)
    return res[0] if res else None

def alpha_masks(n, masks):
    t = 1
    best = 0
    # exact: increase target until none
    while True:
        r = has_indep(n, masks, t)
        if r is None: return t - 1
        t += 1

def all_max_indep(n, masks, target):
    """list of all independent sets of size target (as bitmasks)"""
    by_last = [[] for _ in range(n)]
    for m in masks:
        by_last[m.bit_length() - 1].append(m)
    res = []
    def rec(i, cur, size):
        if size + n - i < target: return
        if size == target:
            res.append(cur); return
        if i == n: return
        nxt = cur | (1 << i)
        if all(m & nxt != m for m in by_last[i]): rec(i + 1, nxt, size + 1)
        rec(i + 1, cur, size)
    rec(0, 0, 0)
    return res

def is_sidon_ints(S):
    S = sorted(S)
    sums = [x + y for i, x in enumerate(S) for y in S[i:]]
    return len(sums) == len(set(sums))

def candidates(P):
    out = set()
    for a, b in itertools.combinations(P, 2):
        s = a + b
        assert s % 2 == 0
        out.add(s // 2); out.add(2 * a - b); out.add(2 * b - a)
    return out - set(P)

def h_exact_B(B, hA_plus2=10):
    """B sorted ints, a (4,5)-set. returns (h, witness-ok). h<=10 trivial bound only if h(A)=8; we find witness of size 10 else exact."""
    n = len(B)
    ms = masks_of(B)
    r = has_indep(n, ms, hA_plus2)
    if r is not None:
        S = [B[i] for i in range(n) if r >> i & 1]
        assert is_sidon_ints(S)
        return hA_plus2
    return alpha_masks(n, ms)

def process(args, want_pairs=False):
    idx, setv = args
    t0 = time.time()
    A0 = sorted(setv)
    n = len(A0)
    assert n == 12
    A = [4 * a for a in A0]
    Aset = set(A)
    out = {'class': idx, 'set': A0}
    # (4,5) of A, h(A)
    assert all(ndist(q) >= 5 for q in itertools.combinations(A, 4))
    mA = masks_of(A)
    hA = alpha_masks(n, mA)
    assert hA == 7
    out['hA'] = hA
    allmax = all_max_indep(n, mA, hA)
    out['n_max_sidon'] = len(allmax)
    inter = (1 << n) - 1
    for m in allmax: inter &= m
    core = [A0[i] for i in range(n) if inter >> i & 1]
    out['in_all_max_sidon'] = core
    out['t2_precheck'] = len(core) > 0
    target = hA + 2
    # ---------------- T1
    single = {}
    pairs3 = list(itertools.combinations(A, 3))
    def single_ok(v):
        r = single.get(v)
        if r is None:
            r = all(ndist((v,) + q) >= 5 for q in pairs3)
            single[v] = r
        return r
    pairs2 = list(itertools.combinations(A, 2))
    def pair_ok(x, y):
        return all(ndist((x, y) + q) >= 5 for q in pairs2)
    Px = sorted(candidates(A))
    Px_ok = [x for x in Px if single_ok(x)]
    out['Px_size'] = len(Px); out['n_single_45'] = len(Px_ok)
    hist = {}
    def rec_h(h, k=1): hist[h] = hist.get(h, 0) + k
    records = []
    seen = set()
    t1_pairs = 0; t1b_45 = 0; t1b_set = set()
    for x in Px_ok:
        Ax = sorted(A + [x])
        hAx = alpha_masks(n + 1, masks_of(Ax))
        rec_h(hAx + 1)   # T1a (y generic): h = h(A u x)+1
        if hAx + 1 < target: records.append(('T1a', x, None, hAx + 1))
        for y in sorted(candidates(Ax)):
            key = frozenset((x, y))
            if key in seen: continue
            seen.add(key)
            t1_pairs += 1
            if not single_ok(y) or not pair_ok(x, y): continue
            t1b_45 += 1; t1b_set.add(key)
            B = sorted(Ax + [y])
            h = h_exact_B(B, target)
            rec_h(h)
            if h < target: records.append(('T1b', x, y, h))
    out['t1_pairs'] = t1_pairs; out['n_t1b_45'] = t1b_45
    # ---------------- T2
    base = ap_triples(A)
    bmasks = [(1 << i) | (1 << j) | (1 << k) for i, j, k in base]
    lines = []
    for a in A:
        lines.append(('x_mid', F(2), F(-a))); lines.append(('y_mid', F(1, 2), F(a, 2))); lines.append(('a_mid', F(-1), F(2 * a)))
    line_h = []
    for t, a in enumerate(A):
        ai = t
        for role in ('x_mid', 'y_mid', 'a_mid'):
            m = bmasks + [(1 << ai) | (1 << n) | (1 << (n + 1))]   # vertices 14,15 are x,y: labels irrelevant for the hyperedge, but index order must have x,y last
            r = has_indep(n + 2, m, target)
            if r is not None:
                line_h.append(target)
            else:
                h = alpha_masks(n + 2, m)
                line_h.append(h)
                records.append(('T2line', role, A0[ai], h))
    out['t2_line_h'] = sorted(set(line_h)); out['t2_lines'] = len(line_h)
    for h in line_h: rec_h(h)
    # exceptional points: pairwise intersections of non-parallel lines
    isect = set()
    for (r1, m1, c1), (r2, m2, c2) in itertools.combinations(lines, 2):
        if m1 == m2: continue
        x = (c2 - c1) / (m1 - m2); y = m1 * x + c1
        isect.add((x, y))
    t2_pts = 0; t2_45 = 0
    for x, y in sorted(isect):
        if x == y or x in Aset or y in Aset: continue
        t2_pts += 1
        D = lcm(x.denominator, y.denominator)
        AD = [a * D for a in A]; xi = int(x * D); yi = int(y * D)
        if xi in AD or yi in AD: continue
        if not all(ndist((xi,) + q) >= 5 for q in itertools.combinations(AD, 3)): continue
        if not all(ndist((yi,) + q) >= 5 for q in itertools.combinations(AD, 3)): continue
        if not all(ndist((xi, yi) + q) >= 5 for q in itertools.combinations(AD, 2)): continue
        t2_45 += 1
        if frozenset((x, y)) in seen: continue
        seen.add(frozenset((x, y)))
        B = sorted(AD + [xi, yi])
        h = h_exact_B(B, target)
        rec_h(h)
        if h < target: records.append(('T2isect', str(x), str(y), h))
    out['t2_isect_pts'] = t2_pts; out['t2_isect_45'] = t2_45
    out['hist'] = {str(k): v for k, v in sorted(hist.items())}
    out['min_h'] = min(hist) if hist else None
    out['records'] = [list(map(str, r)) for r in records]
    out['n_2ext'] = t1b_45 + out['t2_isect_45']
    if want_pairs: out['_t1b'] = t1b_set; out['_Px_ok'] = Px_ok; out['_seen45'] = None
    out['secs'] = round(time.time() - t0, 1)
    return out

def load_sets(inp):
    op = gzip.open if inp.endswith('.gz') else open
    with op(inp, 'rt') as f:
        d = json.load(f)
    return [(i, r['set']) for i, r in enumerate(d)]

KNOWN = {
 'omega1': None, 'omega2': None,
 'third': [0,269,385,467,501,511,521,523,535,538,549,575],
}

def known_sets():
    d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'small_records.json')))
    out = []
    for k, v in d['sets'].items() if isinstance(d['sets'], dict) else enumerate(d['sets']):
        if isinstance(v, dict): v = v.get('set', v.get('A'))
        if v and len(v) == 12: out.append((str(k), sorted(v)))
    return out

def main():
    inp, outdir, nprocs = sys.argv[1], sys.argv[2], int(sys.argv[3])
    limit = None
    if '--limit' in sys.argv: limit = int(sys.argv[sys.argv.index('--limit') + 1])
    os.makedirs(outdir, exist_ok=True)
    try: os.nice(5)
    except Exception: pass
    if '--known' in sys.argv:
        for k, v in known_sets():
            r = process((k, v)); r.pop('records', None) if False else None
            print(json.dumps(r), flush=True)
        return
    sets = load_sets(inp)
    if limit: sets = sets[:limit]
    jl = os.path.join(outdir, 'results.jsonl')
    done = set()
    if os.path.exists(jl):
        for line in open(jl):
            try: done.add(json.loads(line)['class'])
            except Exception: pass
    todo = [s for s in sets if s[0] not in done]
    t0 = time.time(); cnt = len(done)
    prog = os.path.join(outdir, 'progress.txt')
    with Pool(nprocs) as pool, open(jl, 'a') as fo:
        for r in pool.imap_unordered(process, todo, chunksize=4):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            cnt += 1
            if r['records']:
                with open(os.path.join(outdir, 'RECORD_CANDIDATES.txt'), 'a') as fr:
                    fr.write(json.dumps({'class': r['class'], 'set': r['set'], 'records': r['records']}) + '\n')
                print('RECORD CANDIDATE class', r['class'], r['records'][:3], flush=True)
            if cnt % 1000 == 0 or cnt == len(sets):
                with open(prog, 'w') as fp:
                    fp.write(f'{cnt}/{len(sets)} classes done, {time.time()-t0:.0f}s elapsed this run\n')
                print(cnt, len(sets), time.time() - t0, flush=True)
    res = [json.loads(l) for l in open(jl)]
    res.sort(key=lambda r: r['class'])
    ghist = {}
    for r in res:
        ghist[str(r['min_h'])] = ghist.get(str(r['min_h']), 0) + 1
    summ = {'classes_processed': len(res), 'total_2ext_45': sum(r['n_2ext'] for r in res),
            'total_t1b_45': sum(r['n_t1b_45'] for r in res),
            'total_t2_isect_45': sum(r['t2_isect_45'] for r in res),
            'total_single_45': sum(r['n_single_45'] for r in res),
            'single_45_min_max': [min(r['n_single_45'] for r in res), max(r['n_single_45'] for r in res)],
            'n_max_sidon_min_max': [min(r['n_max_sidon'] for r in res), max(r['n_max_sidon'] for r in res)],
            'hist_min_h': ghist, 'classes_min_h_le_8': sum(1 for r in res if r['min_h'] is not None and r['min_h'] <= 8),
            'classes_with_record_candidates': sum(1 for r in res if r['records']),
            'classes_t2_precheck_true': sum(1 for r in res if r['t2_precheck']),
            'all_hA_7': all(r['hA'] == 7 for r in res)}
    json.dump({'summary': summ, 'classes': res}, open(os.path.join(outdir, 'results.json'), 'w'))
    print(summ)

if __name__ == '__main__':
    main()
