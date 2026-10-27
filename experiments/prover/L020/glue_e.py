"""L020: pattern-(e) gluing A (+) B: for graphs F in list A and X in list B (Delta<=3), every role_e configuration
(e; a,b) of F and (f; c,d) of X, add v with {v,a,b},{v,c,d},{v,e,f}; keep results in C with Delta<=3 and
tau = tau(F)+tau(X)+1; report their (n,m,tau,slack), iso classes, and role_e configurations of the results.
Usage: python3 glue_e.py <A: cellfile|json> <B: cellfile|json> <out.json> [same]   ('same': A = B, unordered pairs)"""
import sys, json, itertools, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp, networkx as nx
from roles import read_any, in_C
from pattern_e_build import role_e_configs

def load(p):
    if p.endswith('.json'):
        return [(d['n'], [tuple(e) for e in d['edges']]) for d in json.load(open(p))]
    return [(n, es) for (n, es) in read_any(p) if max(hyp.degrees(n, es)) <= 3]

def inc(n, E):
    G = nx.Graph()
    for x in range(n): G.add_node(('v', x), t=0)
    for i, e in enumerate(E):
        G.add_node(('e', i), t=1)
        for x in e: G.add_edge(('e', i), ('v', x))
    return G

def main(pa, pb, out, same=False):
    A = load(pa); B = A if same else load(pb)
    Ac = [(i, n, es) + role_e_configs(n, es) for i, (n, es) in enumerate(A)]
    Ac = [x for x in Ac if x[3]]
    Bc = Ac if same else [x for x in [(i, n, es) + role_e_configs(n, es) for i, (n, es) in enumerate(B)] if x[3]]
    print('A with role_e', len(Ac), 'B with role_e', len(Bc), flush=True)
    reps = []; tried = 0; kept = 0
    for ia, (i, na, ea, ca, ta) in enumerate(Ac):
        for ib, (j, nb, eb, cb, tb) in enumerate(Bc):
            if same and ib < ia: continue
            for (e, a, b) in ca:
                for (f, c, d) in cb:
                    off = na; v = na + nb; n = na + nb + 1
                    E = list(ea) + [tuple(off + y for y in g) for g in eb] + [(v, a, b), (v, off + c, off + d), (v, e, off + f)]
                    tried += 1
                    if max(hyp.degrees(n, E)) > 3 or not in_C(n, E): continue
                    t = hyp.tau(n, E)
                    if t != ta + tb + 1: continue
                    kept += 1
                    G = inc(n, E); h = nx.weisfeiler_lehman_graph_hash(G, node_attr='t', iterations=4)
                    if any(h2 == h and nx.is_isomorphic(G, G2, node_match=lambda x, y: x['t'] == y['t']) for (h2, G2, _) in reps): continue
                    reps.append((h, G, dict(n=n, m=len(E), tau=t, slack=3 * n + 2 * len(E) - 11 * t, edges=E, src=(i, j))))
        print('A graph', ia, 'tried', tried, 'kept', kept, 'classes', len(reps), flush=True)
    res = [r[2] for r in reps]
    rc = collections.Counter()
    for r in res:
        cfg, t = role_e_configs(r['n'], [tuple(e) for e in r['edges']])
        r['role_e'] = len(cfg); rc[len(cfg)] += 1
    print('RESULT cells', collections.Counter((r['n'], r['m'], r['tau'], r['slack']) for r in res), 'role_e histogram', dict(rc), flush=True)
    json.dump(res, open(out, 'w'))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], len(sys.argv) > 4 and sys.argv[4] == 'same')
