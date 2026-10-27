"""Conjecture T, search (a): tight K with a degree-4 vertex v = v + 4 edges {v,a_i,b_i} attached to a disjoint union Q of
smaller tight connected graphs (library). tau(K)=tau(Q)+1 iff every maximum independent set of Q contains one of the pairs P_i.
Exhaustive over pair choices (DFS with exact coverage probabilities), then exact tau + class-C check in C."""
import sys, json, itertools, collections, time, gzip
sys.path.insert(0,'src')
import numpy as np
from fractions import Fraction
import networkx as nx
from hg import *

class Comp:
    def __init__(self,name,n,edges):
        self.name=name; self.n=n; self.edges=[tuple(e) for e in edges]; self.m=len(edges)
        self.tau=tau(n,self.edges); self.alpha=n-self.tau
        N=1<<n; S=np.arange(N,dtype=np.int64)
        ind=np.ones(N,dtype=bool)
        for a,b,c in self.edges:
            mk=(1<<a)|(1<<b)|(1<<c); ind&=((S&mk)!=mk)
        pc=np.zeros(N,dtype=np.int32)
        for i in range(n): pc+=((S>>i)&1).astype(np.int32)
        mis=S[ind&(pc==self.alpha)]
        self.mis=mis; self.nmis=len(mis)
        self.cache={}
        self.pairs_in_edge={(min(x,y),max(x,y)) for e in self.edges for x,y in itertools.combinations(e,2)}
    def cnt(self,mask):
        r=self.cache.get(mask)
        if r is None:
            r=int(np.count_nonzero((self.mis&mask)==mask)); self.cache[mask]=r
        return r

def load_library():
    lib=[]
    def add(name,L):
        for i,es in enumerate(L):
            n=nverts(es); lib.append(Comp(f'{name}#{i}',n,es))
    R='cells12/cells/'
    add('e3',parse_cell(R+'cell_3_1_1_D4.txt'))
    add('t10',parse_cell(R+'cell_10_7_4_D4.txt'))
    add('t14',parse_cell(R+'cell_14_12_6_D4.txt'))
    add('t17D3',parse_cell(R+'cell_17_13_7_D3.txt'))
    return lib

def multisets(lib,total,maxparts=8):
    """multisets (as index tuples nondecreasing) of library comps with sum n == total, deficit>=5"""
    out=[]
    L=sorted(range(len(lib)),key=lambda i:(lib[i].n,i))
    def rec(start,rem,cur):
        if rem==0:
            if sum(lib[i].n-lib[i].m for i in cur)>=5: out.append(tuple(cur))
            return
        if len(cur)>=maxparts: return
        for k in range(start,len(L)):
            i=L[k]
            if lib[i].n>rem: continue
            cur.append(i); rec(k,rem-lib[i].n,cur); cur.pop()
    rec(0,total,[])
    return out

def search_union(lib,idxs,max_nodes=None):
    comps=[lib[i] for i in idxs]
    off=[];o=0
    for c in comps: off.append(o); o+=c.n
    NQ=o
    comp_of=[]; local=[]
    for ci,c in enumerate(comps):
        for x in range(c.n): comp_of.append(ci); local.append(x)
    total=1
    for c in comps: total*=c.nmis
    # pairs
    pairs=[]
    for u in range(NQ):
        for w in range(u+1,NQ):
            if comp_of[u]==comp_of[w]:
                c=comps[comp_of[u]]
                if (local[u],local[w]) in c.pairs_in_edge: continue
            pairs.append((u,w))
    def joint(vs):
        # number of MIS tuples containing all vertices vs (global ids)
        byc={}
        for v in vs: byc[comp_of[v]]=byc.get(comp_of[v],0)|(1<<local[v])
        r=1
        for ci,c in enumerate(comps):
            if ci in byc: r*=c.cnt(byc[ci])
            else: r*=c.nmis
        return r
    pc=[joint(p) for p in pairs]
    order=sorted(range(len(pairs)),key=lambda i:-pc[i])
    pairs=[pairs[i] for i in order]; pc=[pc[i] for i in order]
    if pc and pc[0]==0: return [],0
    P=len(pairs)
    # coverage of a set of pairs (indices) by inclusion-exclusion; cache by frozenset of chosen
    def cover(S):
        tot=0
        for r in range(1,len(S)+1):
            for sub in itertools.combinations(S,r):
                vs=set()
                for i in sub: vs.update(pairs[i])
                tot+=(-1)**(r+1)*joint(vs)
        return tot
    found=[]; nodes=0
    def dfs(start,S,usedv,k_rem):
        nonlocal nodes
        nodes+=1
        if max_nodes and nodes>max_nodes: raise RuntimeError('node limit')
        cv=cover(S) if S else 0
        if cv==total and S:
            found.append(list(S)); return
        if k_rem==0: return
        # bound: k_rem more pairs can add at most sum of next k_rem probabilities (pairs sorted desc)
        for i in range(start,P):
            if cv+k_rem*pc[i]<total: break   # sorted desc: later pairs have smaller pc
            u,w=pairs[i]
            if u in usedv or w in usedv: continue
            usedv.add(u);usedv.add(w); S.append(i)
            dfs(i+1,S,usedv,k_rem-1)
            S.pop(); usedv.discard(u);usedv.discard(w)
    dfs(0,[],set(),4)
    # build K for each found covering set (size<=4); extend to 4 pairs if needed (any extra admissible pair)
    results=[]
    for S in found:
        base=[pairs[i] for i in S]
        ext_opts=[base]
        if len(base)<4:
            ext_opts=[]
            usedv={x for p in base for x in p}
            cand=[p for p in pairs if p[0] not in usedv and p[1] not in usedv]
            for extra in itertools.combinations(cand,4-len(base)):
                vs=[x for p in extra for x in p]
                if len(set(vs))<len(vs): continue
                ext_opts.append(base+list(extra))
        for prs in ext_opts:
            results.append(prs)
    return results,(comps,off,NQ,nodes)

def build_K(comps,off,NQ,prs):
    edges=[]
    for c,o in zip(comps,off):
        for e in c.edges: edges.append(tuple(sorted(o+x for x in e)))
    v=NQ
    for (a,b) in prs: edges.append(tuple(sorted((a,b,v))))
    return NQ+1,edges
