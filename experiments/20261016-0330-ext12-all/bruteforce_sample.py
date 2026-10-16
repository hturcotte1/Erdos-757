"""Brute-force cross-check of extend12_all.py on a few classes.
Plain integer enumeration (coordinates x4, the same scale as extend12_all) of ALL pairs x<y of integers in the window
[min - span/DIV, max + span/DIV] not in A, with the (4,5) property tested from scratch; new 3-APs of B=A u {x,y} found
directly.  Compared with extend12_all's T1b (4,5) pair set (restricted to the window) and single (4,5) set.
Usage: python3 bruteforce_sample.py CLASS_INDEX,CLASS_INDEX,...  (indices into realized_n12.json.gz) or 'known'."""
import gzip, itertools, json, os, sys, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
import extend12_all as E

def nd(q): return len({abs(u - v) for u, v in itertools.combinations(q, 2)})

def brute(idx, A0, DIV=int(os.environ.get("DIV", "1"))):
    t0 = time.time()
    A = sorted(4 * a for a in A0); AS = set(A); n = len(A)
    lo = A[0] - (A[-1] - A[0]) // DIV; hi = A[-1] + (A[-1] - A[0]) // DIV
    tri = list(itertools.combinations(A, 3)); prs = list(itertools.combinations(A, 2))
    Px = set()
    for a, b in prs:
        if (a + b) % 2 == 0: Px.add((a + b) // 2)
        Px.add(2 * a - b); Px.add(2 * b - a)
    Px -= AS
    valid = [v for v in range(lo, hi + 1) if v not in AS and all(nd((v,) + t) >= 5 for t in tri)]
    singles_Px = [v for v in valid if v in Px]
    def inap(B, p):   # is p in some 3-AP of set B
        for q in B:
            if q == p: continue
            if 2 * p - q in B or 2 * q - p in B: return True
            if (p + q) % 2 == 0 and (p + q) // 2 in B: return True
        return False
    BS = AS
    t1b = set(); n45 = 0; t2like = []
    for i, x in enumerate(valid):
        for y in valid[i + 1:]:
            if all(nd((x, y) + q) >= 5 for q in prs):
                n45 += 1
                Bset = BS | {x, y}
                xin, yin = x in Px, y in Px
                if xin or yin:
                    # T1b iff the other point lies in some 3-AP of B
                    other = y if xin else x
                    # careful: if both in Px then both have new APs
                    if (xin and yin) or inap(Bset, other): t1b.add(frozenset((x, y)))
                    elif xin and not yin: pass
                else:
                    if inap(Bset, x) or inap(Bset, y): t2like.append((x, y))
    # compare with extend12_all
    r = E.process((idx, A0), want_pairs=True)
    Et = {p for p in r['_t1b'] if all(lo <= v <= hi for v in p)}
    outside = len(r['_t1b']) - len(Et)
    okx = sorted(v for v in r['_Px_ok'] if lo <= v <= hi)
    # T2-like pairs: h check on sample (exact alpha target 9)
    rnd = random.Random(1); samp = rnd.sample(t2like, min(2000, len(t2like)))
    minh = 99
    for x, y in samp:
        B = sorted(A + [x, y]); minh = min(minh, E.h_exact_B(B, 9))
    # for T1b brute pairs too (all)
    minh1 = min((E.h_exact_B(sorted(A + list(p)), 9) for p in t1b), default=99)
    return {'class': idx, 'span': A[-1] - A[0], 'window': [lo, hi], 'valid_singles': len(valid), 'singles_in_Px_brute': len(singles_Px),
            'singles_in_Px_extend_in_window': len(okx), 'singles_match': sorted(singles_Px) == okx,
            'pairs45_brute': n45, 't1b_brute': len(t1b), 't1b_extend_in_window': len(Et), 't1b_extend_outside_window': outside,
            't1b_match': t1b == Et, 't2like_pairs_brute': len(t2like), 't2like_sample_min_h': minh, 't1b_brute_min_h': minh1,
            'extend_n_t1b_45': r['n_t1b_45'], 'secs': round(time.time() - t0, 1)}

if __name__ == '__main__':
    d = json.load(gzip.open(os.path.join(ROOT, 'experiments/20261014-1005-census-dfs/results/realized_n12.json.gz')))
    out = []
    if sys.argv[1] == 'known':
        k = json.load(open(os.path.join(ROOT, 'data/small_records.json')))['sets']
        items = [(name, k[name]['set']) for name in ('12', '12b', '12c')]
    else:
        items = [(int(i), d[int(i)]['set']) for i in sys.argv[1].split(',')]
    for idx, s in items:
        r = brute(idx, s); out.append(r); print(json.dumps(r), flush=True)
    json.dump(out, open(os.path.join(HERE, 'bruteforce_sample_results_%s.json' % ('known' if sys.argv[1]=='known' else 'random')), 'w'), indent=1)
