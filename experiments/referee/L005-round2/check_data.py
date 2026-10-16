"""Referee round 2 for L005: independent integrity check of the census and of results.jsonl.
Imports nothing from e757/, judge/ or the authors' experiment folder.
Per census line: 14 distinct ints, (4,5) on all 1001 4-subsets, the 3-APs (count = 12, saturated, equal to stored
edges), h(A) = 8 by a DFS on the DIFFERENCE definition of Sidon (no 3-AP reduction), all maximum Sidon sets,
their common intersection (core), affine normal forms (distinct classes).
Then compare against results.jsonl: set, hA, n_max_sidon, in_all_max_sidon, and the textual numbers of the proof.
Usage: python3 check_data.py CENSUS.jsonl.gz RESULTS.jsonl OUT.json
"""
import gzip, itertools, json, sys
from math import gcd
from functools import reduce


def is45(P):
    for q in itertools.combinations(P, 4):
        if len({abs(u - v) for u, v in itertools.combinations(q, 2)}) < 5:
            return False
    return True


def aps(P):
    S = set(P); out = []
    for a, c in itertools.combinations(sorted(P), 2):
        if (a + c) % 2 == 0 and (a + c) // 2 in S:
            out.append((a, (a + c) // 2, c))
    return out


def sidon_dfs(P):
    """all maximum Sidon subsets of P, by DFS on distinct positive differences."""
    P = sorted(P); n = len(P)
    best = [0]; sets = []
    def rec(i, chosen, diffs):
        # bound
        if len(chosen) + (n - i) < best[0]:
            return
        if i == n:
            if len(chosen) > best[0]:
                best[0] = len(chosen); sets.clear()
            if len(chosen) == best[0]:
                sets.append(tuple(chosen))
            return
        v = P[i]
        nd = [v - c for c in chosen]
        if len(set(nd)) == len(nd) and not (set(nd) & diffs):
            rec(i + 1, chosen + [v], diffs | set(nd))
        rec(i + 1, chosen, diffs)
    rec(0, [], frozenset())
    return best[0], sets


def normal_form(P):
    P = sorted(P); m0 = P[0]
    Q = [p - m0 for p in P]
    g = reduce(gcd, Q[1:])
    Q = tuple(q // g for q in Q)
    R = tuple(sorted(Q[-1] - q for q in Q))
    return min(Q, R)


def main():
    census, resjl, outp = sys.argv[1:4]
    rows = {}
    for line in open(resjl):
        r = json.loads(line); rows[r['class']] = r
    out = {'bad': [], 'n': 0}
    nfs = set(); nmax = []; cores = 0; mism = []
    with gzip.open(census, 'rt') as f:
        for idx, line in enumerate(f):
            d = json.loads(line); A = d['set']
            out['n'] += 1
            ok = (len(A) == 14 and all(isinstance(a, int) for a in A) and len(set(A)) == 14)
            if not ok:
                out['bad'].append((idx, 'pts')); continue
            if not is45(A): out['bad'].append((idx, 'not45'))
            ap = aps(A)
            mids = {b for _, b, _ in ap}
            As = sorted(A)
            if len(ap) != 12 or mids != set(As[1:-1]):
                out['bad'].append((idx, 'ap/sat', len(ap)))
            st_edges = sorted(tuple(sorted(e)) for e in d['edges'])
            my_edges = sorted(tuple(sorted((As.index(a), As.index(b), As.index(c)))) for a, b, c in ap)
            if st_edges != my_edges: out['bad'].append((idx, 'edges'))
            h, M = sidon_dfs(A)
            if h != 8: out['bad'].append((idx, 'h', h))
            core = set(As)
            for S in M: core &= set(S)
            if core: cores += 1
            nmax.append(len(M))
            nfs.add(normal_form(A))
            r = rows.get(idx)
            if r is None or r['set'] != A or r['hA'] != h or r['n_max_sidon'] != len(M) or sorted(r['in_all_max_sidon']) != sorted(core):
                mism.append(idx)
    out['distinct_normal_forms'] = len(nfs)
    out['n_max_sidon_range'] = [min(nmax), max(nmax)]
    out['n_max_sidon_sum'] = sum(nmax)
    out['classes_with_nonempty_core'] = cores
    out['mismatch_with_results_jsonl'] = mism
    out['abase_index'] = None
    with gzip.open(census, 'rt') as f:
        for idx, line in enumerate(f):
            if json.loads(line)['set'] == [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]:
                out['abase_index'] = idx
    # textual numbers of the proof, recomputed from results.jsonl
    R = [rows[k] for k in sorted(rows)]
    out['rows'] = len(R)
    out['classes_ids_ok'] = sorted(rows) == list(range(2910))
    out['single_range'] = [min(r['n_single_45'] for r in R), max(r['n_single_45'] for r in R)]
    out['single_sum'] = sum(r['n_single_45'] for r in R)
    out['t1b45_sum'] = sum(r['n_t1b_45'] for r in R)
    out['t1b45_range'] = [min(r['n_t1b_45'] for r in R), max(r['n_t1b_45'] for r in R)]
    out['t1pairs_sum'] = sum(r['t1_pairs'] for r in R)
    out['n2ext_sum'] = sum(r['n_2ext'] for r in R)
    out['isect_range'] = [min(r['t2_isect_pts'] for r in R), max(r['t2_isect_pts'] for r in R)]
    out['isect_sum'] = sum(r['t2_isect_pts'] for r in R)
    out['isect45_sum'] = sum(r['t2_isect_45'] for r in R)
    out['lines_sum'] = sum(r['t2_lines'] for r in R)
    out['line_h_values'] = sorted({h for r in R for h in r['t2_line_h']})
    out['min_h_values'] = sorted({r['min_h'] for r in R})
    out['records_total'] = sum(len(r['records']) for r in R)
    out['hA_values'] = sorted({r['hA'] for r in R})
    out['precheck_true'] = sum(1 for r in R if r['t2_precheck'])
    # histogram consistency: hist total == singles + t1b45 + isect45 + 42
    out['hist_consistency_fail'] = [r['class'] for r in R if sum(r['hist'].values()) != r['n_single_45'] + r['n_t1b_45'] + r['t2_isect_45'] + r['t2_lines'] or set(r['hist']) != {'10'}]
    json.dump(out, open(outp, 'w'), indent=1)
    print(json.dumps(out))


if __name__ == '__main__':
    main()
