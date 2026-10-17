"""Referee L007 r2: two F7 detectors written from the definition, plus controls.
F7 = {012,034,056,135,246}.  H contains F7 iff some 5 edges of H form a (partial) subhypergraph isomorphic to F7.
 det_A: for every 5-subset of edges with a 7-vertex union, relabel the union increasingly and test membership in
        the set of all labelled copies of F7 on {0..6} (all 5040 permutations applied to F7).
 det_B: networkx subgraph MONOmorphism of the (typed) vertex-edge incidence graph of F7 into that of H.
Neither uses the degree-pattern Lemma F of the certificate."""
import itertools, re, sys, json, random
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
COPIES = set()
for p in itertools.permutations(range(7)):
    COPIES.add(frozenset(tuple(sorted(p[v] for v in e)) for e in F7))
def det_A(es):
    es = [tuple(sorted(e)) for e in es]
    for five in itertools.combinations(es, 5):
        U = sorted(set().union(*five))
        if len(U) != 7: continue
        r = {v: i for i, v in enumerate(U)}
        if frozenset(tuple(sorted(r[v] for v in e)) for e in five) in COPIES: return True
    return False
def inc(es):
    G = nx.Graph()
    for i, e in enumerate(es):
        G.add_node(('e', i), t='e')
        for v in e:
            G.add_node(('v', v), t='v'); G.add_edge(('e', i), ('v', v))
    return G
F7INC = inc(F7)
def det_B(es):
    GM = GraphMatcher(inc(es), F7INC, node_match=lambda a, b: a['t'] == b['t'])
    return GM.subgraph_is_monomorphic()
def is_linear(es):
    seen = set()
    for e in es:
        for p in itertools.combinations(sorted(e), 2):
            if p in seen: return False
            seen.add(p)
    return True
def parse(path, tag):
    out = []
    for l in open(path):
        if l.startswith(tag):
            out.append([tuple(sorted(int(x) for x in t.split(','))) for t in re.findall(r'\(([0-9,]+)\)', l)])
    return out
def controls():
    res = {}
    assert len(COPIES) == 420, len(COPIES)
    res['labelled_F7_copies_on_7'] = len(COPIES)
    # AG(2,3): points Z3^2, lines {p + t d}
    pts = [(a, b) for a in range(3) for b in range(3)]; idx = {p: i for i, p in enumerate(pts)}
    lines = set()
    for p in pts:
        for d in [(0,1),(1,0),(1,1),(1,2)]:
            lines.add(tuple(sorted(idx[((p[0]+t*d[0]) % 3, (p[1]+t*d[1]) % 3)] for t in range(3))))
    AG = sorted(lines); assert len(AG) == 12
    AG_m1 = [e for e in AG if 8 not in e]
    AG_m2 = [e for e in AG if 8 not in e and 7 not in e]
    fano = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    fano_m2 = [e for e in fano if e not in [(0,1,2),(0,3,4)]]
    L13 = sorted(tuple(sorted(((i) % 13, (i+1) % 13, (i+3) % 13))) for i in range(13))
    D14 = [(0,1,2),(3,5,6),(0,3,13),(1,5,13),(2,6,13),(4,7,8),(4,9,10),(7,9,11),(8,9,12),(10,11,12),(2,3,4)]
    rng = random.Random(1)
    perm = list(range(20)); rng.shuffle(perm)
    F7_relab = [tuple(sorted(perm[v] for v in e)) for e in F7]
    F7_minus = F7[:4]
    pos = dict(F7=F7, F7_relabelled=F7_relab, AG23=AG, AG23_minus1=AG_m1, AG23_minus2=AG_m2, D14=D14)
    neg = dict(Fano=fano, Fano_minus2lines=fano_m2, F7_minus_edge=F7_minus, L13=L13,
               cycle5=[(0,1,2),(2,3,4),(4,5,6),(6,7,8),(8,9,0)], star4=[(0,1,2),(0,3,4),(0,5,6),(0,7,8)])
    for k, es in pos.items():
        a, b = det_A(es), det_B(es); res['pos_' + k] = (a, b, is_linear(es)); assert a and b, k
    for k, es in neg.items():
        a, b = det_A(es), det_B(es); res['neg_' + k] = (a, b, is_linear(es)); assert not a and not b, k
    # exhaustive agreement on all labelled linear 5-edge 3-graphs whose union is [7]
    T = list(itertools.combinations(range(7), 3)); tot = 0; f7 = 0
    for five in itertools.combinations(T, 5):
        if set().union(*five) != set(range(7)) or not is_linear(five): continue
        tot += 1; a = det_A(five); b = det_B(list(five)); assert a == b; f7 += a
    res['all_linear_5edge_spanning_7'] = (tot, f7)
    # random linear 3-graphs on 9..12 vertices: agreement A vs B
    agree = 0; withf7 = 0
    for trial in range(400):
        n = rng.randint(7, 12); es = []
        for _ in range(200):
            e = tuple(sorted(rng.sample(range(n), 3)))
            if e not in es and is_linear(es + [e]): es.append(e)
            if len(es) >= rng.randint(5, 12): break
        a, b = det_A(es), det_B(es); assert a == b, es; agree += 1; withf7 += a
    res['random_agreement'] = (agree, withf7)
    return res
if __name__ == '__main__':
    r = controls(); print(json.dumps(r))
    rep = {}
    for arg in sys.argv[1:]:
        path, tag = arg.rsplit(':', 1)
        L = parse(path, tag + ':')
        lin = sum(is_linear(es) for es in L)
        a = [det_A(es) for es in L]
        b = [det_B(es) for es in L]
        assert a == b
        rep[path] = dict(graphs=len(L), distinct=len({frozenset(es) for es in L}), linear=lin, contain_F7=sum(a), F7_free=len(L) - sum(a))
        print(path, rep[path], flush=True)
    json.dump(dict(controls=r, lists=rep), open('f7_ref_results.json', 'w'), indent=1)
