"""(L014) python3 input_counts.py CELLDIR n m t D : for every branch of the recursion key, the number of inputs of every decomposition
recomputed from the cell files as prod over types of C(|cell| + k - 1, k) (k = multiplicity), compared with the INFO record."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('ENGINELOG', os.devnull)
d = sys.argv[1]; os.environ['CELLDIR'] = d
import engine
n, m, t, D = map(int, sys.argv[2:6])
def size(key):
    if key[:2] == (1, 0): return 1
    fn = os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % key)
    if not os.path.exists(fn): return 0      # trivial (guard) cells are not written; they are empty
    return sum(1 for l in open(fn) if l.startswith('FOUND:'))
info = None
for l in open(os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % (n, m, t, D))):
    if l.startswith('INFO '): info = json.loads(l[5:])
ok = True
for b in info['branches']:
    tot = 0
    for dec, recorded in b['dec']:
        dec = [tuple(x) for x in dec]; prod = 1
        for typ in sorted(set(dec)):
            k = dec.count(typ); s = size(typ + (b['d'],)); prod *= math.comb(s + k - 1, k)
        tot += prod; ok = ok and prod == recorded
        print('  d=%d t\'=%d %s: recomputed %d, recorded %d' % (b['d'], b['tp'], dec, prod, recorded))
    ok = ok and tot == b['inputs']
    print('branch d=%d t\'=%d S\'=%d: inputs recomputed %d, recorded %d' % (b['d'], b['tp'], b['Sp'], tot, b['inputs']))
print('ALL EQUAL' if ok else 'DIFFERENCES')
