"""(L013, prover) Which component-cell lists are load-bearing for the twelve top-level cells, and how each of them is corroborated:
'L012' = identical (canonical representatives) to L012's refereed list; 'direct' = computed on the direct route (m <= 10, enum_conn);
'C6' = recursion cell confirmed by direct enumeration in crosscheck_direct.jsonl; 'known-empty' = empty by L010/L011 (Step 7.4);
'recursion' = computed only by the recursion (Lemma E').  For a decomposition with an empty component cell only the empty cells matter."""
import os, sys, json, re
cd = 'out/cells'; L12 = 'out/l012cells/cells'
def reps(d, key):
    fn = os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % key)
    if not os.path.exists(fn): return None
    return frozenset(l.strip() for l in open(fn) if l.startswith('FOUND:'))
def info(key): return json.loads([l for l in open(os.path.join(cd, 'cell_%d_%d_%d_D%d.txt' % key)) if l.startswith('INFO ')][0][5:])
c6 = set(tuple(json.loads(l)['cell']) for l in open('crosscheck_direct.jsonl') if l.strip() and json.loads(l).get('equal'))
KNOWN = {(13,8,5),(19,11,7),(11,6,4),(14,7,5),(16,9,6),(17,8,6),(17,9,6),(19,10,7),(20,10,7)}
KNOWN3 = {(20,14,8,3),(21,13,8,3),(18,12,7,3)}
KNOWN2 = {(21,11,8,2),(21,12,8,2),(21,13,8,2),(20,14,8,2)}   # L011 C2: enum_conn with DMAX = 2 found 0
def status(key):
    n, m, t, D = key
    if (n, m) == (1, 0) or key[:3] == (3, 1, 1): return 'trivial'
    r = reps(cd, key); r12 = reps(L12, key); inf = info(key)
    tags = []
    if r12 is not None and r12 == r: tags.append('L012')
    if inf['route'] == 'direct': tags.append('direct')
    if key in c6: tags.append('C6')
    if not r and (key[:3] in KNOWN and D <= 3 or key in KNOWN3 or key in KNOWN2): tags.append('known-empty')
    if not tags: tags.append('recursion')
    return '+'.join(tags)
TOP = [(23,13,9,2),(23,14,9,3),(23,20,10,3),(24,12,9,2),(24,13,9,3),(24,18,10,3),(25,16,10,2),(25,17,10,3),(25,22,11,3),(26,14,10,2),(26,15,10,3),(26,21,11,3)]
residual = set()
for top in TOP:
    for b in info(top)['branches']:
        for dec, size in b['dec']:
            keys = sorted(set((c[0], c[1], c[2], b['d']) for c in dec), key=lambda k: -k[0])
            empties = [k for k in keys if (k[0], k[1]) != (1, 0) and not reps(cd, k)]
            use = empties if empties else keys
            st = [(k, status(k)) for k in use]
            if empties and any(s != 'recursion' for k, s in st): use_st = [x for x in st if x[1] != 'recursion'][:1]
            else: use_st = st
            for k, s in use_st:
                if s == 'recursion': residual.add(k)
            print('%s d=%d %-45s %s' % (top, b['d'], ' + '.join('(%d,%d,%d)' % tuple(c) for c in dec), '; '.join('%s%s:%s' % ('(%d,%d,%d,%d)' % k, '[empty]' if not reps(cd, k) and (k[0],k[1]) != (1,0) else '', s) for k, s in use_st)))
print('RESIDUAL (load-bearing lists corroborated only by the recursion itself):', sorted(residual))
