"""Independent exact verification (code written separately from hyp.py / roles.py) of the pattern-(e) graphs K.
For each graph: (1) 3-uniform, distinct edges; (2) linear: |e & f| <= 1; (3) F7-free: brute force over all 5-subsets of edges
(a copy of F7 = 5 edges on 7 vertices with one vertex of degree 3 and six of degree 2, two edges disjoint... we test
isomorphism to {012,034,056,135,246} directly by trying all vertex maps of the 7-vertex union); (4) (P3): for every
pair {x,y} a maximum bipartite matching (networkx Hopcroft-Karp) of the edges into V minus {x,y} saturates all edges;
(5) tau: an explicit transversal of size t is exhibited and verified, and the nonexistence of one of size t-1 is shown by
an independent exhaustive search (recursive: choose an uncovered edge, branch on its vertices, vertices in sorted order);
(6) connectivity and max degree.  Usage: python3 verify_K29.py <json>"""
import sys, json, itertools
import networkx as nx
from networkx.algorithms import bipartite

F7 = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(2,4,6)]
F7s = set(frozenset(e) for e in F7)

def linear(E):
    S = [set(e) for e in E]
    return all(len(S[i] & S[j]) <= 1 for i in range(len(S)) for j in range(i+1, len(S)))

def has_F7(E):
    for sub in itertools.combinations(E, 5):
        V = sorted(set(x for e in sub for x in e))
        if len(V) != 7: continue
        deg = {x: sum(1 for e in sub if x in e) for x in V}
        if sorted(deg.values()) != [2,2,2,2,2,2,3]: continue
        subs = set(frozenset(e) for e in sub)
        for perm in itertools.permutations(V):
            mp = dict(zip(range(7), perm))
            if all(frozenset(mp[x] for x in e) in subs for e in F7): return True
    return False

def p3(n, E):
    for x in range(n):
        for y in range(x+1, n):
            G = nx.Graph(); L = [('e', i) for i in range(len(E))]
            G.add_nodes_from(L, bipartite=0)
            G.add_nodes_from([('v', u) for u in range(n) if u not in (x, y)], bipartite=1)
            for i, e in enumerate(E):
                for u in e:
                    if u not in (x, y): G.add_edge(('e', i), ('v', u))
            M = bipartite.hopcroft_karp_matching(G, top_nodes=L)
            if sum(1 for k in M if k[0] == 'e') < len(E): return False
    return True

def exists_transversal(E, k):
    """is there a transversal with at most k vertices?  plain exhaustive branching."""
    def rec(rem, k):
        if not rem: return True
        if k == 0: return False
        e = rem[0]
        for u in sorted(e):
            if rec([f for f in rem if u not in f], k - 1): return True
        return False
    return rec([tuple(e) for e in E], k)

def find_transversal(E, k):
    def rec(rem, k, ch):
        if not rem: return ch
        if k == 0: return None
        for u in sorted(rem[0]):
            r = rec([f for f in rem if u not in f], k - 1, ch + [u])
            if r is not None: return r
        return None
    return rec([tuple(e) for e in E], k, [])

def connected(n, E):
    G = nx.Graph(); G.add_nodes_from(range(n))
    for e in E: G.add_edge(e[0], e[1]); G.add_edge(e[1], e[2])
    return nx.is_connected(G)

if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else len(data)
    ok = 0
    for d in data[:lim]:
        n, E, t = d['n'], [tuple(e) for e in d['edges']], d['tau']
        assert all(len(set(e)) == 3 for e in E) and len(set(frozenset(e) for e in E)) == len(E)
        assert max(max(e) for e in E) == n - 1
        deg = [sum(1 for e in E if x in e) for x in range(n)]
        T = find_transversal(E, t)
        res = dict(linear=linear(E), F7free=not has_F7(E), P3=p3(n, E), Tsize_t=(T is not None and all(any(u in T for u in e) for e in E)),
                   no_t_minus_1=not exists_transversal(E, t - 1), connected=connected(n, E), maxdeg=max(deg), mindeg=min(deg))
        s = 3 * n + 2 * len(E) - 11 * t
        good = res['linear'] and res['F7free'] and res['P3'] and res['Tsize_t'] and res['no_t_minus_1'] and res['connected'] and res['maxdeg'] <= 3
        ok += good
        print(n, len(E), t, 'slack', s, res, 'OK' if good else 'FAIL', flush=True)
    print('verified', ok, 'of', lim)
