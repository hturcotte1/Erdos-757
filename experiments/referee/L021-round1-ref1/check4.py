"""Referee #1 (L021): data tests of Theorem 2 (DEF <= 11(n-m) on C), DEF >= 0 and of KT (P >= 0, a conjecture;
falsification attempt only) on: the record sets of data/small_records.json (A_base, three 12-point sets, n = 8, 10, 11)
and ALL their induced subgraphs; Fibonacci sets {F_3..F_k}; hypertrees with a perfect matching (k = 0..6);
F7 and the sanity numbers.  Own AP-hypergraph builder, own (4,5) check, own tau, own DEF (exhaustive over families)."""
import os, sys, json, itertools, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcore import *
src = json.load(open('/home/user/Erdos-757/experiments/prover/L021/closure_results.json'))['pieces']
pcs = [(p['name'], nv(p['edges']), [tuple(e) for e in p['edges']], p['W']) for p in src]
def ap_graph(A):
    A = sorted(A); idx = {a: i for i, a in enumerate(A)}; S = set(A); E = []
    for i, a in enumerate(A):
        for c in A[i+1:]:
            if (a + c) % 2 == 0 and (a + c)//2 in S: E.append((idx[a], idx[(a+c)//2], idx[c]))
    return len(A), E
def is45(A):
    for q in itertools.combinations(A, 4):
        if len({abs(x - y) for x, y in itertools.combinations(q, 2)}) < 5: return False
    return True
def tau_bf_mask(edges_masks, S):
    """min |T|, T subset of S, meeting every edge inside S (edges given as masks)."""
    em = [e for e in edges_masks if e & S == e]
    if not em: return 0
    vs = [v for v in range(S.bit_length()) if (S >> v) & 1]
    for k in range(1, len(vs) + 1):
        for c in itertools.combinations(vs, k):
            m = 0
            for v in c: m |= 1 << v
            if all(m & e for e in em): return k
def best_def(edges_masks, S, copies):
    """exhaustive max over families of disjoint copies inside S of sum W - 35|E*| (>= 0)."""
    cs = [(U, W) for (U, W) in copies if U & S == U]
    em = [e for e in edges_masks if e & S == e]
    best = 0
    def rec(i, used, fam):
        nonlocal best
        if fam:
            es = 0
            for e in em:
                if e & used and not any(e & U == e for U, W in fam): es += 1
            val = sum(W for U, W in fam) - 35*es
            if val > best: best = val
        for j in range(i, len(cs)):
            if cs[j][0] & used: continue
            fam.append(cs[j]); rec(j + 1, used | cs[j][0], fam); fam.pop()
    rec(0, 0, [])
    return best
def test_set(name, A, allsub=True):
    assert len(set(A)) == len(A)
    n, E = ap_graph(A)
    is45ok = is45(A) if n <= 16 else None
    assert in_C(n, E)
    em = [sum(1 << v for v in e) for e in E]
    copies = []
    for (nm, pn, pe, W) in pcs:
        for U in induced_copies(n, E, pn, pe): copies.append((sum(1 << v for v in U), W))
    viol2 = 0; violKT = 0; minP = None; cnt = 0; cntKT = 0
    subsets = range(1, 1 << n) if allsub else [(1 << n) - 1]
    for S in subsets:
        k = bin(S).count('1'); mS = sum(1 for e in em if e & S == e)
        t = tau_bf_mask(em, S); D = best_def(em, S, copies); Av = A_val(k, mS, t)
        cnt += 1
        if D > 11*(k - mS) or D < 0: viol2 += 1
        deg = max([sum(1 for e in em if e & S == e and (e >> v) & 1) for v in range(n) if (S >> v) & 1] or [0])
        if deg <= 3:
            cntKT += 1; P = Av + D
            minP = P if minP is None else min(minP, P)
            if P < 0: violKT += 1
    tf = tau_bf_mask(em, (1 << n) - 1)
    print(f'{name}: n={n} m={len(E)} tau={tf} A={A_val(n, len(E), tf)} (4,5)={is45ok}; induced subgraphs tested {cnt}: '
          f'Thm2 violations {viol2}; KT tested on {cntKT} with Delta<=3: violations {violKT}, min P {minP}', flush=True)
rec = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
for k in ['8', '10', '11', '12', '12b', '12c', '14']:
    test_set('record ' + k, rec[k]['set'], allsub=True)
fib = [2, 3]
while len(fib) < 22: fib.append(fib[-1] + fib[-2])
for n in range(4, 23):
    test_set('Fibonacci n=%d' % n, fib[:n], allsub=(n <= 12))
# hypertrees with a perfect matching
rng = random.Random(7)
for k in range(0, 7):
    for trial in range(3):
        M = [(3*i, 3*i + 1, 3*i + 2) for i in range(2*k + 1)]
        free = {i: [0, 1, 2] for i in range(2*k + 1)}
        E = list(M); nodes = [0]; nxt = 1
        for c in range(k):
            f = rng.choice([x for x in nodes if free[x]] or nodes)
            g1, g2 = nxt, nxt + 1; nxt += 2; nodes += [g1, g2]
            vs = []
            for x in (f, g1, g2):
                o = free[x].pop(rng.randrange(len(free[x]))) if free[x] else rng.randrange(3)
                vs.append(3*x + o)
            E.append(tuple(vs))
        n = 6*k + 3; m = len(E)
        assert in_C(n, E)
        t = tau_ilp(n, E)
        copies = [(sum(1 << v for v in U), W) for (nm, pn, pe, W) in pcs for U in induced_copies(n, E, pn, pe)]
        D = best_def([sum(1 << v for v in e) for e in E], (1 << n) - 1, copies) if k <= 4 else DEF_ilp(n, E, [(frozenset(v for v in range(n) if (U >> v) & 1), W) for U, W in copies])[0]
        print(f'hypertree k={k} trial {trial}: n={n} m={m} tau={t} A={A_val(n, m, t)} (3k-16={3*k-16}) DEF={D} (16-3k={16-3*k}) P={A_val(n, m, t) + D}', flush=True)
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
t = tau_ilp(7, F7); copies = [(sum(1 << v for v in U), W) for (nm, pn, pe, W) in pcs for U in induced_copies(7, F7, pn, pe)]
print('F7: tau', t, 'A', A_val(7, 5, t), 'DEF', best_def([sum(1 << v for v in e) for e in F7], 127, copies))
