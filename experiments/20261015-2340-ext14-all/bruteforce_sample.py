"""Independent plain-integer brute-force cross-check of L005 on a deterministic sample of classes.
No e757 imports and no extend_all imports in the brute-force part (numpy is used only for vectorised integer
arithmetic).  Coordinates are doubled so half-integers become integers.  For a class A (doubled):
window = integers in [min - span/DIV, max + span/DIV] (DIV=4 by default), x,y not in A.
 * single (4,5): every 4-subset {x,a,b,c} has >= 5 distinct differences.
 * pair (4,5): additionally every 4-subset {x,y,a,b}; x<y both single-valid.
 * for every (4,5) pair a 3-AP-free 10-subset of A u {x,y} exists: 8-subsets c of A that are 3-AP-free
   (all enumerated), c+{x,y} is 3-AP-free iff c+x, c+y are and no AP uses both x and y; this is computed with bitmasks
   over the maximum 8-subsets and EXPLICITLY re-verified (AP-free + Sidon + subset + size 10) for all pairs with a
   cross AP and for every 997th pair; a pair with an empty mask goes to an exhaustive 10-subset fallback.
Usage: python3 bruteforce_sample.py [--div 4] [--procs 2] [--classes 0,2440,...]  (writes bruteforce_sample_results.json)
The comparison with L005's stored counts (results.jsonl) is done separately in main(), after the brute force."""
import gzip, itertools, json, os, sys, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
CLASSES = sorted(set([0, 2440]) | {73 * k for k in range(1, 40)})
DIV = 4

def ap_free(S):
    s = set(S); L = sorted(S)
    return not any(2 * L[j] - L[i] in s for i in range(len(L)) for j in range(i + 1, len(L)))

def sidon(S):
    L = sorted(S); sums = [p + q for i, p in enumerate(L) for q in L[i:]]
    return len(sums) == len(set(sums))

def ndist(q):
    return len({abs(p - r) for p, r in itertools.combinations(q, 2)})

def brute(args):
    idx, A0, div = args
    t0 = time.time()
    A = sorted(2 * a for a in A0); AS = set(A); n = len(A)
    assert n == 14
    assert all(ndist(q) >= 5 for q in itertools.combinations(A, 4))
    S8 = [c for c in itertools.combinations(A, 8) if ap_free(c)]
    assert not any(ap_free(c) for c in itertools.combinations(A, 9))
    nS8 = len(S8); assert nS8 <= 192
    span = A[-1] - A[0]
    lo = A[0] - span // div; hi = A[-1] + span // div
    # P_x (doubled coordinates): x forms a 3-AP with two points of A
    Px = set()
    for a, b in itertools.combinations(A, 2):
        if (a + b) % 2 == 0: Px.add((a + b) // 2)
        Px.add(2 * a - b); Px.add(2 * b - a)
    Px -= AS
    # valid singles
    triples = list(itertools.combinations(A, 3))
    vals = []
    for v in range(lo, hi + 1):
        if v in AS: continue
        if all(ndist((v,) + t) >= 5 for t in triples): vals.append(v)
    nsingle_all = len(vals)
    singles_Px = [v for v in vals if v in Px]
    # masks over S8 : which c have c+x AP-free
    nw = 3
    def tow(m): return [(m >> (64 * w)) & ((1 << 64) - 1) for w in range(nw)]
    Mx = []
    for v in vals:
        m = 0
        for ci, c in enumerate(S8):
            if ap_free(c + (v,)): m |= 1 << ci
        Mx.append(m)
    W = np.array([tow(m) for m in Mx], dtype=np.uint64)          # (N, 3)
    abit = {a: sum(1 << ci for ci, c in enumerate(S8) if a in c) for a in A}   # c containing a
    V = np.array(vals, dtype=np.int64); N = len(V)
    Aarr = np.array(A, dtype=np.int64)
    IJ = [(i, j) for i in range(n) for j in range(i + 1, n)]
    dxall = np.abs(V[:, None] - Aarr[None, :])                   # (N, 14)
    total45 = 0; nfail = 0; ncross = 0; nver = 0; nfallback = 0; nline_hit = 0
    npairs_Px_both = 0
    for xi in range(N - 1):
        x = int(V[xi]); ys = V[xi + 1:]; M = len(ys)
        ok = np.ones(M, dtype=bool)
        d = np.abs(ys - x)
        dy = dxall[xi + 1:]                                        # (M,14)
        dx = dxall[xi]
        for (i, j) in IJ:
            if not ok.any(): break
            dab = A[j] - A[i]
            cols = np.stack([d, np.full(M, dx[i]), np.full(M, dx[j]), dy[:, i], dy[:, j], np.full(M, dab)], axis=1)
            cols.sort(axis=1)
            nd = 1 + (cols[:, 1:] != cols[:, :-1]).sum(axis=1)
            ok &= nd >= 5
        idxs = np.nonzero(ok)[0]
        if len(idxs) == 0: continue
        total45 += len(idxs)
        yv = ys[idxs]
        # cross APs involving both x and y
        s = x + yv
        cross = (np.isin(2 * x - yv, Aarr)) | (np.isin(2 * yv - x, Aarr)) | ((s % 2 == 0) & np.isin(s // 2, Aarr))
        wm = (W[xi][None, :] & W[xi + 1 + idxs])                  # (k,3)
        has = wm.any(axis=1)
        # pairs with no cross AP: witness exists iff has
        bad = ~has & ~cross
        nfail_pairs = []
        special = np.nonzero(cross | bad)[0]
        # deterministic explicit verification of every 997th pair
        sample = set(range(0, len(idxs), 997))
        todo = sorted(set(special.tolist()) | sample)
        ncross += int(cross.sum())
        for k in todo:
            y = int(yv[k]); nver += 1
            Wit = None
            for ci, c in enumerate(S8):
                T = c + (x, y)
                if ap_free(T): Wit = T; break
            if Wit is None:
                nfallback += 1
                for T in itertools.combinations(A + [x, y], 10):
                    if ap_free(T): Wit = T; break
            if Wit is None or len(Wit) != 10 or len(set(Wit)) != 10 or not ap_free(Wit) or not sidon(Wit) or not set(Wit) <= AS | {x, y}:
                nfail += 1; nfail_pairs.append((x / 2, y / 2))
        # consistency: mask says witness but explicit search must agree on has & ~cross (sampled above); bad handled above
    return {'class': idx, 'set': A0, 'window_doubled': [lo, hi], 'window': [lo / 2, hi / 2], 'span_div': div,
            'n_S8': nS8, 'valid_singles_all': nsingle_all, 'singles_in_Px': len(singles_Px),
            'singles_in_Px_values_doubled': singles_Px,
            'pairs45': total45, 'cross_ap_pairs': ncross, 'explicit_verified': nver, 'fallbacks': nfallback,
            'failures': nfail, 'secs': round(time.time() - t0, 1)}

def run(a):
    try: os.nice(15)
    except Exception: pass
    return brute(a)

def main():
    div = int(sys.argv[sys.argv.index('--div') + 1]) if '--div' in sys.argv else DIV
    procs = int(sys.argv[sys.argv.index('--procs') + 1]) if '--procs' in sys.argv else 2
    classes = CLASSES
    if '--classes' in sys.argv: classes = [int(c) for c in sys.argv[sys.argv.index('--classes') + 1].split(',')]
    sets = {}
    with gzip.open(os.path.join(ROOT, 'data', 'census_n14_m12_classes.jsonl.gz'), 'rt') as f:
        for i, line in enumerate(f):
            if i in classes: sets[i] = json.loads(line)['set']
    stored = {}
    for line in open(os.path.join(HERE, 'results.jsonl')):
        r = json.loads(line)
        if r['class'] in sets: stored[r['class']] = r
    t0 = time.time()
    res = []
    with Pool(procs) as pool:
        for r in pool.imap_unordered(run, [(i, sets[i], div) for i in classes]):
            res.append(r); print('class', r['class'], 'pairs45', r['pairs45'], 'fail', r['failures'], r['secs'], 's', flush=True)
    res.sort(key=lambda r: r['class'])
    # ---- comparison with L005 (not part of the independent brute force): which of extend_all's candidate singles fall outside the window
    sys.path.insert(0, HERE)
    import extend_all as E
    for r in res:
        A4 = [4 * a for a in r['set']]
        Px4 = sorted(E.candidates(A4))
        A4s = A4
        triples = list(itertools.combinations(A4s, 3))
        ok4 = [x for x in Px4 if all(E.ndist((x,) + q) >= 5 for q in triples)]
        lo, hi = r['window_doubled']
        inside = [x for x in ok4 if x % 2 == 0 and lo <= x // 2 <= hi]
        nonint = [x for x in ok4 if x % 2]
        outside = [x for x in ok4 if x % 2 == 0 and not (lo <= x // 2 <= hi)]
        r['stored_n_single_45'] = stored[r['class']]['n_single_45']
        r['stored_n_t1b_45'] = stored[r['class']]['n_t1b_45']
        r['recomputed_extend_all_singles'] = len(ok4)
        r['singles_inside_window_extend_all'] = len(inside)
        r['singles_noninteger_doubled'] = len(nonint)
        r['singles_outside_window'] = len(outside)
        bf = sorted(r['singles_in_Px_values_doubled'])
        r['singles_match_inside'] = (bf == sorted(x // 2 for x in inside))
        del r['singles_in_Px_values_doubled']
    json.dump({'span_div': div, 'wall_secs': round(time.time() - t0, 1), 'classes': res,
               'total_pairs45': sum(r['pairs45'] for r in res), 'total_failures': sum(r['failures'] for r in res)},
              open(os.path.join(HERE, 'bruteforce_sample_results.json'), 'w'), indent=1)
    print('total pairs45', sum(r['pairs45'] for r in res), 'failures', sum(r['failures'] for r in res), 'wall', time.time() - t0)

if __name__ == '__main__':
    main()
