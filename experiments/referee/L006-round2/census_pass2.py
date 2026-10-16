"""Referee round 2: (i) all 54,243 census sets: distinct, (4,5), exactly 10 3-APs, h = 7 and every point avoided by some
maximum Sidon subset (all by Sidon definition, own code); (ii) consistency of the L006 consequence on the 2,910 saturated
extremal 14-point classes: every 2-point deletion has h = 8 (some maximum Sidon 8-subset avoids both points)."""
import gzip, json, os, sys, time
from itertools import combinations
from multiprocessing import Pool
ROOT = '/home/user/Erdos-757'

def sidon_sets(vals, size):
    """all subsets of vals of the given size with distinct positive differences"""
    vals = sorted(vals); n = len(vals); out = []
    def rec(i, chosen, used):
        if len(chosen) == size: out.append(tuple(chosen)); return
        for k in range(i, n):
            if len(chosen) + (n - k) < size: return
            v = vals[k]; nd = {v - c for c in chosen}
            if not (nd & used):
                chosen.append(v); rec(k + 1, chosen, used | nd); chosen.pop()
    rec(0, [], frozenset())
    return out

def n_aps(A):
    S = set(A); return sum(1 for a, b in combinations(sorted(A), 2) if (a + b) % 2 == 0 and (a + b) // 2 in S)

def job12(s):
    A = sorted(s)
    ok45 = len(set(A)) == 12 and all(len({abs(u - v) for u, v in combinations(q, 2)}) >= 5 for q in combinations(A, 4))
    s8 = sidon_sets(A, 8); s7 = sidon_sets(A, 7)
    avoided = all(any(a not in T for T in s7) for a in A)
    return ok45, n_aps(A), len(s8) == 0 and len(s7) > 0, len(s7), avoided

def job14(s):
    B = sorted(s)
    s9 = sidon_sets(B, 9); s8 = sidon_sets(B, 8)
    pairs_ok = all(any(u not in T and v not in T for T in s8) for u, v in combinations(B, 2))
    return len(s9) == 0 and len(s8) > 0, pairs_ok, len(s8)

if __name__ == '__main__':
    os.nice(5); t0 = time.time()
    cen = json.load(gzip.open(ROOT + '/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz', 'rt'))
    rows = {r['class']: r for r in (json.loads(l) for l in gzip.open(ROOT + '/data/ext12_all_rows.jsonl.gz', 'rt'))}
    with Pool(2) as pool:
        R = pool.map(job12, [c['set'] for c in cen], chunksize=200)
    print('n=12 census:', len(R), 'classes; (4,5):', sum(r[0] for r in R), '; m=10:', sum(r[1] == 10 for r in R),
          '; h=7:', sum(r[2] for r in R), '; no universal vertex:', sum(r[4] for r in R),
          '; #max Sidon = stored n_max_sidon:', sum(r[3] == rows[i]['n_max_sidon'] for i, r in enumerate(R)), '; %.0fs' % (time.time() - t0))
    c14 = [json.loads(l) for l in gzip.open(ROOT + '/data/census_n14_m12_classes.jsonl.gz', 'rt')]
    key = 'set' if 'set' in c14[0] else list(c14[0].keys())[0]
    with Pool(2) as pool:
        R2 = pool.map(job14, [c[key] for c in c14], chunksize=50)
    print('n=14 saturated census:', len(R2), 'classes; h=8:', sum(r[0] for r in R2), '; all 91 two-point deletions keep h=8:',
          sum(r[1] for r in R2), '; #max Sidon range', min(r[2] for r in R2), max(r[2] for r in R2), '; %.0fs' % (time.time() - t0))
