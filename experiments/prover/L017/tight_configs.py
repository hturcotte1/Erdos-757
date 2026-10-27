"""L017, Remark 8.3 (illustrative; conditional consequences of Theorem 4 for slack -2).
For every tight connected member F of C with maximum degree <= 3 in the stored, refereed cell lists (the only non-empty
tight Delta<=3 cells with at most 26 vertices other than the uncomputed (25,23,11): (3,1,1), (10,7,4), (14,12,6), (17,13,7);
the other tight Delta<=3 cells with n <= 26 are stored EMPTY, see engine_decomps/tight_cells output), compute exactly:
 - the anti-pairs: pairs {x, y} of vertices with d_F <= 2 contained in no minimum transversal of F;
 - property (P): every anti-pair {x, y} shares an edge of F and {d_F(x), d_F(y)} = {1, 2} (or F is the single edge);
 - the numbers of local configurations required by the exact conditions of Theorem 4 (iv) (attachment vertices must have
   d_F <= 2 because Delta(H) <= 3; a pair of co-vertices of v lying inside one component must not lie inside an edge of F):
     role_b : 3-sets of pairwise anti vertices                                  (pattern (b), on both components)
     role_c : two disjoint pairs, each not inside an edge, all 4 cross pairs anti   (patterns (c1), (c2), (d), on F_1)
     role_e : a pair {a,b} not inside an edge and a vertex e with {a,e}, {b,e} anti  (pattern (e), on both components)
     role_f1: a pair {a,b} not inside an edge and two more vertices c, e, all 4 cross pairs anti (pattern (f), on F_1)
     role_f2: anti-pairs {d, f}                                                  (pattern (f), on F_2)
Usage: python3 tight_configs.py"""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hyp import read_cell, masks, all_min_transversals, degrees
HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ['out/L012/cells/cell_3_1_1_D3.txt', 'out/L012/cells/cell_10_7_4_D3.txt', 'out/L012/cells/cell_14_12_6_D3.txt',
         'out/L012/cells/cell_17_13_7_D3.txt']

def analyse(n, es):
    Ts, t = all_min_transversals(masks(es)); d = degrees(n, es)
    cov = set()
    for T in Ts:
        vs = [x for x in range(n) if T >> x & 1]
        for a, b in itertools.combinations(vs, 2): cov.add((a, b))
    inedge = set()
    for e in es:
        for a, b in itertools.combinations(sorted(e), 2): inedge.add((a, b))
    V2 = [x for x in range(n) if d[x] <= 2]
    anti = set((a, b) for a, b in itertools.combinations(V2, 2) if (a, b) not in cov)
    A = lambda x, y: (min(x, y), max(x, y)) in anti
    P = all(((a, b) in inedge) and sorted((d[a], d[b])) == [1, 2] for (a, b) in anti) or len(es) == 1
    rb = sum(1 for x, y, z in itertools.combinations(V2, 3) if A(x, y) and A(x, z) and A(y, z))
    pairs = [(a, b) for a, b in itertools.combinations(V2, 2) if (a, b) not in inedge]
    rc = sum(1 for (p, q) in itertools.combinations(pairs, 2) if not set(p) & set(q) and all(A(x, y) for x in p for y in q))
    re_ = sum(1 for (a, b) in pairs for e in V2 if e not in (a, b) and A(a, e) and A(b, e))
    rf1 = sum(1 for (a, b) in pairs for c, e in itertools.permutations([x for x in V2 if x not in (a, b)], 2)
              if all(A(x, y) for x in (a, b) for y in (c, e))) // 2
    rf2 = len(anti)
    return dict(n=n, m=len(es), tau=t, deg=''.join(map(str, sorted(d, reverse=True))), anti=sorted(anti),
                anti_types=sorted((d[a], d[b], int((a, b) in inedge)) for a, b in anti), P=P, role_b=rb, role_c=rc,
                role_e=re_, role_f1=rf1, role_f2=rf2)

if __name__ == '__main__':
    for f in FILES:
        gs = read_cell(os.path.join(HERE, f)); n = int(os.path.basename(f).split('_')[1])
        for i, es in enumerate(gs):
            r = analyse(n, es)
            print('%s #%d: (n,m,tau)=(%d,%d,%d) degrees %s; anti-pairs %d %s; (P) %s; role_b=%d role_c=%d role_e=%d role_f1=%d role_f2=%d'
                  % (os.path.basename(f), i, r['n'], r['m'], r['tau'], r['deg'], len(r['anti']), r['anti_types'], r['P'],
                     r['role_b'], r['role_c'], r['role_e'], r['role_f1'], r['role_f2']))
