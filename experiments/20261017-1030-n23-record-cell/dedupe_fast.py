"""Component-wise isomorphism dedupe: a graph is a disjoint union of connected components; canonical key = sorted tuple of component class ids
(component iso classes by WL hash + exact nx isomorphism inside buckets).  F7 / e(S) filters applied per iso class (e(S) per class via post.sub_ok)."""
import re,sys,json,time
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'.')
import networkx as nx
from gutil import graph
from e757.cpsat_model import find_f7
from post import sub_ok
nm=lambda a,b:a['t']==b['t']
comp_buckets={}; comp_list=[]
import igraph
def canon_key(es):
    """exact canonical form of the incidence graph (BLISS via igraph)"""
    vs=sorted({v for e in es for v in e}); mp={v:i for i,v in enumerate(vs)}; nv=len(vs); m=len(es)
    edges=[]
    for k,e in enumerate(es):
        for v in e: edges.append((mp[v],nv+k))
    g=igraph.Graph(n=nv+m,edges=edges)
    col=[0]*nv+[1]*m
    perm=g.canonical_permutation(color=col)
    gc=g.permute_vertices(perm)
    return (nv,m,tuple(sorted((min(a,b),max(a,b)) for a,b in gc.get_edgelist())))
_ids={}
def comp_id(es):
    k=canon_key(es)
    if k not in _ids: _ids[k]=len(_ids); comp_list.append(es)
    return _ids[k]
def components(es):
    # union-find on vertices
    par={}
    def f(x):
        while par.setdefault(x,x)!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for e in es:
        for v in e[1:]: par[f(v)]=f(e[0])
    g={}
    for e in es: g.setdefault(f(e[0]),[]).append(e)
    out=[]
    for es_ in g.values():
        vs=sorted({v for e in es_ for v in e}); mp={v:i for i,v in enumerate(vs)}
        out.append([tuple(mp[v] for v in e) for e in es_])
    return out
def dedupe_fast(graphs,nv,tag):
    seen={}; tot=nf7=nsub=0; reps=[]; f7cache={}
    for es in graphs:
        tot+=1
        cids=tuple(sorted(comp_id(c) for c in components(es)))
        if cids in seen: continue
        seen[cids]=1
        if find_f7(es): nf7+=1; continue
        if not sub_ok(es,nv): nsub+=1; continue
        reps.append(es)
    st=dict(labelled=tot,iso_classes=len(seen),with_F7=nf7,killed_by_eS=nsub,kept=len(reps))
    print(tag,st,flush=True); return reps,st
if __name__=="__main__":
    src,nv,out=sys.argv[1],int(sys.argv[2]),sys.argv[3]
    hits=[[tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)] for l in open(src) if l.startswith('HIT:')]
    t0=time.time(); reps,st=dedupe_fast(hits,nv,src); st['secs']=time.time()-t0
    json.dump(reps,open(out,'w')); json.dump(st,open(out+'.stats.json','w'))
