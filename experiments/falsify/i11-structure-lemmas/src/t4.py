import sys,time,json; sys.path.insert(0,'src')
from part3a import *
lib=load_library()
d=json.load(open('part3a_results.json'))
for i,g in enumerate(d['graphs']):
    lib.append(Comp('gen17#%d'%i,g['n'],[tuple(e) for e in g['edges']]))
names={c.name:i for i,c in enumerate(lib)}
tests=[]
for nm in ['t17D3#2','t17D3#3','t17D3#4','t17D3#5']:
    tests.append((nm,'e3#0'))
for t in tests:
    idxs=[names[x] for x in t]
    t0=time.time()
    res,info=search_union(lib,idxs,max_nodes=3_000_000)
    comps,off,NQ,nodes,fs=info
    tight=0
    for prs in res:
        nn,edges=build_K(comps,off,NQ,prs)
        if not is_connected(nn,edges): continue
        if not classC_fast(nn,edges): continue
        tight+=1
    print(t,len(res),collections.Counter(fs),nodes,'tight K in C:',tight,round(time.time()-t0,1),flush=True)
