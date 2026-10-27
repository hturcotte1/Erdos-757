"""(L023) Classify every extension printed by `ext_d ... noprune` (no F7 pruning, no (P3) test) with the own verifier verify_c.py
(independent of filt and pyverify), in the order: linear, F7-free, (P3), connected on 25 vertices, Delta <= D, tau = 11 exactly (and, for every SAMPLE-th extension, tau >= 11 re-checked);
the members of C(25,23,11,D) are reduced to isomorphism classes by networkx (VF2 on incidence graphs, independent of nauty) and
compared with the stored list.   usage: python3 classify_final.py NOPRUNE_FILE D LISTFILE [SAMPLE]"""
import sys, re, json, collections
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from verify_c import linear, has_F7, p3, connected, tau_exact, degrees
import networkx as nx
from networkx.algorithms import isomorphism as iso
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def inc(E, n):
    G = nx.Graph()
    for i in range(n): G.add_node(('v', i), side='v')
    for j, e in enumerate(E):
        G.add_node(('e', j), side='e')
        for v in e: G.add_edge(('v', v), ('e', j))
    return G
fn, D, lst = sys.argv[1], int(sys.argv[2]), sys.argv[3]; SAMPLE = int(sys.argv[4]) if len(sys.argv) > 4 else 10
n = 25
cnt = collections.Counter(); members = []
for l in open(fn):
    if not l.startswith('HIT'): continue
    E = parse(l); cnt['extensions'] += 1
    assert len(E) == 23 and all(max(e) < n for e in E)
    if cnt['extensions'] % SAMPLE == 1:   # every SAMPLE-th extension: tau >= 11 re-checked exactly (no cover of size 10)
        assert tau_exact(E, n)[0] >= 11, 'extension with tau < 11'; cnt['tau_rechecked'] += 1
    if not linear(E): cnt['nonlinear'] += 1; continue
    if has_F7(E, n): cnt['F7'] += 1; continue
    if not p3(E, n): cnt['P3_violated'] += 1; continue
    if not connected(E, n): cnt['disconnected_member_of_C'] += 1; continue
    if max(degrees(E, n)) > D: cnt['degree'] += 1; continue
    t = tau_exact(E, n)[0]
    if t != 11: cnt['tau_not_11'] += 1; continue
    cnt['member_of_C(25,23,11,%d)' % D] += 1; members.append(E)
nm = iso.categorical_node_match('side', None)
reps = []
for E in members:
    G = inc(E, n)
    if not any(nx.is_isomorphic(G, H, node_match=nm) for H in reps): reps.append(G)
L = [inc(parse(l), n) for l in open(lst) if l.startswith('FOUND:')]
match = [sum(1 for H in L if nx.is_isomorphic(G, H, node_match=nm)) for G in reps]
cover = [any(nx.is_isomorphic(G, H, node_match=nm) for G in reps) for H in L]
print('SUMMARY', json.dumps(dict(cnt)), 'classes_found', len(reps), 'stored_list_classes', len(L),
      'each_found_class_in_list', all(x == 1 for x in match), 'each_list_class_found', all(cover))
