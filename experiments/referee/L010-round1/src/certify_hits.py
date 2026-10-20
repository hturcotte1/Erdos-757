"""Referee L010 r1: definitional certificates for every hit of the class-representative runs that is claimed NOT in C.
For a hit claimed to contain F7: an explicit injective map phi of {0..6} into V(H) with phi(e) an edge of H for each of
the five edges e of F7 = {012,034,056,135,246}; it is found by plain backtracking over all images of 0 and all ordered
triples of edges at phi(0) and both orientations of each, then CHECKED against the definition.
For a hit claimed F7-free but violating (P3): an explicit vertex set S with e(S) >= |S|-1, |S| >= 2, found by trying the
vertex sets V(F) of all edge subsets F, then checked by recounting the edges inside S.
Also re-checks tau(H) >= TG+1 by exhaustive search over all vertex subsets of size TG (itertools).
Usage: certify_hits.py FILE TG"""
import sys, re, itertools
F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def f7_embedding(E):
    Es = set(frozenset(e) for e in E); V = sorted(set(v for e in E for v in e))
    for p in V:
        at = [e for e in E if p in e]
        for e1, e2, e3 in itertools.permutations(at, 3):
            o = [tuple(v for v in e if v != p) for e in (e1, e2, e3)]
            for s in itertools.product((0, 1), repeat=3):
                img = [p] + [x for i in range(3) for x in (o[i] if s[i] == 0 else o[i][::-1])]
                if len(set(img)) != 7: continue
                if all(frozenset(img[v] for v in f) in Es for f in F7): return img
    return None
def p3_violation(E):
    for k in range(1, len(E) + 1):
        for F in itertools.combinations(E, k):
            S = set(v for e in F for v in e)
            eS = sum(1 for e in E if set(e) <= S)
            if eS >= len(S) - 1: return sorted(S), eS
    return None
def tau_ge(E, t):  # no vertex set of size t-1 meets every edge
    V = sorted(set(v for e in E for v in e))
    return not any(all(set(e) & set(T) for e in E) for T in itertools.combinations(V, t - 1))
f, TG = sys.argv[1], int(sys.argv[2])
n = nf7 = np3 = ninC = bad = ntau = 0
for l in open(f):
    if not (l.startswith('HIT') or l.startswith('CHIT')): continue
    tag = l.split(':')[0]; E = parse(l); n += 1
    if not tau_ge(E, TG + 1): bad += 1; print('TAU FAIL', l.strip())
    else: ntau += 1
    if tag.startswith('CHIT'): ninC += 1; continue
    if '_F7' in tag:
        img = f7_embedding(E)
        Es = set(frozenset(e) for e in E)
        if img is None or len(set(img)) != 7 or not all(frozenset(img[v] for v in fe) in Es for fe in F7): bad += 1; print('F7 FAIL', l.strip())
        else: nf7 += 1
    elif '_P3' in tag:
        if f7_embedding(E) is not None: bad += 1; print('claimed F7-free but embedding found', l.strip())
        w = p3_violation(E)
        if w is None or not (len(w[0]) >= 2 and sum(1 for e in E if set(e) <= set(w[0])) >= len(w[0]) - 1): bad += 1; print('P3 FAIL', l.strip())
        else: np3 += 1
    else: bad += 1; print('UNCLASSIFIED', l.strip())
print('%s: hits %d, tau>=%d confirmed %d, F7 embeddings verified %d, P3 violations verified %d, claimed in C %d, failures %d' % (f, n, TG + 1, ntau, nf7, np3, ninC, bad))
