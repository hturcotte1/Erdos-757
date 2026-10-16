"""Referee L005, Route C: independent re-implementation of the T0/T1a/T1b/T2 case analysis, plain integers.
Imports nothing from e757/, judge/ or the authors' experiment directory.

Differences from the authors' extend_all.py:
  * h is never computed from the 3-AP hypergraph. With H = h(A) and M = all maximum Sidon subsets of A
    (DFS on the difference definition), h(A u {x}) = H+1 iff S u {x} is Sidon for some S in M, and
    h(A u {x,y}) = H+2 iff S u {x,y} is Sidon for some S in M (sums test); otherwise h is computed by a full
    DFS on the extended set (difference definition).
  * the set is scaled by 12 (every candidate and every line intersection is then an integer; asserted).
  * T2 line intersections are computed in closed form per pair of roles.
Outputs per class the authors' counters (Px_size, n_single_45, t1_pairs, n_t1b_45, t2_isect_pts, t2_isect_45,
n_max_sidon) for comparison with results.jsonl, and every deficient item (h < H+2) found, by sub-case.

usage: python3 cases.py CENSUS.jsonl.gz OUT.jsonl --classes i,j,.. [--drop k]   (--drop k: remove the k-th
       smallest point of each set first, positive-control mode on 13-point sets)
"""
import sys, json, gzip, itertools, time, os

SCALE = 12


def ndist(q):
    return len({abs(u - v) for u, v in itertools.combinations(q, 2)})


def is_sidon_sums(S):
    S = sorted(S)
    sums = [S[i] + S[j] for i in range(len(S)) for j in range(i, len(S))]
    return len(sums) == len(set(sums))


def max_sidon_all(P):
    n = len(P)
    best = [0, []]

    def rec(i, chosen, diffs):
        if len(chosen) + (n - i) < best[0]:
            return
        if i == n:
            k = len(chosen)
            if k > best[0]:
                best[0] = k
                best[1] = [tuple(chosen)]
            elif k == best[0]:
                best[1].append(tuple(chosen))
            return
        a = P[i]
        nd = [a - c for c in chosen]
        if not any(d in diffs for d in nd):
            rec(i + 1, chosen + [a], diffs | set(nd))
        rec(i + 1, chosen, diffs)

    rec(0, [], frozenset())
    return best[0], best[1]


def ap_partners(P):
    """all reals forming a 3-AP with two distinct points of P (midpoint or endpoint), as integers (asserted)"""
    out = set()
    for a, b in itertools.combinations(P, 2):
        assert (a + b) % 2 == 0
        out.add((a + b) // 2)
        out.add(2 * a - b)
        out.add(2 * b - a)
    return out - set(P)


def run_class(P0, label, drop=None):
    t0 = time.time()
    A = sorted(SCALE * v for v in P0)
    if drop is not None:
        A = [v for i, v in enumerate(A) if i != drop]
    n = len(A)
    Aset = set(A)
    assert all(ndist(q) >= 5 for q in itertools.combinations(A, 4))
    H, M = max_sidon_all(A)
    target = H + 2
    triples = list(itertools.combinations(A, 3))
    pairs = list(itertools.combinations(A, 2))
    c1 = {}

    def single45(v):
        r = c1.get(v)
        if r is None:
            r = all(ndist((v,) + q) >= 5 for q in triples)
            c1[v] = r
        return r

    def pair45(x, y):
        return all(ndist((x, y) + q) >= 5 for q in pairs)

    def h_ext(extra):
        """h(A u extra) given that A u extra is a (4,5)-set... (only Sidon facts are used)"""
        k = len(extra)
        for S in M:
            if is_sidon_sums(list(S) + list(extra)):
                return H + k
        hh, _ = max_sidon_all(sorted(A + list(extra)))
        return hh

    out = {'class': label, 'n': n, 'hA': H, 'n_max_sidon': len(M)}
    Px = sorted(ap_partners(A))
    Px_ok = [x for x in Px if single45(x)]
    out['Px_size'] = len(Px)
    out['n_single_45'] = len(Px_ok)
    # T1a
    t1a_def = []
    for x in Px_ok:
        hx = h_ext([x])
        if hx + 1 < target:
            t1a_def.append([x, hx])
    out['t1a_deficient'] = t1a_def
    # T1b
    seen = set()
    n45 = 0
    t1b_def = []
    hist = {}
    for x in Px_ok:
        for y in sorted(ap_partners(A + [x])):
            key = (x, y) if x < y else (y, x)
            if key in seen:
                continue
            seen.add(key)
            if not single45(y) or not pair45(x, y):
                continue
            n45 += 1
            hb = h_ext([x, y])
            hist[hb] = hist.get(hb, 0) + 1
            if hb < target:
                t1b_def.append([key[0], key[1], hb])
    out['t1_pairs'] = len(seen)
    out['n_t1b_45'] = n45
    out['t1b_hist'] = {str(k): v for k, v in sorted(hist.items())}
    out['t1b_deficient'] = t1b_def
    # T2 generic: h = H+2 iff some maximum Sidon set avoids a
    univ = set(A)
    for S in M:
        univ &= set(S)
    out['universal'] = sorted(univ)
    # T2 intersections: lines in the (x,y) plane: xm(a): y = 2x - a ; ym(a): 2y = x + a ; am(a): x + y = 2a
    pts = set()
    for a in A:
        for b in A:
            cands = []
            # xm(a) & ym(b): y = 2x - a, 2y = x + b -> 3x = 2a + b
            cands.append((2 * a + b, 3, 'xy'))
            # xm(a) & am(b): 2x - a = 2b - x -> 3x = a + 2b
            cands.append((a + 2 * b, 3, 'xa'))
            # ym(a) & am(b): (x + a)/2 = 2b - x -> 3x = 4b - a
            cands.append((4 * b - a, 3, 'ya'))
            for num, den, kind in cands:
                assert num % den == 0
                x = num // den
                if kind == 'xy' or kind == 'xa':
                    y = 2 * x - a
                else:
                    y = 2 * b - x
                pts.add((x, y))
    # same-role pairs are parallel; also consistency check of the closed forms
    t2pts = [(x, y) for (x, y) in pts if x != y and x not in Aset and y not in Aset]
    t2_45 = []
    for x, y in t2pts:
        if single45(x) and single45(y) and pair45(x, y):
            t2_45.append((x, y, h_ext([x, y])))
    out['t2_isect_pts'] = len(t2pts)
    out['t2_isect_45'] = len(t2_45)
    out['t2_isect_def'] = [list(t) for t in t2_45 if t[2] < target]
    out['secs'] = round(time.time() - t0, 2)
    return out


def main():
    path, outp = sys.argv[1], sys.argv[2]
    try:
        os.nice(15)
    except Exception:
        pass
    sets = [json.loads(l)['set'] for l in gzip.open(path, 'rt') if l.strip()]
    if '--classes' in sys.argv:
        cl = [int(v) for v in sys.argv[sys.argv.index('--classes') + 1].split(',')]
    else:
        a, b = sys.argv[sys.argv.index('--range') + 1].split(':')
        cl = list(range(int(a), min(int(b), len(sets))))
    drop = int(sys.argv[sys.argv.index('--drop') + 1]) if '--drop' in sys.argv else None
    done = set()
    if os.path.exists(outp) and drop is None:
        for l in open(outp):
            try:
                done.add(json.loads(l)['class'])
            except Exception:
                pass
    with open(outp, 'a') as fo:
        for i in cl:
            if i in done:
                continue
            r = run_class(sets[i], i, drop)
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print(i, {k: r[k] for k in ('Px_size', 'n_single_45', 't1_pairs', 'n_t1b_45', 't2_isect_pts',
                                         't2_isect_45', 'n_max_sidon', 'secs')},
                  'def:', len(r['t1a_deficient']), len(r['t1b_deficient']), len(r['universal']),
                  len(r['t2_isect_def']), flush=True)


if __name__ == '__main__':
    main()
