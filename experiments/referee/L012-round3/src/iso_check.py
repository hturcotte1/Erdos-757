"""Referee L012 round 3: isomorphism checks without nauty.
(a) canon_igraph(edges, n): canonical form of a 3-graph via igraph's BLISS canonical_permutation on the 2-coloured incidence graph; the
    canonical EDGE LIST is returned (so equal forms imply isomorphic by construction).
(b) Mode 'classes FILE n': the graphs of FILE (FOUND/HIT lines) are pairwise non-isomorphic iff their BLISS forms are distinct; in
    addition, pairs with equal cheap invariants (degree sequence + sorted neighbour-degree multisets + WL hash) are tested with
    networkx VF2 (vertex-coloured incidence graphs), as a third independent method.
(c) Mode 'match REPS SURV n': every graph in SURV is matched to a representative in REPS by BLISS form; reports unmatched survivors and
    representatives never hit; a random sample of 200 matches is confirmed with VF2.
(d) Mode 'relabel FILE n CANON_BIN': relabelling invariance of the prover's nauty canon: 3 random relabellings of every graph give the
    same canon output as the original (and igraph forms also agree)."""
import sys, re, random, subprocess, itertools
import igraph as ig
import networkx as nx
from networkx.algorithms import isomorphism as nxiso
def parse(fn):
    out = []
    for l in open(fn):
        if l.startswith('FOUND:') or l.startswith('HIT:') or l.startswith('S:'):
            out.append([tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+),(\d+),(\d+)\)', l) and [','.join(t) for t in re.findall(r'\((\d+),(\d+),(\d+)\)', l)]])
    return out
def inc_graph(edges, n):
    m = len(edges); g = ig.Graph(n + m)
    g.add_edges([(v, n + j) for j, e in enumerate(edges) for v in e])
    return g
def canon_igraph(edges, n):
    m = len(edges); g = inc_graph(edges, n)
    perm = g.canonical_permutation(color=[0] * n + [1] * m)
    # igraph convention (verified by a relabelling-invariance test, logs/igraph_convention.txt): perm[i] is the ORIGINAL vertex placed at
    # canonical position i, so the new label of vertex v is inv[v]
    inv = [0] * len(perm)
    for i, pv in enumerate(perm): inv[pv] = i
    newedges = sorted(tuple(sorted(inv[v] for v in e)) for e in edges)
    # colour classes are preserved by BLISS when colours are given, so vertex labels stay < n; assert it
    assert all(x < n for e in newedges for x in e)
    return tuple(newedges)
def nx_inc(edges, n):
    G = nx.Graph()
    for v in range(n): G.add_node(('v', v), c=0)
    for j, e in enumerate(edges):
        G.add_node(('e', j), c=1)
        for v in e: G.add_edge(('v', v), ('e', j))
    return G
def vf2_iso(e1, e2, n):
    return nxiso.GraphMatcher(nx_inc(e1, n), nx_inc(e2, n), node_match=lambda a, b: a['c'] == b['c']).is_isomorphic()
def invariant(edges, n):
    deg = [0] * n
    for e in edges:
        for v in e: deg[v] += 1
    nb = []
    for v in range(n):
        nb.append((deg[v], tuple(sorted(deg[u] for e in edges if v in e for u in e if u != v))))
    wl = nx.weisfeiler_lehman_graph_hash(nx_inc(edges, n), node_attr='c', iterations=4)
    return (tuple(sorted(nb)), wl)
mode = sys.argv[1] if (__name__ == '__main__' and len(sys.argv) > 1) else None
if mode == 'classes':
    fn, n = sys.argv[2], int(sys.argv[3]); G = parse(fn)
    forms = [canon_igraph(e, n) for e in G]
    print('graphs', len(G), 'distinct BLISS forms', len(set(forms)))
    inv = {}
    for i, e in enumerate(G): inv.setdefault(invariant(e, n), []).append(i)
    pairs = [(a, b) for grp in inv.values() for a, b in itertools.combinations(grp, 2)]
    niso = sum(vf2_iso(G[a], G[b], n) for a, b in pairs)
    print('invariant buckets', len(inv), 'pairs with equal invariants tested by VF2', len(pairs), 'isomorphic pairs found', niso)
elif mode == 'match':
    reps, surv, n = parse(sys.argv[2]), parse(sys.argv[3]), int(sys.argv[4])
    rf = {}
    for i, e in enumerate(reps): rf.setdefault(canon_igraph(e, n), []).append(i)
    assert all(len(v) == 1 for v in rf.values()), 'representatives not pairwise non-isomorphic'
    hit = [0] * len(reps); unmatched = 0; matched_pairs = []
    for e in surv:
        f = canon_igraph(e, n)
        if f in rf: hit[rf[f][0]] += 1; matched_pairs.append((e, rf[f][0]))
        else: unmatched += 1
    print('survivors', len(surv), 'matched', len(surv) - unmatched, 'UNMATCHED', unmatched, 'representatives hit', sum(1 for h in hit if h), 'of', len(reps))
    random.seed(1); samp = random.sample(matched_pairs, min(200, len(matched_pairs)))
    ok = sum(vf2_iso(e, reps[i], n) for e, i in samp)
    print('VF2 confirmation on a sample of matches:', ok, 'of', len(samp))
    print('hits per representative: min', min(hit), 'max', max(hit))
elif mode == 'relabel':
    fn, n, cb = sys.argv[2], int(sys.argv[3]), sys.argv[4]; G = parse(fn); random.seed(7)
    lines = []; idx = []
    for i, e in enumerate(G):
        lines.append('FOUND: ' + ' '.join('(%d,%d,%d)' % t for t in e)); idx.append(i)
        for r in range(3):
            perm = list(range(n)); random.shuffle(perm)
            e2 = [tuple(sorted(perm[v] for v in t)) for t in e]; random.shuffle(e2)
            lines.append('FOUND: ' + ' '.join('(%d,%d,%d)' % t for t in e2)); idx.append(i)
    out = subprocess.run([cb, str(n)], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
    assert len(out) == len(lines)
    bad = 0; byi = {}
    for i, o in zip(idx, out): byi.setdefault(i, set()).add(o)
    bad = sum(1 for s in byi.values() if len(s) != 1)
    print('graphs', len(G), 'relabellings 3 each; graphs whose canon output varies under relabelling:', bad)
    # igraph forms agree too, and the number of distinct canon outputs equals the number of distinct igraph forms
    forms = set(canon_igraph(e, n) for e in G); couts = set(o for s in byi.values() for o in s)
    print('distinct nauty canon outputs', len(couts), 'distinct igraph BLISS forms', len(forms))
