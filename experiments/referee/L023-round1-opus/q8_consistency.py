"""Referee L023 round 1: consistency of Proposition 6 with known realizable sets (own code): the AP hypergraph of a (4,5)-set
must not contain Q8. Checked on A_base, all judged claim sets C001-C008, the small records of data/small_records.json; and Q8 in
classes 5 and 7 of the refereed cell(14,12,6,4) (Step 3.6 of the certificate)."""
import json, glob, itertools, re
import hg_checks as H
def ap_graph(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return [(i, idx[(A[i] + A[k]) // 2], k) for i in range(len(A)) for k in range(i + 1, len(A)) if (A[i] + A[k]) % 2 == 0 and (A[i] + A[k]) // 2 in idx]
sets = {'A_base': [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]}
for f in sorted(glob.glob('/home/user/Erdos-757/results/claims/C*.json')):
    d = json.load(open(f)); sets[d['id']] = d['set']
rec = json.load(open('/home/user/Erdos-757/data/small_records.json'))['sets']
for k, v in rec.items():
    s = v['set'] if isinstance(v, dict) and 'set' in v else v
    if isinstance(s, list) and s and isinstance(s[0], int): sets['small_records_' + k] = s
    elif isinstance(s, list):
        for j, t in enumerate(s):
            if isinstance(t, list): sets['small_records_%s_%d' % (k, j)] = t
for name, A in sets.items():
    E = ap_graph(A)
    print(name, 'n=%d m=%d' % (len(A), len(E)), 'contains Q8:', len(H.q8_embeddings(E)) > 0)
L = [H.parse(l) for l in open('cell_14_12_6_D4_refereed.txt')]
for i in (5, 7):
    E = L[i]; emb = H.q8_embeddings(E)
    print('cell(14,12,6,4) class', i, 'Q8 embeddings', len(emb), 'vertex sets', sorted(set(tuple(sorted(e.values())) for e in emb)))
print('other classes of cell(14,12,6,4) containing Q8:', [i for i in range(len(L)) if i not in (5, 7) and H.q8_embeddings(L[i])])
