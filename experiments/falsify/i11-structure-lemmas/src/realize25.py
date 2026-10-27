import sys, json, itertools, time
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'src')
from e757.saturated import solve_midpoint_map, check_values, to_integers
from fractions import Fraction
gs=json.load(open(sys.argv[1]))['graphs']
n=int(sys.argv[2]); tl=float(sys.argv[3])
t0=time.time()
def matchings(edges,lo,hi):
    # assign each edge a distinct midpoint vertex in it, not lo/hi; cover all non-extreme vertices
    m=len(edges); res=[]
    used=set(); assign=[None]*m
    order=sorted(range(m),key=lambda i:sum(1 for v in edges[i] if v not in (lo,hi)))
    def rec(k):
        if k==m: res.append(list(assign)); return
        i=order[k]
        for v in edges[i]:
            if v in (lo,hi) or v in used: continue
            used.add(v); assign[i]=v; rec(k+1); used.discard(v)
    rec(0)
    return res
out=[]
for gi,g in enumerate(gs):
    es=[tuple(e) for e in g['edges']]
    nmatch=0; nsolved=0; nvalid=0; found=[]
    for lo,hi in itertools.combinations(range(n),2):
        # lo, hi must be non-midpoints; they may be any vertices
        ms=matchings(es,lo,hi)
        nmatch+=len(ms)
        for a in ms:
            mid={}
            for i,v in enumerate(a):
                others=[w for w in es[i] if w!=v]; mid[v]=(others[0],others[1])
            vals=solve_midpoint_map(n,lo,hi,mid)
            if vals is None: continue
            nsolved+=1
            if len(set(vals))<n: continue
            edges=[(i,j,k) for j,(i,k) in mid.items()]
            ok,reason=check_values(vals,edges)
            if ok:
                nvalid+=1; found.append(to_integers(vals))
                print('REALIZED',gi,lo,hi,to_integers(vals),flush=True)
        if time.time()-t0>tl: break
    print('graph',gi,'labelings',nmatch,'solved',nsolved,'valid',nvalid,round(time.time()-t0),flush=True)
    out.append({'graph':gi,'labelings':nmatch,'solved':nsolved,'valid':nvalid,'sets':found})
json.dump(out,open('realize_%d.json'%n,'w'))
