"""Referee round 2 for L005: own T1 enumeration (counters compared with results.jsonl) and pure-definition brute force h(B)
(all 10-subsets / all 11-subsets of B checked for distinct differences; no 3-AP reduction, no reduction to Sidon sets of A)
on a random sample of (4,5) T1b pairs; writes judge claim files for a few of them.
Imports nothing from e757/, judge/, the authors' folder or the round-1 referee folder.
Usage: python3 t1_brute.py CENSUS RESULTS.jsonl OUT.jsonl CLAIMDIR SAMPLE_PER_CLASS IDX [IDX ...]
"""
import gzip, itertools, json, os, random, sys, time


def nd(q):
    return len({abs(u - v) for u, v in itertools.combinations(q, 2)})


def is_sidon(T):
    d = [abs(u - v) for u, v in itertools.combinations(T, 2)]
    return len(d) == len(set(d))


def completions(P):
    """reals not in P forming a 3-AP with two points of P (P scaled so that all are integers)."""
    out = set()
    for a, b in itertools.combinations(P, 2):
        assert (a + b) % 2 == 0
        out.update(((a + b) // 2, 2 * a - b, 2 * b - a))
    return out - set(P)


def h_pure(B):
    """exact h by the definition: largest k with a Sidon k-subset (scan downward from 11)."""
    for k in (11, 10, 9):
        for T in itertools.combinations(B, k):
            if is_sidon(T):
                return k, T
    raise RuntimeError


def main():
    census, resjl, outp, claimdir, nsamp = sys.argv[1:6]
    nsamp = int(nsamp); idxs = [int(a) for a in sys.argv[6:]]
    sets = [json.loads(l)['set'] for l in gzip.open(census, 'rt')]
    rows = {}
    for l in open(resjl):
        r = json.loads(l); rows[r['class']] = r
    os.makedirs(claimdir, exist_ok=True)
    fo = open(outp, 'a')
    for idx in idxs:
        t0 = time.time()
        A = sorted(4 * a for a in sets[idx])
        tri = list(itertools.combinations(A, 3)); duo = list(itertools.combinations(A, 2))
        cache = {}
        def sok(v):
            if v not in cache:
                cache[v] = all(nd((v,) + q) >= 5 for q in tri)
            return cache[v]
        Px = sorted(completions(A))
        X = [x for x in Px if sok(x)]
        seen = set(); pairs45 = []; npairs = 0
        for x in X:
            for y in sorted(completions(sorted(A + [x]))):
                k = frozenset((x, y))
                if k in seen:
                    continue
                seen.add(k); npairs += 1
                if sok(y) and all(nd((x, y) + q) >= 5 for q in duo):
                    pairs45.append((x, y))
        st = rows[idx]
        cmp = {'Px_size': (len(Px), st['Px_size']), 'n_single_45': (len(X), st['n_single_45']),
               't1_pairs': (npairs, st['t1_pairs']), 'n_t1b_45': (len(pairs45), st['n_t1b_45'])}
        rng = random.Random(77 + idx)
        samp = rng.sample(pairs45, min(nsamp, len(pairs45)))
        hs = {}
        for j, (x, y) in enumerate(samp):
            B = sorted(A + [x, y])
            h, T = h_pure(B)
            hs[h] = hs.get(h, 0) + 1
            if j < 2:
                g = 4
                Bs = [b for b in B]  # integers at scale 4
                json.dump({'id': f'REF2-L005-c{idx}-{j}', 'type': 'construction', 'set': Bs, 'claimed_h': h,
                           'notes': f'referee round 2 L005 spot check: class {idx} scaled by 4 plus T1b pair ({x},{y})'},
                          open(os.path.join(claimdir, f'REF2-L005-c{idx}-{j}.json'), 'w'))
        r = {'class': idx, 'counters_mine_vs_stored': cmp, 'counters_equal': all(a == b for a, b in cmp.values()),
             'sample': len(samp), 'h_hist_pure': hs, 'secs': round(time.time() - t0, 1)}
        fo.write(json.dumps(r) + '\n'); fo.flush(); print(json.dumps(r), flush=True)


if __name__ == '__main__':
    main()
