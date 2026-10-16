"""Referee L006: full-census pass with own code (Sidon definition; no e757 / authors' code).
Per class: (4,5) (all 495 4-subsets), h(A)=7 (no Sidon 8-subset, some Sidon 7-subset), number of maximum Sidon subsets
(compared with stored n_max_sidon), m = number of 3-APs (=10 expected), every point avoided by some maximum Sidon subset
(=> alpha(H(A)+{a,x,y}) = 9 for every a, i.e. every T2 line is non-deficient)."""
import gzip, json, itertools, sys, time
from multiprocessing import Pool
CENSUS = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'
ROWS = '/home/user/Erdos-757/data/ext12_all_rows.jsonl.gz'
def is_sidon(S):
    seen = set(); n = len(S)
    for i in range(n):
        for j in range(i, n):
            s = S[i] + S[j]
            if s in seen: return False
            seen.add(s)
    return True
def nd(Q): return len({abs(u - v) for u, v in itertools.combinations(Q, 2)})
def work(item):
    c, A = item
    A = sorted(A)
    ok45 = all(nd(Q) >= 5 for Q in itertools.combinations(A, 4))
    no8 = not any(is_sidon(S) for S in itertools.combinations(A, 8))
    Ts = [T for T in itertools.combinations(A, 7) if is_sidon(T)]
    AS = set(A)
    aps = [(u, (u + v) // 2, v) for u, v in itertools.combinations(A, 2) if (u + v) % 2 == 0 and (u + v) // 2 in AS]
    m = len(aps)
    mindeg = min(sum(1 for t in aps if a in t) for a in A)
    avoid = all(any(a not in T for T in Ts) for a in A)
    return c, ok45, no8, len(Ts), m, avoid, mindeg
if __name__ == '__main__':
    cen = json.load(gzip.open(CENSUS, 'rt'))
    rows = {r['class']: r for r in (json.loads(l) for l in gzip.open(ROWS, 'rt'))}
    t0 = time.time(); bad = []; ms = {}; cnt = 0; md = {}
    with Pool(3) as pool:
        for c, ok45, no8, nT, m, avoid, mindeg in pool.imap_unordered(work, enumerate(r['set'] for r in cen), chunksize=64):
            cnt += 1; ms[m] = ms.get(m, 0) + 1; md[mindeg] = md.get(mindeg, 0) + 1
            if not (ok45 and no8 and nT > 0 and nT == rows[c]['n_max_sidon'] and m == 10 and avoid and mindeg >= 1):
                bad.append((c, ok45, no8, nT, rows[c]['n_max_sidon'], m, avoid, mindeg))
    print(f'classes {cnt}; failures {len(bad)} {bad[:10]}; m histogram {ms}; min-degree histogram {md}; {time.time() - t0:.0f}s')
