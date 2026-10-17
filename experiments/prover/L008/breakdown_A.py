"""Case A breakdown: classify each hit by the type of its R (= the hit minus the edge (12,13,14) and the edges at 15) and by how
many of the three edges at the new vertex 15 meet the separate edge {12,13,14}."""
import re, sys, collections, itertools
sys.path.insert(0, 'indep'); 
def f7(es):
    for five in itertools.combinations(es, 5):
        d = collections.Counter(v for e in five for v in e)
        if len(d) == 7 and sorted(d.values()) == [2, 2, 2, 2, 2, 2, 3]: return True
    return False
def p3(es):
    ms = [sum(1 << v for v in e) for e in es]; U = [0] * (1 << len(ms))
    for F in range(1, 1 << len(ms)):
        low = (F & -F).bit_length() - 1; U[F] = U[F & (F - 1)] | ms[low]
        if bin(U[F]).count('1') - bin(F).count('1') < 2: return False
    return True
cache = {}
c = collections.Counter()
for l in open(sys.argv[1]):
    if not l.startswith('HIT:'): continue
    es = [tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)]
    R = tuple(e for e in es if 15 not in e and e != (12, 13, 14))
    if R not in cache: cache[R] = ('R has F7' if f7(R) else ('R F7-free, violates P3' if not p3(R) else 'R in O+'))
    k = sum(1 for e in es if 15 in e and set(e) & {12, 13, 14})
    c[(cache[R], 'v-edges meeting {12,13,14}: %d' % k)] += 1
for key, val in sorted(c.items()): print(key, val)
print('distinct R among hits:', len(cache), collections.Counter(cache.values()))
