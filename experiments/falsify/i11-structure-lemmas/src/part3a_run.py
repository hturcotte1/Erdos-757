import sys, json, time, collections
sys.path.insert(0,'src')
from part3a import *
nmax=int(sys.argv[1]); tlimit=float(sys.argv[2])
lib=load_library()
t0=time.time()
found_by_n={}   # n -> list of dict(edges)
summary=[]
def canon_key(n,edges):
    G=nx.Graph()
    G.add_nodes_from(range(n)); 
    # bipartite incidence graph for isomorphism
    B=nx.Graph()
    for v in range(n): B.add_node(('v',v),t=0)
    for i,e in enumerate(edges):
        B.add_node(('e',i),t=1)
        for v in e: B.add_edge(('v',v),('e',i))
    return B
def same(B1,B2):
    return nx.is_isomorphic(B1,B2,node_match=lambda a,b:a['t']==b['t'])
newgraphs=[]
for n in range(5,nmax+1):
    N=n-1
    ms=multisets(lib,N)
    ngraphs=[]  # (B,edges)
    hits=0; unions_done=0; unions_hit=0; node_total=0; errs=0
    for idxs in ms:
        if time.time()-t0>tlimit: break
        try:
            res,info=search_union(lib,idxs,max_nodes=3_000_000)
        except RuntimeError:
            errs+=1; continue
        unions_done+=1
        if not res: 
            if info: node_total+=info[3]
            continue
        comps,off,NQ,nodes=info; node_total+=nodes
        hit_here=False
        for prs in res[:3000]:
            nn,edges=build_K(comps,off,NQ,prs)
            # connectivity, class C, tight
            if not is_connected(nn,edges): continue
            if not classC_fast(nn,edges): continue
            tq=sum(c.tau for c in comps)
            t=tau(nn,edges)
            s=slack(nn,edges,t)
            assert t==tq+1 and s==0,(t,tq,s)
            hit_here=True; hits+=1
            B=canon_key(nn,edges)
            key=(len(edges),tuple(sorted(degrees(nn,edges))))
            dup=False
            for (B2,e2,k2) in ngraphs:
                if k2==key and same(B,B2): dup=True;break
            if not dup: ngraphs.append((B,edges,key))
        unions_hit+=hit_here
    summary.append({'n':n,'unions':len(ms),'unions_done':unions_done,'unions_with_tight_K':unions_hit,'node_total':node_total,'errs':errs,
                    'new_tight_classes_deg4':len(ngraphs),'time':round(time.time()-t0,1)})
    print(summary[-1],flush=True)
    known_re=0; knownset=set()
    for (B,edges,key) in ngraphs:
        match=None
        for j,c in enumerate(lib):
            if c.n==n and c.m==len(edges):
                if same(B,canon_key(n,c.edges)): match=j;break
        if match is not None:
            known_re+=1; knownset.add(match); continue
        newgraphs.append({'n':n,'m':len(edges),'tau':tau(n,edges),'edges':edges})
        lib.append(Comp(f'gen{n}#{len(newgraphs)}',n,edges))
    summary[-1]['reproduced_known_classes']=known_re
    summary[-1]['new_classes']=len(ngraphs)-known_re
    print('   n=%d: generated %d classes, %d match library, %d NEW'%(n,len(ngraphs),known_re,len(ngraphs)-known_re),flush=True)
    json.dump({'summary':summary,'graphs':newgraphs},open('part3a_results.json','w'))
