"""Referee L005, step D: integrity of the input census and of the authors' output files.
Plain Python; imports nothing from e757/, judge/ or the authors' experiment directory.

usage: python3 check_data.py CENSUS.jsonl.gz RESULTS.jsonl RESULTS.json L004_REFEREE_REALIZABLE.txt.gz OUT.json

Checks, per census line:
  * 14 distinct integers, (4,5) by brute force over all 1001 4-subsets,
  * the 3-term APs (computed from the values) are exactly the stored 'edges', there are 12 of them,
    every non-extreme point is a midpoint (saturated),
  * h(A) = 8 by a DFS over Sidon subsets using the DIFFERENCE definition (no 3-AP hypergraph),
    with the list of all maximum Sidon subsets, their number and their common intersection;
  * affine normal form (translation, positive and negative scaling); all 2,910 distinct;
  * the same 2,910 normal forms as the L004 referee's own independent realization (my_realizable.txt.gz).
Per results row: same set as the census line, hA = 8, min_h = 10, no records, t2_line_h = [10], 42 lines,
  t2_isect_45 = 0, n_2ext = n_t1b_45 + t2_isect_45, hist only {10}; totals; ranges.
"""
import sys, json, gzip, itertools
from math import gcd
from functools import reduce


def is45(P):
    for q in itertools.combinations(P, 4):
        if len({abs(u - v) for u, v in itertools.combinations(q, 2)}) < 5:
            return False
    return True


def three_aps(P):
    s = set(P)
    idx = {v: i for i, v in enumerate(P)}
    out = []
    for i, j in itertools.combinations(range(len(P)), 2):
        t = P[i] + P[j]
        if t % 2 == 0 and t // 2 in s:
            out.append(tuple(sorted((i, idx[t // 2], j))))
    return sorted(out)


def sidon_max_all(P):
    """all maximum Sidon subsets of P (sorted list of distinct numbers), difference definition."""
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


def is_sidon_sums(S):
    sums = [S[i] + S[j] for i in range(len(S)) for j in range(i, len(S))]
    return len(sums) == len(set(sums))


def normal_form(P):
    def nf(Q):
        Q = sorted(Q)
        m = Q[0]
        Q = [q - m for q in Q]
        g = reduce(gcd, Q)
        return tuple(q // g for q in Q)
    a = nf(P)
    b = nf([-p for p in P])
    return min(a, b)


def main():
    census, rjl, rjs, l4, outp = sys.argv[1:6]
    sets = []
    for line in gzip.open(census, 'rt'):
        if line.strip():
            sets.append(json.loads(line))
    rep = {'n_census_lines': len(sets)}
    bad = []
    nf_list = []
    nmax = []
    universal = 0
    for i, rec in enumerate(sets):
        P = rec['set']
        ok = (len(P) == 14 and len(set(P)) == 14 and P == sorted(P) and all(isinstance(v, int) for v in P))
        ok = ok and rec.get('n') == 14 and rec.get('m') == 12 and rec.get('h') == 8
        ok = ok and is45(P)
        aps = three_aps(P)
        ok = ok and len(aps) == 12 and aps == sorted(tuple(sorted(e)) for e in rec['edges'])
        mids = {e[1] for e in aps}
        ok = ok and mids == set(range(1, 13))
        h, allmax = sidon_max_all(P)
        ok = ok and h == 8 and all(is_sidon_sums(list(S)) for S in allmax)
        # no Sidon 9-subset: double check by extension of every maximum one (a Sidon 9-set contains Sidon 8-sets)
        for S in allmax:
            for a in P:
                if a not in S and is_sidon_sums(sorted(S + (a,))):
                    ok = False
        inter = set(P)
        for S in allmax:
            inter &= set(S)
        if inter:
            universal += 1
        nmax.append(len(allmax))
        nf_list.append(normal_form(P))
        if not ok:
            bad.append(i)
    rep['bad_census_lines'] = bad
    rep['classes_with_universal_vertex'] = universal
    rep['n_max_sidon_range'] = [min(nmax), max(nmax)]
    rep['distinct_normal_forms'] = len(set(nf_list))
    abase = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    nfa = normal_form(abase)
    rep['abase_index'] = [i for i, f in enumerate(nf_list) if f == nfa]
    # L004 referee's own realizations
    l4nf = set()
    for line in gzip.open(l4, 'rt'):
        f = line.split('\t')
        if len(f) >= 2:
            l4nf.add(normal_form(list(map(int, f[1].split(',')))))
    rep['l004_referee_normal_forms'] = len(l4nf)
    rep['census_minus_l004ref'] = len(set(nf_list) - l4nf)
    rep['l004ref_minus_census'] = len(l4nf - set(nf_list))
    # authors' results
    rows = [json.loads(l) for l in open(rjl) if l.strip()]
    rep['n_rows_jsonl'] = len(rows)
    cls = [r['class'] for r in rows]
    rep['rows_class_ids_ok'] = sorted(cls) == list(range(len(sets)))
    rowbad = []
    byc = {r['class']: r for r in rows}
    for c, r in byc.items():
        e = []
        if r['set'] != sets[c]['set']: e.append('set')
        if r['hA'] != 8: e.append('hA')
        if r['min_h'] != 10: e.append('min_h')
        if r['records']: e.append('records')
        if r['t2_line_h'] != [10]: e.append('t2_line_h')
        if r['t2_lines'] != 42: e.append('t2_lines')
        if r['t2_isect_45'] != 0: e.append('t2_isect_45')
        if r['n_2ext'] != r['n_t1b_45'] + r['t2_isect_45']: e.append('n_2ext')
        if set(r['hist']) != {'10'}: e.append('hist')
        if r['hist']['10'] != r['n_single_45'] + r['n_t1b_45'] + 42 + r['t2_isect_45']:
            e.append('hist_total')
        if r['t2_precheck'] or r['in_all_max_sidon']: e.append('precheck')
        if r['n_max_sidon'] != nmax[c]: e.append('n_max_sidon_mismatch_with_referee')
        if e:
            rowbad.append((c, e))
    rep['row_problems'] = rowbad[:50]
    rep['n_row_problems'] = len(rowbad)
    for key in ('Px_size', 'n_single_45', 't1_pairs', 'n_t1b_45', 'n_2ext', 'n_max_sidon', 't2_isect_pts'):
        vals = [r[key] for r in rows]
        rep['range_' + key] = [min(vals), max(vals)]
        rep['sum_' + key] = sum(vals)
    from collections import Counter
    rep['hist_t2_isect_pts'] = dict(Counter(r['t2_isect_pts'] for r in rows))
    js = json.load(open(rjs))
    rep['results_json_summary'] = js['summary']
    jsrows = sorted(js['classes'], key=lambda r: r['class'])
    rep['results_json_rows_equal_jsonl'] = jsrows == sorted(rows, key=lambda r: r['class'])
    if rep['abase_index']:
        r = byc[rep['abase_index'][0]]
        rep['abase_row'] = {k: v for k, v in r.items() if k != 'set'}
    json.dump(rep, open(outp, 'w'), indent=1)
    print(json.dumps({k: v for k, v in rep.items() if k not in ('abase_row',)}, indent=None)[:4000])
    if 'abase_row' in rep:
        print('abase_row', rep['abase_row'])


if __name__ == '__main__':
    main()
