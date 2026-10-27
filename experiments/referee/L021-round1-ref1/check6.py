"""Referee #1 (L021): more data (data/): KT (conjecture; falsification attempt) and Theorem 2 (0 <= DEF <= 11(n-m))
on the reader family S_0 (all induced subgraphs), S_1 and S_2 (whole graph and random induced subgraphs) and on all
induced subgraphs of a few random classes of the census of extremal 14-point sets (data/census_n14_m12_classes)."""
import os, sys, json, gzip, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
src4 = open(os.path.join(HERE, 'check4.py')).read().split("rec = json.load")[0]   # function definitions only
exec(src4)
fam = json.load(open('/home/user/Erdos-757/data/reader_5_9_family.json'))['family']
rng = random.Random(5)
def run(name, n, E, subsets):
    em = [sum(1 << v for v in e) for e in E]
    copies = [(sum(1 << v for v in U), W) for (nm, pn, pe, W) in pcs for U in induced_copies(n, E, pn, pe)]
    v2 = vk = 0; minP = None; cnt = 0; ck = 0
    for S in subsets:
        k = bin(S).count('1'); mS = sum(1 for e in em if e & S == e)
        t = tau_bf_mask(em, S) if k <= 16 else tau_ilp(n, [e for e, f in zip(E, em) if f & S == f]) if S == (1 << n) - 1 else None
        if t is None: continue
        D = best_def(em, S, copies) if len(copies) <= 40 else DEF_ilp(n, [e for e, f in zip(E, em) if f & S == f], [(frozenset(v for v in range(n) if (U >> v) & 1), W) for U, W in copies if U & S == U])[0]
        cnt += 1
        if D < 0 or D > 11*(k - mS): v2 += 1
        deg = max([sum(1 for e in em if e & S == e and (e >> v) & 1) for v in range(n) if (S >> v) & 1] or [0])
        if deg <= 3:
            ck += 1; P = A_val(k, mS, t) + D; minP = P if minP is None else min(minP, P); vk += P < 0
    print(f'{name}: n={n} m={len(E)}; subgraphs {cnt}: Thm2 violations {v2}; KT (Delta<=3) tested {ck}: violations {vk}, min P {minP}', flush=True)
for f in fam[:3]:
    A = f['set']; n, E = ap_graph(A); assert in_C(n, E)
    if n <= 12: subs = range(1, 1 << n)
    else: subs = [(1 << n) - 1] + [rng.getrandbits(n) | 1 for _ in range(200)]
    subs = [S for S in subs if bin(S).count('1') <= 16 or S == (1 << n) - 1]
    run('reader S_%d' % f['K'], n, E, subs)
rows = [json.loads(l) for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt')]
print('census classes:', len(rows))
for r in rng.sample(rows, 4):
    E = [tuple(e) for e in r['edges']]; n = r['n']
    assert in_C(n, E) and ap_graph(r['set'])[1] and len(ap_graph(r['set'])[1]) == len(E)
    run('census class set=%s' % r['set'][:4], n, E, range(1, 1 << n))
