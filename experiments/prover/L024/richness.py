"""L024, Lemma P input: co-transversality of vertex pairs in the 32 pieces.
A piece is RICH if every two of its vertices lie in a common minimum transversal.
For each piece: rich or not; the list of non-co-transversal pairs (with degrees and whether they share an edge).
Also checks the hand prediction from the pair lemma (L017 Thm 2(U) + L016): in a tight piece a non-co-transversal pair
{x,y} has d(x)+d(y)-sigma(x,y) <= 2 (slack-1 piece: <= 3).
Run: timeout 600 nice -n 10 python3 richness.py > richness_output.txt"""
import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L024')
from hyp24 import *
pieces = load_pieces()
for P in pieces:
    n = P['n']; E = P['edges']; d = P['deg']
    s = 3 * n + 2 * P['m'] - 11 * P['tau']
    share = set()
    for e in E:
        for a, b in itertools.combinations(e, 2): share.add((min(a, b), max(a, b)))
    nc = []
    for x, y in itertools.combinations(range(n), 2):
        b = (1 << x) | (1 << y)
        if not any(T & b == b for T in P['mts']):
            sig = 1 if (x, y) in share else 0
            nc.append((x, y, d[x], d[y], sig, d[x] + d[y] - sig))
    pred_ok = all(t[5] <= 2 for t in nc) if s == 0 else all(t[5] <= 3 for t in nc)
    print(P['name'], 'slack', s, 'RICH' if not nc else 'poor', 'non-co-transversal pairs (x,y,dx,dy,sigma,|boundary|):', nc,
          'pair-lemma bound respected:', pred_ok)
