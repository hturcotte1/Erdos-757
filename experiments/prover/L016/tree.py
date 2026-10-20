"""(L014) Dry run of engine.cell: lists every cell key (n,m,t,D) that engine.cell(n0,m0,t0,D0) visits (same guards, same branches
(d, t'), same decompositions engine.decompositions, same component cells with bound d), without computing anything.
Usage: python3 tree.py n m t D [MD]   -> prints one line per non-trivial cell: key, route (direct/recurse), and its branches."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
def trivial(n, m, t, D):
    if (n, m) == (1, 0): return 'isolated'
    if m == 0 or t < 1 or t > m or n > 2 * m + 1 or m > n - 2 or 17 * t > 5 * n + 3 * m or D < 1: return 'empty-by-guard'
    return None
def visit(key, MD, seen, order, need):
    if key in seen: return
    seen[key] = None
    n, m, t, D = key
    tr = trivial(*key)
    if tr: seen[key] = (tr, []); return
    if m <= MD: seen[key] = ('direct', []); order.append(key); need[key] = set(); return
    brs = []; kids = set()
    for d in range(max(1, math.ceil(3 * m / n)), D + 1):
        for tp in (t - 1, t):
            Sp = 3 * (n - 1) + 2 * (m - d) - 11 * tp
            if Sp < 0 or tp < 0: continue
            decs = engine.decompositions(n - 1, m - d, Sp)
            brs.append((d, tp, Sp, decs))
            for dec in decs:
                for typ in sorted(set(dec)):
                    k2 = (typ[0], typ[1], typ[2], d); visit(k2, MD, seen, order, need); kids.add(k2)
    seen[key] = ('recurse', brs); order.append(key)
    need[key] = set(k for k in kids if seen[k][0] in ('direct', 'recurse'))
if __name__ == '__main__':
    a = list(map(int, sys.argv[1:5])); MD = int(sys.argv[5]) if len(sys.argv) > 5 else 10
    seen, order, need = {}, [], {}
    visit(tuple(a), MD, seen, order, need)
    for k in order:
        route, brs = seen[k]
        print('CELL', k, route, ' '.join('[d=%d tp=%d S=%d decs=%d]' % (d, tp, S, len(decs)) for d, tp, S, decs in brs), 'needs', sorted(need[k]))
    print('TOTAL nontrivial cells', len(order), 'direct', sum(1 for k in order if seen[k][0] == 'direct'), 'recurse', sum(1 for k in order if seen[k][0] == 'recurse'))
