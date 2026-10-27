"""Theorem 1 of L020: independent verification (referee round 1, opus).
Parses K29 from the certificate text itself, verifies it, then verifies all 45 classes of
experiments/prover/L020/K29_classes.json (data only; no prover code imported)."""
import json, re, sys, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L020-round1-opus')
import hg

CERT = '/home/user/Erdos-757/results/proofs/L020-joint-induction-i11.md'
CLS = '/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'


def parse_k29():
    txt = open(CERT).read()
    i = txt.index('K_{29}=')
    a = txt.index('$$', i)            # closes the first display
    b = txt.index('$$', a + 2)        # opens the second display
    j = txt.index('$$', b + 2)        # closes the second display
    chunk = txt[i:j]
    es = re.findall(r'\\\{(\d+),(\d+),(\d+)\\\}', chunk)
    return [tuple(int(a) for a in e) for e in es]


def full_check(n, edges, label, exhaustive_p3=True, cpsat=True):
    t0 = time.time()
    r = {}
    r['n_vertices_used'] = len(hg.vertex_set(edges))
    r['vertices_are_0..n-1'] = hg.vertex_set(edges) == set(range(n))
    r['3uniform_distinct'] = hg.is_3uniform(edges)
    r['linear'] = hg.is_linear(edges)
    r['F7_copies'] = len(hg.f7_copies(edges, both=True))
    if exhaustive_p3:
        mn, k = hg.p3_exhaustive_min(edges)
        r['P3_exhaustive_min(|U|-|E|)'] = mn
    r['P3_hall_kuhn'] = hg.p3_hall(n, edges)
    r['connected'] = hg.is_connected(n, edges)
    d = hg.degrees(n, edges)
    r['maxdeg'] = max(d)
    r['deg_hist'] = {k: d.count(k) for k in sorted(set(d))}
    t_bb = hg.tau_bb(edges)
    r['tau_bb'] = t_bb
    if cpsat:
        t_cp, T = hg.tau_cpsat(n, edges)
        r['tau_cpsat'] = t_cp
        # explicit transversal check
        assert all(any(x in T for x in e) for e in edges)
        r['cpsat_infeasible_11'] = hg.cpsat_no_transversal_of_size(n, edges, t_bb - 1)
    r['no_transversal_of_size_tau-1(own B&B)'] = not hg.has_transversal_of_size(edges, t_bb - 1)
    r['m'] = len(edges)
    r['slack'] = hg.slack(n, len(edges), t_bb)
    r['secs'] = round(time.time() - t0, 2)
    return r


if __name__ == '__main__':
    K = parse_k29()
    print('K29 parsed from certificate:', len(K), 'edges')
    print(K)
    r = full_check(29, K, 'K29')
    print('K29:', r)
    cls = json.load(open(CLS))
    print('classes in file:', len(cls))
    same = [i for i, c in enumerate(cls) if set(frozenset(e) for e in c['edges']) == set(frozenset(e) for e in K)]
    print('K29 (certificate text) equals class index(es):', same)
    allok = True
    hist = {}
    for i, c in enumerate(cls):
        es = [tuple(e) for e in c['edges']]
        r = full_check(c['n'], es, i, exhaustive_p3=True, cpsat=True)
        ok = (r['vertices_are_0..n-1'] and r['3uniform_distinct'] and r['linear'] and r['F7_copies'] == 0
              and r['P3_exhaustive_min(|U|-|E|)'] >= 2 and r['P3_hall_kuhn'] and r['connected']
              and r['maxdeg'] == 3 and r['tau_bb'] == 12 and r['tau_cpsat'] == 12 and r['cpsat_infeasible_11']
              and r['no_transversal_of_size_tau-1(own B&B)'] and r['m'] == 23 and c['n'] == 29 and r['slack'] == 1)
        allok &= ok
        key = str(r['deg_hist'])
        hist[key] = hist.get(key, 0) + 1
        print(i, 'OK' if ok else 'FAIL', r, flush=True)
    print('ALL 45 OK' if allok else 'SOME FAILED', hist)
