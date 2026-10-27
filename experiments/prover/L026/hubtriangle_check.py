"""L026 C10: which members of L* contain a 'hub triangle' T_hub: distinct vertices x,y,z,v,b,c with edges
{x,y,z}, {v,y,b}, {v,z,c} and degrees d(x)=1, d(y)=d(z)=d(v)=2 (the structure that the component C_hub of H-a
must contain in Theorem 12(e)(alpha))?  Also lists, for each piece, its E1-hubs for comparison."""
import sys, itertools
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L026')
import ownlib as L
tot = 0
for P in L.load_pieces():
    Es = [tuple(sorted(e)) for e in P.E]
    inc = [[] for _ in range(P.n)]
    for e in Es:
        for u in e: inc[u].append(e)
    found = []
    for e0 in Es:
        for x in e0:
            if P.deg[x] != 1: continue
            y, z = [u for u in e0 if u != x]
            for (yy, zz) in ((y, z), (z, y)):
                if P.deg[yy] != 2 or P.deg[zz] != 2: continue
                eb = [e for e in inc[yy] if e != e0][0]
                ec = [e for e in inc[zz] if e != e0][0]
                common = set(eb) & set(ec)
                if len(common) != 1: continue
                v = common.pop()
                if v in e0 or P.deg[v] != 2: continue
                b = [u for u in eb if u not in (v, yy)][0]
                c = [u for u in ec if u not in (v, zz)][0]
                if len({x, yy, zz, v, b, c}) == 6:
                    found.append((x, yy, zz, v, b, c))
    tot += len(found)
    print(P.name, 'hub triangles with d(x)=1, d(y)=d(z)=d(v)=2:', len(found), found[:3])
print('TOTAL', tot)
