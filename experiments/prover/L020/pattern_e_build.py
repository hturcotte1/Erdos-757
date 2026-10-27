"""L020: build every pattern-(e) graph K = F + X + v from a slack-2 graph F (stored list, Delta<=3) with a role_e
configuration (e; a,b) and a slack-1 graph X with a role_e configuration (f; c,d), v joined by {v,a,b},{v,c,d},{v,e,f}.
Checks exactly: K in C (linear, F7-free, (P3) via Hall), Delta(K) <= 3, tau(K) = tau(F)+tau(X)+1, slack(K), connectivity.
Usage: python3 pattern_e_build.py <F-cellfile> <X-cellfile>"""
import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp
from roles import read_any, in_C

def role_e_configs(n, es):
    deg = hyp.degrees(n, es)
    Ts, t = hyp.all_min_transversals(hyp.masks(es))
    A = [x for x in range(n) if deg[x] <= 2]
    cov = [0] * n
    for T in Ts:
        mm = T
        while mm:
            b = mm & -mm; mm ^= b; cov[b.bit_length() - 1] |= T
    share = set()
    for e in es:
        for x, y in itertools.combinations(e, 2): share.add(frozenset((x, y)))
    out = []
    for e in A:
        part = [x for x in A if x != e and not (cov[e] >> x) & 1]
        for a, b in itertools.combinations(part, 2):
            if frozenset((a, b)) not in share: out.append((e, a, b))
    return out, t

def main(fpath, xpath):
    Fs = [(n, es) for (n, es) in read_any(fpath) if max(hyp.degrees(n, es)) <= 3]
    Xs = [(n, es) for (n, es) in read_any(xpath) if max(hyp.degrees(n, es)) <= 3]
    Xc = []
    for (nx, ex) in Xs:
        cfg, tx = role_e_configs(nx, ex)
        if cfg: Xc.append((nx, ex, tx, cfg))
    print('X classes with role_e:', len(Xc), [len(c[3]) for c in Xc], flush=True)
    tot = 0; inC = 0; found = []
    for fi, (nf, ef) in enumerate(Fs):
        cfg, tf = role_e_configs(nf, ef)
        if not cfg: continue
        for (e, a, b) in cfg:
            for (nx, ex, tx, cx) in Xc:
                for (f, c, d) in cx:
                    off = nf; v = nf + nx
                    E = list(ef) + [tuple(off + y for y in g) for g in ex] + [(v, a, b), (v, off + c, off + d), (v, e, off + f)]
                    n = nf + nx + 1
                    tot += 1
                    if max(hyp.degrees(n, E)) > 3: continue
                    if not in_C(n, E): continue
                    inC += 1
                    tK = hyp.tau(n, E)
                    s = 3 * n + 2 * len(E) - 11 * tK
                    if tK == tf + tx + 1:
                        found.append((fi, (e, a, b), (f, c, d), n, len(E), tK, s, E))
        print('F class', fi, 'configs', len(cfg), 'running: built', tot, 'inC&Delta<=3', inC, 'tau-raising', len(found), flush=True)
    print('TOTAL built', tot, 'in C with Delta<=3', inC, 'tau(K)=tau(F)+tau(X)+1:', len(found))
    for x in found[:5]: print('FOUND', x)
    if found:
        import json
        json.dump([dict(F_index=x[0], role_e_F=x[1], role_e_X=x[2], n=x[3], m=x[4], tau=x[5], slack=x[6], edges=x[7]) for x in found],
                  open('pattern_e_found_%s.json' % fpath.split('/')[-1].replace('.txt', ''), 'w'))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
