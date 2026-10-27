"""Phase M: minimal covering clusters. A cluster = multiset W of tight comps + k pairs (k<=4) such that every maximum-independent-set tuple of W
contains one of the pairs, minimal under deleting pairs, pair graph connected, every comp has >=2 pair endpoints, class-C counting k<=sum(def)-1."""
import sys, json, itertools, collections, time
sys.path.insert(0,'src')
from part3a import *

def deff(c): return c.n-c.m

def minimal_covers(comps,k,max_nodes=5_000_000):
    ncomp=len(comps)
    comp_of=[];local=[]
    for ci,c in enumerate(comps):
        for x in range(c.n): comp_of.append(ci); local.append(x)
    NQ=len(comp_of)
    total=1
    for c in comps: total*=c.nmis
    pairs=[]
    for u in range(NQ):
        for w in range(u+1,NQ):
            if comp_of[u]==comp_of[w] and (local[u],local[w]) in comps[comp_of[u]].pairs_in_edge: continue
            pairs.append((u,w))
    def joint(vs):
        byc={}
        for v in vs: byc[comp_of[v]]=byc.get(comp_of[v],0)|(1<<local[v])
        r=1
        for ci,c in enumerate(comps):
            r*= c.cnt(byc[ci]) if ci in byc else c.nmis
        return r
    pc=[joint(p) for p in pairs]
    order=sorted(range(len(pairs)),key=lambda i:-pc[i])
    pairs=[pairs[i] for i in order]; pc=[pc[i] for i in order]
    P=len(pairs)
    memo={}
    def cover(S):
        key=tuple(S)
        r=memo.get(key)
        if r is not None: return r
        tot=0
        for r_ in range(1,len(S)+1):
            for sub in itertools.combinations(S,r_):
                vs=set()
                for i in sub: vs.update(pairs[i])
                tot+=(-1)**(r_+1)*joint(vs)
        memo[key]=tot
        return tot
    found=[]; nodes=0
    def structure(S):
        par=list(range(ncomp)); ep=[0]*ncomp
        def f(x):
            while par[x]!=x: par[x]=par[par[x]]; x=par[x]
            return x
        for i in S:
            u,w=pairs[i]; par[f(comp_of[u])]=f(comp_of[w]); ep[comp_of[u]]+=1; ep[comp_of[w]]+=1
        g=len({f(x) for x in range(ncomp)})
        need=sum(max(0,2-e) for e in ep)
        return g,need
    def dfs(start,S,usedv,k_rem):
        nonlocal nodes
        nodes+=1
        if nodes>max_nodes: raise RuntimeError('node limit')
        g,need=structure(S)
        if g-1>k_rem or need>2*k_rem: return
        cv=cover(S) if S else 0
        if k_rem==0:
            if cv==total and g==1 and need==0: found.append(list(S))
            return
        if cv==total: return   # a smaller cover exists: not minimal at size k
        for i in range(start,P):
            if cv+k_rem*pc[i]<total: break
            u,w=pairs[i]
            if u in usedv or w in usedv: continue
            usedv.add(u);usedv.add(w); S.append(i)
            dfs(i+1,S,usedv,k_rem-1)
            S.pop(); usedv.discard(u);usedv.discard(w)
    dfs(0,[],set(),k)
    # minimality: no proper subset covers
    out=[]
    for S in found:
        if all(cover([j for j in S if j!=i])<total for i in S):
            out.append([pairs[i] for i in S])
    return out,nodes

def comp_multisets(lib,c,maxtotal):
    L=sorted(range(len(lib)),key=lambda i:(lib[i].n,i))
    res=[]
    def rec(start,cur,tot):
        if len(cur)==c: res.append(tuple(cur)); return
        for kk in range(start,len(L)):
            i=L[kk]
            if tot+lib[i].n>maxtotal: break
            cur.append(i); rec(kk,cur,tot+lib[i].n); cur.pop()
    rec(0,[],0)
    return res

if __name__=='__main__':
    kk=int(sys.argv[1]); maxtotal=int(sys.argv[2]); tlimit=float(sys.argv[3])
    lib=load_library()
    import os
    if os.path.exists('part3a_results.json'):
        for i,g in enumerate(json.load(open('part3a_results.json'))['graphs']):
            lib.append(Comp('gen%d_%d#%d'%(g['n'],i,i),g['n'],[tuple(e) for e in g['edges']]))
    t0=time.time(); report=[]; done=0; trunc=0; hits=[]
    for c in range(1,kk+1):
        for idxs in comp_multisets(lib,c,maxtotal):
            comps=[lib[i] for i in idxs]
            if sum(deff(x) for x in comps)<kk+1: continue
            if time.time()-t0>tlimit: print('TIME LIMIT'); break
            try:
                covs,nodes=minimal_covers(comps,kk)
            except RuntimeError:
                trunc+=1; report.append({'W':[x.name for x in comps],'truncated':True}); continue
            done+=1
            if covs:
                hits.append({'W':[x.name for x in comps],'k':kk,'covers':covs})
                print('MINIMAL COVER',[x.name for x in comps],len(covs),flush=True)
    print('k',kk,'maxtotal',maxtotal,'unions done',done,'truncated',trunc,'hits',len(hits),'time',round(time.time()-t0,1))
    json.dump({'k':kk,'maxtotal':maxtotal,'done':done,'truncated':trunc,'trunc_list':report,'hits':hits},open('part3m_k%d_max%d.json'%(kk,maxtotal),'w'))
