"""Referee L023 round 1: the selfsim/reader JSON files hold many integer lists (seeds, map indices, h-sequences). Keep only the
lists that ARE (4,5)-sets (direct check of all 4-subsets) and report Q8 containment per key."""
import json, itertools
import hg_checks as H
def ap_graph(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [(i, idx[(A[i] + A[k]) // 2], k) for i in range(len(A)) for k in range(i + 1, len(A)) if (A[i] + A[k]) % 2 == 0 and (A[i] + A[k]) // 2 in idx]
def is45(A):
    if len(set(A)) != len(A): return False
    return all(len(set(abs(a - b) for a, b in itertools.combinations(Q, 2))) >= 5 for Q in itertools.combinations(A, 4))
def walk(o, path, out):
    if isinstance(o, list) and len(o) >= 4 and all(isinstance(x, int) for x in o): out.append((path, o))
    elif isinstance(o, list):
        for i, x in enumerate(o): walk(x, path + '[%d]' % i, out)
    elif isinstance(o, dict):
        for k, x in o.items(): walk(x, path + '/' + str(k), out)
for f in ('reader_5_9_family.json', 'selfsim_families.json'):
    out = []; walk(json.load(open('/home/user/Erdos-757/data/' + f)), '', out)
    for path, A in out:
        q = len(H.q8_embeddings(ap_graph(A))) > 0
        s45 = is45(A) if len(A) <= 70 else None
        if q or not s45: print(f, path, 'len', len(A), 'is (4,5)-set:', s45, 'contains Q8:', q, 'head', A[:6])
    print(f, 'lists', len(out), '; (4,5)-sets', sum(1 for p, A in out if is45(A)), '; (4,5)-sets containing Q8', sum(1 for p, A in out if is45(A) and H.q8_embeddings(ap_graph(A))))
