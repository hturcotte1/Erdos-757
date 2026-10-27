import sys
from localconf import run, best_value_all
from hg import in_class_C
rootdeg = int(sys.argv[1]); R = int(sys.argv[2]); lim = int(sys.argv[3]) if len(sys.argv) > 3 else 50
out, stats = run(rootdeg, R)
print(stats['nodes'], stats['reducible'], stats['leaves'])
for c in out[:lim]:
    closed = c.nproc >= len(c.inc)
    bv = best_value_all(c, closed)
    print('nV=%d nproc=%d closed=%s best=%s degs=%s dist=%s' % (len(c.inc), c.nproc, closed, bv, [c.deg[v] for v in range(c.nproc)], c.dist))
    print('   edges', c.edges)
