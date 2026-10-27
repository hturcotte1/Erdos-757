"""L020: iterate the pattern-(e) gluing.  Input: a JSON list of graphs (keys n, edges) or a cell file; for each graph
compute all role_e configurations (e; a,b) among vertices of degree <= 2 ({a,e},{b,e} not co-transversal, a,b not in a
common edge), then glue with every role_e configuration (f; c,d) of the (8,5,3) graphs (or of a second list) by a new
vertex v with edges {v,a,b},{v,c,d},{v,e,f}; keep the results that lie in C, have Delta <= 3 and tau = tau1 + tau2 + 1.
Usage: python3 iterate_e.py <input.json|cell> <partner cellfile|json> <out.json> [maxgraphs]"""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp
from roles import read_any, in_C
from pattern_e_build import role_e_configs

def load(p):
    if p.endswith('.json'):
        return [(d['n'], [tuple(e) for e in d['edges']]) for d in json.load(open(p))]
    return [(n, es) for (n, es) in read_any(p) if max(hyp.degrees(n, es)) <= 3]

def main(inp, partner, out, lim=None):
    A = load(inp); B = load(partner)
    if lim: A = A[:lim]
    Bc = []
    for (nb, eb) in B:
        cfg, tb = role_e_configs(nb, eb)
        if cfg: Bc.append((nb, eb, tb, cfg))
    print('partner graphs with role_e:', len(Bc), flush=True)
    res = []; withcfg = 0
    for ia, (na, ea) in enumerate(A):
        cfg, ta = role_e_configs(na, ea)
        sa = 3 * na + 2 * len(ea) - 11 * ta
        if cfg: withcfg += 1
        print('graph', ia, (na, len(ea), ta, 'slack', sa), 'role_e configs', len(cfg), flush=True)
        for (e, a, b) in cfg:
            for (nb, eb, tb, cb) in Bc:
                for (f, c, d) in cb:
                    off = na; v = na + nb; n = na + nb + 1
                    E = list(ea) + [tuple(off + y for y in g) for g in eb] + [(v, a, b), (v, off + c, off + d), (v, e, off + f)]
                    if max(hyp.degrees(n, E)) > 3 or not in_C(n, E): continue
                    t = hyp.tau(n, E)
                    if t == ta + tb + 1:
                        res.append(dict(n=n, m=len(E), tau=t, slack=3 * n + 2 * len(E) - 11 * t, edges=E, src=(ia, (e, a, b), (f, c, d))))
    print('inputs with role_e:', withcfg, 'of', len(A), '; glued graphs in C, Delta<=3, tau-raising:', len(res), flush=True)
    if res: print('slacks:', sorted(set(r['slack'] for r in res)), 'n:', sorted(set(r['n'] for r in res)))
    json.dump(res, open(out, 'w'))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else None)
