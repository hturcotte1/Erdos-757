"""iterate K -> v + (3,1,1) + K  (n -> n+4) starting from all tight comps found, using the exact cover search of e3plus."""
import sys, json, time, itertools
sys.path.insert(0,'src')
import numpy as np
from part3a import *
import e3plus
sys.setrecursionlimit(10000)

class FastComp:
    def __init__(self,name,n,edges):
        self.name=name; self.n=n; self.edges=[tuple(e) for e in edges]; self.m=len(edges)
        self.tau=tau(n,self.edges); self.alpha=n-self.tau
        inc=[[] for _ in range(n)]
        for e in self.edges:
            mk=(1<<e[0])|(1<<e[1])|(1<<e[2])
            for v in e: inc[v].append(mk)
        res=[]
        alpha=self.alpha
        def rec(i,I,sz):
            if sz+(n-i)<alpha: return
            if i==n:
                if sz==alpha: res.append(I)
                return
            bit=1<<i
            ok=True
            for e in inc[i]:
                if (e&~bit)&~I==0: ok=False;break
            if ok: rec(i+1,I|bit,sz+1)
            rec(i+1,I,sz)
        rec(0,0,0)
        self.mis=np.array(res,dtype=np.int64); self.nmis=len(res)
        self.pairs_in_edge={(min(x,y),max(x,y)) for e in self.edges for x,y in itertools.combinations(e,2)}

def inc_graph(n,edges): return e3plus.inc(n,edges)
if __name__=='__main__':
    start=sys.argv[1]; nlevels=int(sys.argv[2]); tl=float(sys.argv[3])
    cur=[(n,[tuple(e) for e in g]) for n,g in json.load(open(start))['graphs_by_n']]   # list of (n, edges)
    t0=time.time(); log=[]
    allout={}
    for lev in range(nlevels):
        nxt=[]; stats=[]
        for (n,edges) in cur:
            if time.time()-t0>tl: break
            A=FastComp('c',n,edges)
            st,gs=e3plus.run(A)
            stats.append((n,st))
            for g in gs:
                B=inc_graph(n+4,g)
                if not any(n2==n+4 and len(e2)==len(g) and e3plus.iso(B,B2) for n2,e2,B2 in nxt): nxt.append((n+4,g,B))
            print('level',lev,'from n',n,st,round(time.time()-t0),flush=True)
        cur=[(n,g) for n,g,_ in nxt]
        allout['n%d'%(cur[0][0] if cur else -1)]=[{'n':n,'edges':g} for n,g in cur]
        print('LEVEL',lev,'new distinct tight graphs',len(cur),'n=',[n for n,_ in cur][:1],flush=True)
        json.dump(allout,open('chain_out.json','w'))
        if not cur: break
