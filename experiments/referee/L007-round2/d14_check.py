import itertools, random, re, json
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
from canon_branch_test import canonical  # my implementation of the Lemma D process
from f7_ref import det_A, inc, is_linear
D14 = [(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13),(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12),(2,3,4)]
def tau(n, es):
    for k in range(n + 1):
        for S in itertools.combinations(range(n), k):
            s = set(S)
            if all(s & set(e) for e in es): return k
def p3(n, es):
    for r in range(2, n + 1):
        for S in itertools.combinations(range(n), r):
            s = set(S)
            if sum(set(e) <= s for e in es) > r - 2: return False
    return True
L = {frozenset(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([0-9,]+)\)', l)) for l in open('rerun/mine_14_11_6_deg3.txt') if l.startswith('FOUND:')}
rng = random.Random(5); hits = 0
for i in range(200):
    hits += canonical(14, D14, rng) in L
G = inc(D14); aut = sum(1 for _ in GraphMatcher(G, G, node_match=lambda a, b: a['t'] == b['t']).isomorphisms_iter())
deg = sorted((sum(v in e for e in D14) for v in range(14)), reverse=True)
ex = [tuple(e) for e in json.load(open('/home/user/Erdos-757/experiments/falsify/i11-inequality/f7_containing_violation.json'))['edges']]
iso_ex = nx.is_isomorphic(inc(ex), G, node_match=lambda a, b: a['t'] == b['t'])
print(dict(canonical_copies_in_998=hits, of=200, tau=tau(14, D14), aut=aut, degrees=deg, linear=is_linear(D14), P3=p3(14, D14), hasF7=det_A(D14), iso_to_falsifier_example=iso_ex))
