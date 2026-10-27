import sys, json, os, collections
sys.path.insert(0,'src')
from part3a import *
tag=sys.argv[1]
d=json.load(open('part3m_%s.json'%tag)); k=d['k']
lib=load_library()
for i,g in enumerate(json.load(open('part3a_results_n18.json'))['graphs']):
    lib.append(Comp('gen%d_%d#%d'%(g['n'],i,i),g['n'],[tuple(e) for e in g['edges']]))
byname={c.name:c for c in lib}
def inc(n,edges):
    B=nx.Graph()
    for v in range(n): B.add_node(('v',v),t=0)
    for i,e in enumerate(edges):
        B.add_node(('e',i),t=1)
        for v in e: B.add_edge(('v',v),('e',i))
    return B
def iso(B1,B2): return nx.is_isomorphic(B1,B2,node_match=lambda a,b:a['t']==b['t'])
found=[]; stats=collections.Counter()
for hit in d['hits']:
    W=[byname[nm] for nm in hit['W']]
    off=[];o=0
    for c in W: off.append(o); o+=c.n
    NQ=o
    for covs in hit['covers']:
        if len(covs)!=4:
            stats['cover_size_%d_(needs_fillers)'%len(covs)]+=1; continue
        nn,edges=build_K(W,off,NQ,[tuple(p) for p in covs])
        stats['k4_candidates']+=1
        if not is_connected(nn,edges): stats['disconnected']+=1; continue
        if not classC_fast(nn,edges): stats['not_in_C']+=1; continue
        t=tau(nn,edges); s=slack(nn,edges,t)
        if s!=0: stats['slack_%d'%s]+=1; continue
        B=inc(nn,edges)
        for (n2,e2,B2) in found:
            if n2==nn and iso(B,B2): break
        else:
            found.append((nn,edges,B)); 
        stats['tight_K_hits']+=1
summary=collections.Counter(n for n,_,_ in found)
print(dict(stats)); print('distinct tight classes by n (deg-4 vertex):',dict(summary))
# compare with library
newc=0
for n,e,B in found:
    if any(c.n==n and c.m==len(e) and iso(B,inc(n,c.edges)) for c in lib): continue
    newc+=1
print('not in library:',newc)
json.dump({'stats':dict(stats),'by_n':dict(summary),'not_in_library':newc,'graphs':[{'n':n,'m':len(e),'edges':e} for n,e,_ in found]},open('part3m_post_%s.json'%tag,'w'))
