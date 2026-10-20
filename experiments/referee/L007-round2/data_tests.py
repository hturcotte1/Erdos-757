"""Numerical tests of Lemma A (11 tau <= 3n+2m for n<=13), Theorem 1/2 (m=11, n=14 -> tau<=5) on realizable data.
Own code: APs from the definition, tau by exact branching (pick an uncovered edge, branch on its 3 vertices)."""
import itertools, json, gzip, sys, collections, time
def aps(A):
    S = set(A); A = sorted(A)
    return [(x, (x + z) // 2, z) for x, z in itertools.combinations(A, 2) if (x + z) % 2 == 0 and (x + z) // 2 in S]
def cover(edges, k):
    if not edges: return True
    if k == 0: return False
    e = edges[0]
    return any(cover([f for f in edges if v not in f], k - 1) for v in e)
def tau(edges):
    k = 0
    while not cover(edges, k): k += 1
    return k
def is45(A):
    return all(len({abs(x - y) for x, y in itertools.combinations(B, 2)}) >= 5 for B in itertools.combinations(A, 4))
res = collections.OrderedDict(); t0 = time.time()
rec = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
fib = [2, 3]
while len(fib) < 14: fib.append(fib[-1] + fib[-2])
sets = {('rec_' + k): v['set'] for k, v in rec.items()}
sets['W'] = [0, 323, 523, 566, 569, 572, 595, 609, 621, 646, 723, 851, 919, 1379]
sets['Fib_F3_F16'] = fib
fib20 = [2, 3]
while len(fib20) < 20: fib20.append(fib20[-1] + fib20[-2])
# Part A: all subsets with <= 13 points of each record set (and of the first 16 Fibonacci numbers from F3)
viol = 0; tested = 0; thm1 = 0; thm1_bad = 0
for name, A in sets.items():
    A = sorted(A); assert is45(A), name
    E = aps(A); n = len(A)
    for r in range(1, min(n, 13) + 1):
        for S in itertools.combinations(A, r):
            s = set(S); ES = [e for e in E if set(e) <= s]
            t = tau(ES); tested += 1
            if 11 * t > 3 * r + 2 * len(ES): viol += 1; print('LEMMA A VIOLATION', name, S)
    if n == 14 and len(E) == 11:
        thm1 += 1; thm1_bad += tau(E) > 5
res['partA'] = dict(sets=list(sets), subsets_tested=tested, lemmaA_violations=viol, fourteen_point_m11_sets=thm1, thm1_violations=thm1_bad)
print('part A', res['partA'], round(time.time() - t0, 1), flush=True)
# Part B: census classes, all 13- and 12-point subsets
viol = 0; tested = 0; ncls = 0
for line in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt'):
    d = json.loads(line); ncls += 1
    E = [tuple(e) for e in d['edges']]; assert len(E) == 12
    for r in (13, 12):
        for S in itertools.combinations(range(14), r):
            s = set(S); ES = [e for e in E if set(e) <= s]
            t = tau(ES); tested += 1
            if 11 * t > 3 * r + 2 * len(ES): viol += 1
res['partB'] = dict(classes=ncls, subsets_tested=tested, lemmaA_violations=viol)
print('part B', res['partB'], round(time.time() - t0, 1), flush=True)
# Part C: Theorem 2 on 14-point (4,5)-sets with exactly 11 APs: (class + new-AP point x) minus a point, classes 2000..2199
lo, hi = int(sys.argv[1]) if len(sys.argv) > 1 else 2000, int(sys.argv[2]) if len(sys.argv) > 2 else 2200
hist = collections.Counter(); nsets = 0; ncls = 0
for idx, line in enumerate(gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt')):
    if idx < lo: continue
    if idx >= hi: break
    ncls += 1
    A = sorted(4 * a for a in json.loads(line)['set']); S = set(A)
    cand = set()
    for a, b in itertools.combinations(A, 2): cand |= {(a + b) // 2, 2 * a - b, 2 * b - a}
    cand -= S
    trip = list(itertools.combinations(A, 3)); seen = set()
    for x in sorted(cand):
        if not all(len({abs(p - q) for p, q in itertools.combinations(T + (x,), 2)}) >= 5 for T in trip): continue
        B = sorted(A + [x])
        for u in B:
            C = [y for y in B if y != u]
            E = aps(C)
            if len(E) != 11: continue
            key = tuple(y - C[0] for y in C)
            if key in seen: continue
            seen.add(key); nsets += 1
            hist[14 - tau(E)] += 1
res['partC'] = dict(classes=[lo, hi], sets_m11=nsets, h_hist=dict(hist))
print('part C', res['partC'], round(time.time() - t0, 1), flush=True)
json.dump(res, open('data_tests.json', 'w'), indent=1)
