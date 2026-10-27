"""Referee L023 round 1 (own code): Proposition 6 tested on all realizable data in data/ (APs recomputed from the integer sets):
the 2,910 saturated extremal 14-point census sets, the 54,243 extremal 12-point sets, the ext15 sets (if they carry a set),
the reader's family and self-similar family sets, and the Fibonacci set {F_3..F_30}. A hit would refute Proposition 6."""
import gzip, json, itertools
import hg_checks as H
def ap_graph(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [(i, idx[(A[i] + A[k]) // 2], k) for i in range(len(A)) for k in range(i + 1, len(A)) if (A[i] + A[k]) % 2 == 0 and (A[i] + A[k]) // 2 in idx]
def scan(name, sets):
    hits = 0; cnt = 0
    for A in sets:
        cnt += 1
        if H.q8_embeddings(ap_graph(A)): hits += 1
    print(name, 'sets', cnt, 'containing Q8', hits, flush=True)
def jl(p):
    for l in gzip.open(p, 'rt'):
        if l.strip(): yield json.loads(l)
D = '/home/user/Erdos-757/data/'
scan('census_n14_m12 (2,910 classes)', (r['set'] for r in jl(D + 'census_n14_m12_classes.jsonl.gz')))
scan('ext12_all_rows (54,243 classes)', (r['set'] for r in jl(D + 'ext12_all_rows.jsonl.gz')))
e15 = [r['set'] for r in jl(D + 'ext15_sets.jsonl.gz') if isinstance(r.get('set'), list)]
scan('ext15_sets (rows with a set)', e15)
def walk(o, out):
    if isinstance(o, list) and len(o) >= 4 and all(isinstance(x, int) for x in o): out.append(o)
    elif isinstance(o, list):
        for x in o: walk(x, out)
    elif isinstance(o, dict):
        for x in o.values(): walk(x, out)
for f in ('reader_5_9_family.json', 'selfsim_families.json'):
    out = []; walk(json.load(open(D + f)), out); scan(f + ' (integer lists found)', out)
F = [2, 3]
while len(F) < 28: F.append(F[-1] + F[-2])
bad = sum(1 for Q in itertools.combinations(F[:14], 4) if len(set(abs(a - b) for a, b in itertools.combinations(Q, 2))) < 5)
print('Fibonacci F_3..F_16 is (4,5):', bad == 0, '; AP count of F_3..F_30:', len(ap_graph(F)))
scan('Fibonacci {F_3..F_30}', [F])
