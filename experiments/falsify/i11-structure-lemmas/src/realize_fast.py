import sys, json, itertools, time
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'src')
import numpy as np
from e757.saturated import solve_midpoint_map, check_values, to_integers
gs=json.load(open(sys.argv[1]))['graphs']
n=int(sys.argv[2]); tl=float(sys.argv[3])
t0=time.time()
def matchings(edges,lo,hi):
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
    want={frozenset(e) for e in es}
    nmatch=0; nsing=0; nfloat_ok=0; nexact=0; found=[]; pairs_done=0
    for lo,hi in itertools.combinations(range(n),2):
        ms=matchings(es,lo,hi)
        nmatch+=len(ms)
        unknown=[v for v in range(n) if v not in (lo,hi)]
        col={v:c for c,v in enumerate(unknown)}
        for a in ms:
            A=np.zeros((n-2,n-2)); b=np.zeros(n-2)
            for i,v in enumerate(a):
                o=[w for w in es[i] if w!=v]
                r=col[v]; A[r,r]+=2
                for w in o:
                    if w==hi: b[r]+=1
                    elif w!=lo: A[r,col[w]]-=1
            try: x=np.linalg.solve(A,b)
            except np.linalg.LinAlgError: nsing+=1; continue
            vals=np.zeros(n); vals[hi]=1.0
            for v in unknown: vals[v]=x[col[v]]
            s=np.sort(vals)
            if (np.diff(s)<1e-9).any(): continue
            # float AP set
            sums={}
            ok=True
            ap=set()
            for i in range(n):
                for k in range(i+1,n):
                    mid=(vals[i]+vals[k])/2
                    j=np.searchsorted(s,mid-1e-9)
                    if j<n and abs(s[j]-mid)<1e-9:
                        jj=int(np.where(vals==s[j])[0][0]); ap.add(frozenset((i,jj,k)))
            if ap!=want: continue
            nfloat_ok+=1
            mid={}
            for i,v in enumerate(a):
                o=[w for w in es[i] if w!=v]; mid[v]=(o[0],o[1])
            vv=solve_midpoint_map(n,lo,hi,mid)
            if vv is None: continue
            ok2,reason=check_values(vv,[(i,j,k) for j,(i,k) in mid.items()])
            nexact+=1
            if ok2:
                found.append(to_integers(vv)); print('REALIZED',gi,lo,hi,to_integers(vv),flush=True)
        pairs_done+=1
        if time.time()-t0>tl*(gi+1)/len(gs): break
    print('graph',gi,'extreme pairs scanned',pairs_done,'of',n*(n-1)//2,'labelings',nmatch,'singular',nsing,'float-AP-consistent',nfloat_ok,'exact-checked',nexact,'realized',len(found),round(time.time()-t0),flush=True)
    out.append({'graph':gi,'pairs_scanned':pairs_done,'labelings':nmatch,'float_ap_consistent':nfloat_ok,'realized':found})
    json.dump(out,open('realize_fast_%d.json'%n,'w'))
