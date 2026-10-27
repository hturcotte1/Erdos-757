"""(a) Is the AP hypergraph of the C008 set isomorphic to class 40 of the (19,16,8,Delta<=4) cell list
(README claim), also as a midpoint-labelled hypergraph?  (b) Non-load-bearing: re-verify every set in
sets_19_16_8_realizable.json with the referee's own code."""
import json, sys, itertools, re
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/C008')
from refcheck import *
import networkx as nx
from networkx.algorithms import isomorphism as iso

REPO = '/home/user/Erdos-757'
EXP = REPO + '/experiments/20261027-0815-realize-f19'
A = parse(json.load(open(REPO + '/results/claims/C008-f19-h11.json'))['set'])
E = aps(A)

lines_list = [l for l in open(REPO + '/experiments/20261027-0340-induction-n28-n29-f25/lists/cell_19_16_8_D4.txt') if l.startswith('FOUND')]
lines_c19 = [l for l in open(EXP + '/c19_16_8.txt') if l.startswith('FOUND')]
print('cell list FOUND lines', len(lines_list), 'c19_16_8.txt FOUND lines', len(lines_c19), 'identical', lines_list == lines_c19)
def parse_line(l):
    return [tuple(map(int, t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', l)]
cls40 = parse_line(lines_list[40])
print('class 40 edges', len(cls40), cls40)

def incg(edges, mids=None):
    G = nx.Graph()
    for t, e in enumerate(edges):
        G.add_node(('e', t), kind='e')
        for v in e:
            G.add_node(('v', v), kind='v')
            G.add_edge(('e', t), ('v', v), role=('mid' if mids is not None and v == mids[t] else 'end'))
    return G
nm = iso.categorical_node_match('kind', None)
em = iso.categorical_edge_match('role', None)
G_set = incg(E)
G_40 = incg(cls40)
print('unlabelled isomorphic to class 40:', nx.is_isomorphic(G_set, G_40, node_match=nm))
# which classes of the list is it isomorphic to (should be exactly one, the list is one class per line)
hits = [i for i, l in enumerate(lines_list) if nx.is_isomorphic(G_set, incg(parse_line(l)), node_match=nm)]
print('isomorphic list indices', hits)
# labelled: labelling of cls 40 in sets_19_16_8_realizable.json
R = json.load(open(EXP + '/sets_19_16_8_realizable.json'))
print('records in sets_19_16_8_realizable.json', len(R), 'keys', sorted(R[0].keys()))
rec40 = [r for r in R if r['cls'] == 40][0]
print('rec40 set equals claim set', sorted(rec40['set']) == A)
lab = rec40['labelling']
G_set_l = incg(E, mids=[j for _, j, _ in E])
for pos, name in ((1, 'middle entry = midpoint'), (0, 'first entry = midpoint'), (2, 'last entry = midpoint')):
    G_l = incg([tuple(t) for t in lab], mids=[t[pos] for t in lab])
    print('labelled iso (', name, '):', nx.is_isomorphic(G_set_l, G_l, node_match=nm, edge_match=em))

print('-- non-load-bearing: all records in sets_19_16_8_realizable.json')
bad = 0
summary = {}
for r in R:
    B = parse(r['set'])
    EB = aps(B)
    ok45 = is45_bf(B)
    hB = h_numpy(B)
    tB = len(B) - hB
    key = (len(B), ok45, len(EB), hB, linear(EB), f7_homs(len(B), EB) == 0)
    summary[key] = summary.get(key, 0) + 1
    # is its AP hypergraph isomorphic to the listed class?
    isoc = nx.is_isomorphic(incg(EB), incg(parse_line(lines_list[r['cls']])), node_match=nm)
    if not (ok45 and len(B) == 19 and hB == 11 and len(EB) == 16 and isoc):
        bad += 1
        print('PROBLEM', r['cls'], key, isoc)
print('summary (n, is45, m, h, linear, F7free) -> count:', summary, 'problems', bad)
