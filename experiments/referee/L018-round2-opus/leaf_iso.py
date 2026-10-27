"""Referee round 2 (opus): classify the radius-3 leaves of the prover's enumeration
(experiments/prover/L018/out_root1_R3_leaves.txt) under rooted isomorphism and recompute,
with my own exact tau, the maximum value over all nonempty Z of processed vertices.
No import from e757/, judge/ or the prover's hg.py/localconf.py."""
import ast, re, sys, itertools
import networkx as nx
from networkx.algorithms import isomorphism as iso

fn = sys.argv[1]
leaves = []
cur = None
for line in open(fn):
    line = line.rstrip('\n')
    m = re.match(r'nV=(\d+) nproc=(\d+) closed=(\w+) best=(.*) degs=(\[.*?\]) dist=(\[.*?\])', line)
    if m:
        cur = dict(nV=int(m.group(1)), nproc=int(m.group(2)), closed=(m.group(3) == 'True'),
                   best=m.group(4), degs=ast.literal_eval(m.group(5)), dist=ast.literal_eval(m.group(6)))
        continue
    m = re.match(r'\s+edges (\[.*\])', line)
    if m and cur is not None:
        cur['edges'] = ast.literal_eval(m.group(1)); leaves.append(cur); cur = None
print('leaves read:', len(leaves))

def tau_mask(edges, mask, memo):
    if mask == 0: return 0
    if mask in memo: return memo[mask]
    i = (mask & -mask).bit_length() - 1
    best = 10**9
    for u in edges[i]:
        rem = mask
        for j, e in enumerate(edges):
            if (rem >> j) & 1 and u in e: rem &= ~(1 << j)
        best = min(best, 1 + tau_mask(edges, rem, memo))
    memo[mask] = best
    return best

def incgraph(L):
    G = nx.Graph()
    for v in range(L['nV']): G.add_node(('v', v), kind='v', root=(v == 0))
    for i, e in enumerate(L['edges']):
        G.add_node(('e', i), kind='e', root=False)
        for v in e: G.add_edge(('v', v), ('e', i))
    return G

classes = []
nm = iso.categorical_node_match(['kind', 'root'], ['v', False])
for k, L in enumerate(leaves):
    E = L['edges']; n = L['nV']; P = list(range(L['nproc']))
    deg = [0] * n; inc = [0] * n
    for i, e in enumerate(E):
        for v in e: deg[v] += 1; inc[v] |= 1 << i
    memo = {}; best = None
    for r in range(1, len(P) + 1):
        for Z in itertools.combinations(P, r):
            if L['closed'] and len(Z) == n: continue
            F = 0
            for z in Z: F |= inc[z]
            val = 3 * len(Z) + 2 * bin(F).count('1') - 11 * tau_mask(E, F, memo)
            if best is None or val > best[0]: best = (val, Z)
    # structural type
    ty = 'other'
    if n == 3: ty = 'single-edge'
    else:
        e0 = [e for e in E if 0 in e][0]; a, b = [v for v in e0 if v != 0]
        A = [e for e in E if a in e and e != e0][0]; B = [e for e in E if b in e and e != e0][0]
        com = set(A) & set(B)
        if not com: ty = 'P-tree-3' if L['nproc'] == 15 and all(deg[v] == 2 for v in P[1:]) else 'tree-other'
        else:
            c = com.pop(); Cs = [e for e in E if c in e and e not in (A, B)]
            if len(Cs) == 1:
                C = Cs[0]; x, y = sorted(v for v in C if v != c)
                ty = 'P-tri-3 Cdegs=%s' % (tuple(sorted((deg[x], deg[y]))),)
    G = incgraph(L)
    for cl in classes:
        if nx.is_isomorphic(cl['G'], G, node_match=nm):
            cl['members'].append(k); break
    else:
        classes.append(dict(G=G, members=[k], ty=ty))
    print('leaf %d: nV=%d nproc=%d closed=%s type=%s my best value=%s (prover: %s)' % (k, n, L['nproc'], L['closed'], ty, best[0], L['best']))
print('rooted isomorphism classes:', len(classes))
for cl in classes: print('  ', cl['ty'], 'multiplicity', len(cl['members']), 'leaves', cl['members'])
