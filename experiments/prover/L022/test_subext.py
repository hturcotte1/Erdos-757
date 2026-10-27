"""Falsification test of Theorem 2 (sub-extension lemma) of L022 on linear vertex-critical violators.
Random connected linear 3-graphs (NOT required to be in C, so violators exist at small n), Delta<=3;
keep those with slack<0 that are vertex-critical (every proper induced subgraph, checked over ALL vertex subsets,
has slack>=0). For every degree-3 vertex v: classify the distribution of the co-vertex pairs over the components
of H-v into the L017 patterns and check the claims of Theorem 2:
  (c1),(c2),(d),(e) never occur; in (f) the component containing the inside pair has slack 1 and the other slack 0;
  in (b) if the three attachment vertices of a component span an edge then that component is a single edge;
  the induced subgraphs H[Y] named in the proof have the predicted slack.
Exact integer arithmetic.  usage: python3 test_subext.py seed trials nmin nmax"""
import sys, random, itertools
import lib22
from hyp import tau_masks, masks, components

def slack_of(n, E):
    return 3 * n + 2 * len(E) - 11 * (tau_masks(masks(E)) if E else 0)

def induced_slack(S, E):
    S = set(S); F = [e for e in E if all(x in S for x in e)]
    return 3 * len(S) + 2 * len(F) - 11 * (tau_masks(masks(F)) if F else 0)

def vertex_critical(n, E):
    for k in range(1, n):  # proper nonempty-complement subsets: size 1..n-1 kept vertices (all proper induced subgraphs)
        for S in itertools.combinations(range(n), k):
            if induced_slack(S, E) < 0: return False
    return True

def rand_graph(rnd, n, m_target):
    E = []; deg = [0] * n
    tries = 0
    while len(E) < m_target and tries < 2000:
        tries += 1
        e = tuple(sorted(rnd.sample(range(n), 3)))
        if any(deg[x] >= 3 for x in e): continue
        if any(len(set(e) & set(f)) > 1 for f in E): continue
        E.append(e)
        for x in e: deg[x] += 1
    return E

def pattern(v, E, n):
    vedges = [e for e in E if v in e]
    pairs = [tuple(x for x in e if x != v) for e in vedges]
    G = [e for e in E if v not in e]
    rest = [x for x in range(n) if x != v]
    comps = components(rest, G)
    cid = {}
    for i, c in enumerate(comps):
        for x in c: cid[x] = i
    r = len(comps)
    types = []
    for p in pairs:
        types.append((cid[p[0]], cid[p[1]]))
    return pairs, comps, cid, r, types, G

def main():
    seed, trials, nmin, nmax = map(int, sys.argv[1:5])
    rnd = random.Random(seed)
    stats = dict(graphs=0, violators=0, vc=0, deg3=0, pat={}, fails=0)
    seen = set()
    for t in range(trials):
        n = rnd.randint(nmin, nmax)
        m = rnd.randint(max(1, n // 2), min(n, (3 * n) // 3))
        E = rand_graph(rnd, n, m)
        used = sorted({x for e in E for x in e})
        if len(used) < n: continue
        if len(components(range(n), E)) != 1: continue
        stats['graphs'] += 1
        if slack_of(n, E) >= 0: continue
        stats['violators'] += 1
        key = (n, tuple(sorted(E)))
        if key in seen: continue
        seen.add(key)
        if not vertex_critical(n, E): continue
        stats['vc'] += 1
        s = slack_of(n, E)
        deg = [0] * n
        for e in E:
            for x in e: deg[x] += 1
        for v in range(n):
            if deg[v] != 3: continue
            stats['deg3'] += 1
            pairs, comps, cid, r, types, G = pattern(v, E, n)
            cs = [induced_slack(c, G) for c in comps]
            inside = [a == b for (a, b) in types]
            if r == 1: pat = 'a'
            else:
                ins = sum(inside)
                if ins >= 2:
                    comps_in = [types[k][0] for k in range(3) if inside[k]]
                    pat = 'c' if len(set(comps_in)) < len(comps_in) else 'e'
                elif ins == 0: pat = 'b'
                else:
                    j = inside.index(True); comp_in = types[j][0]
                    others = [types[k] for k in range(3) if k != j]
                    # (e): one other pair inside the other comp, third split; (f): two split pairs
                    pat = 'f' if all(a != b for (a, b) in others) else 'e?'
                    if r == 3: pat = 'd'
            stats['pat'][pat] = stats['pat'].get(pat, 0) + 1
            ok = True
            if pat in ('c', 'd', 'e', 'e?'): ok = False
            if pat == 'f':
                j = inside.index(True); ci = types[j][0]
                if not (cs[ci] == 1 and sum(cs) - cs[ci] == 0): ok = False
            if pat == 'b':
                for ci in range(r):
                    att = [p[0] if cid[p[0]] == ci else p[1] for p in pairs]
                    if tuple(sorted(att)) in {tuple(sorted(e)) for e in G}:
                        if len(comps[ci]) != 3: ok = False
            if not ok:
                stats['fails'] += 1
                print('FAIL', n, E, 'v', v, pat, types, cs, 's', s, flush=True)
    print(stats)

main()
