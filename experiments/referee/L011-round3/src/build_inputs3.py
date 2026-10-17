"""Referee round 3: disjoint unions of class representatives (my in-C lists, SURV lines) as extension inputs (numeric lines).
Usage: build_inputs3.py OUT SLOT ...   SLOT = AP | ISO | FILE:n[:k]  (k copies of the same file: unordered with repetition)"""
import re, sys, itertools
def load(f):
    L = []
    for l in open(f):
        if l.startswith('SURV:'): L.append([tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)])
    return L
slots = []
for s in sys.argv[2:]:
    if s == 'AP': slots.append(([[(0, 1, 2)]], 3))
    elif s == 'ISO': slots.append(([[]], 1))
    else:
        parts = s.split(':'); L = load(parts[0]); n = int(parts[1]); k = int(parts[2]) if len(parts) > 2 else 1
        if k == 1: slots.append((L, n))
        else:
            combos = [sum(([comp] for comp in combo), []) for combo in itertools.combinations_with_replacement(range(len(L)), k)]
            # each combo is a list of k components placed on consecutive blocks
            merged = []
            for combo in itertools.combinations_with_replacement(range(len(L)), k):
                es = []; off = 0
                for ci in combo: es += [tuple(v + off for v in e) for e in L[ci]]; off += n
                merged.append(es)
            slots.append((merged, n * k))
cnt = 0
with open(sys.argv[1], 'w') as f:
    for combo in itertools.product(*[s[0] for s in slots]):
        es = []; off = 0
        for (L, nv), comp in zip(slots, combo):
            es += [tuple(v + off for v in e) for e in comp]; off += nv
        f.write('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) + '\n'); cnt += 1
print(sys.argv[1], 'inputs:', cnt, 'points:', off)
