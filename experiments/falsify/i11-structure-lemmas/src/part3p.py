"""Pattern-level (mask) analysis of minimal covers whose components all have exactly two pair endpoints.
For a comp item and ordered vertex pair (u,w) the relation R(u,w) subset of {0,1}^2 = membership patterns of (u,w) over maximum independent sets.
Triangle (k=3, three comps) and 4-cycle (k=4, four comps) shapes: unsat iff no pattern choice avoids all pairs."""
import sys, json, itertools, collections, time, os
sys.path.insert(0,'src')
from part3a import *
lib=load_library()
if os.path.exists('part3a_results.json'):
    for i,g in enumerate(json.load(open('part3a_results.json'))['graphs']):
        lib.append(Comp('gen%d_%d#%d'%(g['n'],i,i),g['n'],[tuple(e) for e in g['edges']]))
# masks per item
maskcount=[collections.Counter() for _ in lib]
tuples=[collections.defaultdict(list) for _ in lib]
for ii,c in enumerate(lib):
    bits=[(c.mis>>v)&1 for v in range(c.n)]
    for u in range(c.n):
        for w in range(c.n):
            if u==w: continue
            pat=set(zip(bits[u].tolist(),bits[w].tolist()))
            mask=sum(1<<(2*a+b) for a,b in pat)   # bit index 2*x_u + x_w
            maskcount[ii][mask]+=1
            tuples[ii][mask].append((u,w))
allmasks=sorted({m for mc in maskcount for m in mc})
print('distinct masks over all items/ordered pairs:',[(bin(m)) for m in allmasks])
# R as set of (xu,xw)
def rel(mask): return [(a,b) for a in (0,1) for b in (0,1) if mask>>(2*a+b)&1]
RL={m:rel(m) for m in allmasks}
# which items have each mask
byMask=collections.defaultdict(set)
for ii,mc in enumerate(maskcount):
    for m in mc: byMask[m].add(ii)
# cycle of length c: comp j has endpoints (first_j, second_j); pair joins second_j with first_{j+1}. avoid: not(second_j and first_{j+1})
def cycle_unsat(masks):
    c=len(masks)
    # exists choice (xf_j,xs_j) in rel(masks[j]) with not(xs_j and xf_{j+1})
    # DP around cycle
    for start in RL[masks[0]]:
        # state: xs of current comp ; start comp chosen as 'start'
        cur={start[1]}
        for j in range(1,c):
            nxt=set()
            for (xf,xs) in RL[masks[j]]:
                if any(not(prev and xf) for prev in cur): nxt.add(xs)
            cur=nxt
            if not cur: break
        if cur and any(not(xs and start[0]) for xs in cur): return False
    return True
res={}
for c in (2,3,4):
    uns=[]
    for masks in itertools.product(allmasks,repeat=c):
        if cycle_unsat(masks): uns.append(masks)
    # canonical up to rotation
    canon={min(tuple(m[i:]+m[:i]) for i in range(c)) for m in uns}
    res[c]=[[bin(x) for x in m] for m in sorted(canon)]
    print('cycle length',c,'unsat mask cycles (up to rotation):',len(canon))
    # realisable by items? the item must have the mask
    out=[]
    for m in sorted(canon):
        sets=[byMask[x] for x in m]
        out.append((m,[len(s) for s in sets]))
    res['items_%d'%c]=[( [bin(x) for x in m], l) for m,l in out]
    for m,l in out[:12]: print('  ',[bin(x) for x in m],l)
json.dump(res,open('part3p_out.json','w'))
