"""(L012, descriptive, NOT part of the proof) Structure of the open maximum-degree-3 case: H = (23,21,10) with max degree 3, v of degree 3,
G = H - v = (22,18,9) of slack 3, max degree <= 3.  Lists the decompositions of (22,18) with total slack 3, and for the connected
cells that would be needed, the decompositions of X - w (one level of the engine's recursion) with the class counts of the
component cells already computed in out/cells (None = not computed)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import decompositions
def known(c):
    p = 'out/cells/cell_%d_%d_%d_D%d.txt' % c
    if c[:2] == (1, 0): return 1
    if not os.path.exists(p): return None
    return sum(1 for l in open(p) if l.startswith('FOUND:'))
print('decompositions of (22,18), slack 3:', decompositions(22, 18, 3))
for X in [(21, 18, 9), (19, 17, 8), (22, 18, 9)]:
    n, m, t = X; s = 3 * n + 2 * m - 11 * t
    for d in range(max(1, math.ceil(3 * m / n)), 4):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0: continue
            decs = decompositions(n - 1, m - d, Sp)
            print('cell', X, 'slack', s, '| d=%d tau\'=%d: X-w=(%d,%d) slack %d, %d decompositions' % (d, tp, n - 1, m - d, Sp, len(decs)))
            for dec in decs:
                ks = [known(c + (3,)) for c in dec if c != (1, 0, 0)]
                big = [c for c in dec if c != (1, 0, 0) and c[1] > 10]
                print('     ', list(dec), 'known D3 class counts', ks, 'components with m>10 needing recursion', big)
