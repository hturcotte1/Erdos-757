s=open('structure.py').read()
s=s.replace("print('candidates', len(cands), flush=True)","""def conn(n, es):
    par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for e in es:
        for v in e[1:]: par[f(v)] = f(e[0])
    return len(set(v for e in es for v in e)) == n and len(set(f(v) for v in range(n))) == 1
cands = {k: v for k, v in cands.items() if conn(v[1], v[2])}
print('candidates (connected)', len(cands), flush=True)""")
open('structure.py','w').write(s)
