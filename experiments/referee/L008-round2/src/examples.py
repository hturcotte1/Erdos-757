"""Referee round 2 (L008): one hand-checkable obstruction for each case: an explicit F7 copy in a case-B hit and the smallest
P3 violation in an F7-free case-A hit (from out/ext_B.txt, out/ext_A.txt)."""
import re, itertools
def edges(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l.split('|')[0])]
def find_f7(E):
    Es = set(tuple(sorted(e)) for e in E)
    for p in sorted(set(v for e in E for v in e)):
        for a, b, c in itertools.combinations([e for e in E if p in e], 3):
            A, B, C = ([v for v in e if v != p] for e in (a, b, c))
            for x, y in itertools.product((0, 1), repeat=2):
                T1 = tuple(sorted((A[0], B[x], C[y]))); T2 = tuple(sorted((A[1], B[1 - x], C[1 - y])))
                if T1 in Es and T2 in Es: return [a, b, c, T1, T2]
def p3_witness(E, nv):
    best = None
    for S in range(1 << nv):
        s = bin(S).count('1'); e = sum(1 for t in E if all(S >> v & 1 for v in t))
        if s >= 2 and e > s - 2 and (best is None or (s - e, s) < best[:2]): best = (s - e, s, e, [v for v in range(nv) if S >> v & 1])
    return best
B = next(l for l in open('out/ext_B.txt') if l.startswith('HIT')); E = edges(B)
print('case B hit:', E); print('  F7 copy:', find_f7(E)); print('  P3 violation (|S|-e(S), |S|, e(S), S):', p3_witness(E, 16))
A = next(l for l in open('out/ext_A.txt') if l.startswith('HIT') and 'F7=0' in l); E = edges(A)
print('case A hit (F7-free):', E); print('  P3 violation:', p3_witness(E, 16))
