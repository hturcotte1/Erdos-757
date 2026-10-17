"""(L014) Remark 4 arithmetic: the branch of (27,25,12,3) and of (26,22,11,3), decompositions by engine.decompositions and by the brute
force of decomp_check.py (must be EQUAL)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('CELLDIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'dummycells')); os.environ.setdefault('ENGINELOG', os.devnull)
import engine, decomp_check, math
for (n, m, t) in ((27, 25, 12), (26, 22, 11)):
    for d in range(max(1, math.ceil(3 * m / n)), 4):
        for tp in (t - 1, t):
            S = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if S < 0: print('(%d,%d,%d,3): d=%d t\'=%d S\'=%d < 0, no branch' % (n, m, t, d, tp, S)); continue
            e = sorted(tuple(sorted(x)) for x in engine.decompositions(n - 1, m - d, S)); b = sorted(decomp_check.bf(n - 1, m - d, S))
            print('(%d,%d,%d,3): d=%d t\'=%d S\'=%d: decompositions of (%d,%d): engine %d, brute force %d, %s' % (n, m, t, d, tp, S, n - 1, m - d, len(e), len(b), 'EQUAL' if e == b else 'DIFFERENT'))
            for x in e: print('     ', list(x))
