"""Referee L023 round 1 (own code): for every X_i and every vertex w of degree 4, the component types (n,m,tau) of X_i - w;
for the 14-vertex 12-edge components: Q8 containment and my generic realizability decision (Step 3.5 of the certificate)."""
import json
import hg_checks as H, realize_generic as R
L = [H.parse(l) for l in open('six_from_certificate.txt')]
def comps(E, V):
    adj = {v: set() for v in V}
    for e in E:
        for v in e: adj[v] |= set(e) - {v}
    seen = set(); out = []
    for s in V:
        if s in seen: continue
        st = [s]; seen.add(s); C = {s}
        while st:
            v = st.pop()
            for u in adj[v]:
                if u not in seen: seen.add(u); C.add(u); st.append(u)
        out.append(sorted(C))
    return out
done = {}
for i, E in enumerate(L):
    d = H.deg(E, 25)
    for w in [v for v in range(25) if d[v] == 4]:
        F = [e for e in E if w not in e]; V = [v for v in range(25) if v != w]
        types = []
        for C in comps(F, V):
            FE = [e for e in F if e[0] in C]
            types.append((len(C), len(FE), H.tau(FE)[0] if FE else 0))
            if (len(C), len(FE)) == (14, 12):
                mp = {v: j for j, v in enumerate(C)}; K = [tuple(sorted(mp[v] for v in e)) for e in FE]
                key = tuple(sorted(K))
                ok, st, _ = R.decide(K, 14)
                print('X_%d w=%d (14,12) component: contains Q8 %s, generic decision %s nodes %d' % (i, w, len(H.q8_embeddings(K)) > 0, 'REALIZABLE' if ok else 'NOT-REALIZABLE', st['nodes']), flush=True)
        print('X_%d w=%d components of X-w:' % (i, w), sorted(types, reverse=True), flush=True)
