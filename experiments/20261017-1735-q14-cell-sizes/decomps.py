"""Step 1: decompositions used by the engine recursion for the cells of the degree-3 case of (23,21,10); marks component cells not yet computed
(no cell file in out/cells) -- note the engine recursion itself may need further sub-cells below MD. Arithmetic only."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('CELLDIR', os.path.join(HERE, 'out', 'cells'))
sys.path.insert(0, HERE)
import engine
def valid(n, m, t, D):
    return not (m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1)
for (n, m, t, D) in [(23,21,10,3),(22,18,9,3),(19,17,8,3),(21,15,8,3),(18,14,7,3),(15,13,6,3)]:
    print('=== cell (%d,%d,%d) Delta<=%d' % (n, m, t, D))
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = engine.decompositions(n - 1, m - d, Sp)
            print('  branch d=%d tau\'=%d remainder (%d,%d) slack %d: %d decompositions' % (d, tp, n - 1, m - d, Sp, len(decs)))
            for dec in decs:
                desc = []
                for c in sorted(set(dec)):
                    k = dec.count(c)
                    if c == (1, 0, 0): desc.append('%dx isolated' % k); continue
                    ok = valid(c[0], c[1], c[2], d)
                    if not ok: st = 'void(guard)'
                    else:
                        r = engine.load((c[0], c[1], c[2], d)); st = 'DONE=%d' % len(r) if r is not None else 'NOT COMPUTED'
                    desc.append('%dx(%d,%d,%d)[%s]' % (k, c[0], c[1], c[2], st))
                print('     ', ' + '.join(desc))
