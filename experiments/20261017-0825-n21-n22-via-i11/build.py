"""Vertex-by-vertex reconstruction of tight graphs inside class O (maxdeg<=3):
 cell_classes(n,m,t)  : iso classes of CONNECTED linear F7-free graphs with e(S)<=|S|-2, n vertices, m edges, tau>=t, maxdeg<=3 (conn_dfs3 + dedupe)
 extend(Gs,nG,T)      : all graphs obtained by adding ONE vertex with 3 new edges (disjoint pairs, endpoints of degree<=2), tau>=T; dedupe (F7-free, e(S) ok)
All counts are appended to stats (json)."""
import re,sys,json,subprocess,itertools,os,time
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'.')
import networkx as nx
from e757.cpsat_model import find_f7
from gutil import graph
from post import sub_ok
nm=lambda a,b:a['t']==b['t']
STATS={}
def parse_found(txt):
    for l in txt.splitlines():
        if l.startswith('FOUND') and l.endswith(')'):
            yield [tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
def dedupe(graphs,nv,tag):
    """graphs: iterable of edge lists on nv vertices -> iso classes that are F7-free and e(S)-ok"""
    buckets={}; reps=[]; tot=nf7=nsub=0
    for es in graphs:
        tot+=1
        if find_f7(es): nf7+=1; continue
        G=graph(es); h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t'); b=buckets.setdefault(h,[])
        if any(nx.is_isomorphic(G,H,node_match=nm) for H in b): continue
        b.append(G)
        if not sub_ok(es,nv): nsub+=1; continue
        reps.append(es)
    STATS[tag]=dict(labelled=tot,with_F7=nf7,F7free_iso_classes=sum(len(b) for b in buckets.values()),killed_by_eS=nsub,kept=len(reps))
    print(tag,STATS[tag],flush=True); return reps
def cell_classes(n,m,t,maxdeg=3):
    tag='cell_%d_%d_%d'%(n,m,t); f='K_%d_%d_%d.txt'%(n,m,t)
    if not os.path.exists(f) or 'DONE' not in open(f).read()[-300:]:
        subprocess.run('nice -n 10 ./conn_dfs3 %d %d %d %d 0 0 > %s'%(n,m,t,maxdeg,f),shell=True,check=True)
    last=open(f).read().strip().splitlines()[-1]
    STATS[tag+'_dfs']=dict(nodes=int(re.search(r'nodes=(\d+)',last).group(1)),found=int(re.search(r'found=(\d+)',last).group(1)))
    return dedupe(parse_found(open(f).read()),n,tag)
def ap(off): return [(off,off+1,off+2)]
def union(parts):
    es=[];off=0
    for nv,p in parts:
        es+= [tuple(v+off for v in e) for e in p]; off+=nv
    return es,off
def extend(Gs,nG,T,tag):
    inp='in_%s.txt'%tag; out='hits_%s.txt'%tag
    with open(inp,'w') as f:
        for es in Gs: f.write("%d "%len(es)+" ".join("%d %d %d"%tuple(e) for e in es)+"\n")
    t0=time.time()
    subprocess.run('nice -n 10 ./ext_vertex2 %d %d 3 < %s > %s'%(nG,T,inp,out),shell=True,check=True)
    last=open(out).read().strip().splitlines()[-1]
    STATS[tag+'_ext']=dict(graphs=len(Gs),summary=last,secs=round(time.time()-t0,1)); print(tag,last,flush=True)
    hits=[[tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)] for l in open(out) if l.startswith('HIT:')]
    return dedupe(hits,nG+1,tag+'_classes')
