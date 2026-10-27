"""Side check for Lemma A+ case (beta): with n >= 25 (L021 Thm 7(ii)) case (beta) forces the degree-3 vertex w of F_v
to be a cut vertex of F_v whose non-trace components of F_v - w have >= 25 - 1 - 17 = 7 vertices in total.
List, for each piece with a vertex of degree 3, the component sizes of F - w."""
import pattern_a_ref as R
from rlib import degs
def comps(n, E, removed):
    par = {x: x for x in range(n) if x != removed}
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for e in E:
        if removed in e: continue
        a = f(e[0])
        for y in e[1:]:
            b = f(y)
            if a != b: par[b] = a
    sz = {}
    for x in par:
        r = f(x); sz[r] = sz.get(r, 0) + 1
    return sorted(sz.values(), reverse=True)
cand = 0
for name, (n, E) in R.P.items():
    d = degs(n, E)
    for w in range(n):
        if d[w] == 3:
            cs = comps(n, E, w)
            if len(cs) > 1:
                maxnontrace = n - 1 - min(cs)
                print(name, 'w', w, 'components', cs, 'max non-trace total', maxnontrace, 'OK>=7' if maxnontrace >= 7 else '')
                cand += maxnontrace >= 7
print('pieces/vertices with a degree-3 cut vertex leaving >= 7 vertices outside some component:', cand)
