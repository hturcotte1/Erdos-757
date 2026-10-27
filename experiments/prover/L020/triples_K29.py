"""L020: triple coverage on the 29-vertex graphs.  For each graph K (JSON list, keys n, edges): all minimum transversals;
for every triple of pairwise disjoint vertex pairs P1,P2,P3, none inside an edge of K (otherwise K+v is not linear), test
whether some minimum transversal meets all three (bit-parallel over the transversal index).  For every uncoverable
triple, test whether H = K + v(P1,P2,P3) lies in C (linear, F7-free, (P3)) and compute tau(H) exactly; an H in C with
tau(H) = tau(K)+1 has slack s(K)-2 = -1 and would violate I11.  Also records pair-pair failures.
Usage: python3 triples_K29.py <json> [first] [last]"""
import sys, json, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L017'); sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L020')
import hyp
from roles import in_C

def run(d):
    n, es = d['n'], [tuple(e) for e in d['edges']]
    Ts, t = hyp.all_min_transversals(hyp.masks(es))
    Vb = [0] * n
    for i, T in enumerate(Ts):
        mm = T
        while mm:
            b = mm & -mm; mm ^= b; Vb[b.bit_length() - 1] |= (1 << i)
    inedge = set()
    for e in es:
        for x, y in itertools.combinations(e, 2): inedge.add((min(x, y), max(x, y)))
    pairs = [(x, y) for x in range(n) for y in range(x + 1, n) if (x, y) not in inedge]
    B = {p: Vb[p[0]] | Vb[p[1]] for p in pairs}
    pp_fail = 0; unc = 0; unc_inC = 0; viol = []
    P = pairs; L = len(P)
    for i in range(L):
        p1 = P[i]; b1 = B[p1]
        for j in range(i + 1, L):
            p2 = P[j]
            if p2[0] in p1 or p2[1] in p1: continue
            b12 = b1 & B[p2]
            if not b12: pp_fail += 1
            for k in range(j + 1, L):
                p3 = P[k]
                if p3[0] in p1 or p3[1] in p1 or p3[0] in p2 or p3[1] in p2: continue
                if b12 & B[p3]: continue
                unc += 1
                v = n; E = es + [(v,) + p1, (v,) + p2, (v,) + p3]
                if in_C(n + 1, E):
                    unc_inC += 1
                    tH = hyp.tau(n + 1, E)
                    if tH == t + 1: viol.append((p1, p2, p3))
    return dict(n=n, m=len(es), tau=t, nT=len(Ts), pairs=L, pp_fail=pp_fail, uncoverable=unc, uncoverable_inC=unc_inC, violators=viol[:5], nviol=len(viol))

if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    a = int(sys.argv[2]) if len(sys.argv) > 2 else 0; b = int(sys.argv[3]) if len(sys.argv) > 3 else len(data)
    tot = 0
    for i in range(a, b):
        r = run(data[i]); tot += r['nviol']
        print(i, json.dumps(r), flush=True)
    print('TOTAL violators', tot)
