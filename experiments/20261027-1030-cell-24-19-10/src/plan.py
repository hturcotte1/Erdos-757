"""Dry-run plan: for each target cell, the (d,tp) branches, decompositions, input counts (product of class counts), and the missing sub-cells.
usage: python3 plan.py n,m,t,D ...   (reads CELLDIR=../cells_seed read-only; never writes cells)"""
import os, sys, math, itertools
HERE=os.path.dirname(os.path.abspath(__file__)); CELLS=os.environ.get('CELLDIR',os.path.join(HERE,'..','cells_seed'))
os.environ['CELLDIR']='/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad/plan_cells'; os.environ['ENGINELOG']='/dev/null'
sys.path.insert(0,HERE); import engine
MD=10
def valid(n,m,t,D): return not (m==0 or t<1 or t>m or n>2*m+1 or m>n-2 or 17*t>5*n+3*m or D<1)
CNT={}
def count(k):
    if k in CNT: return CNT[k]
    p=os.path.join(CELLS,'cell_%d_%d_%d_D%d.txt'%k)
    if not os.path.exists(p): CNT[k]=None; return None
    c=sum(1 for l in open(p) if l.startswith('FOUND:')); CNT[k]=c; return c
def ncomb(c,k): return math.comb(c+k-1,k)
seen={}
def visit(k,top=False):
    if k in seen: return
    if not valid(*k): seen[k]=dict(status='guard-empty'); return
    n,m,t,D=k; c=count(k)
    if c is not None: seen[k]=dict(status='have',classes=c); return
    seen[k]=dict(status='MISSING',route='direct' if m<=MD else 'recurse',branches=[])
    if m<=MD: return
    for d in range(max(1,math.ceil(3*m/n)),D+1):
        for tp in (t-1,t):
            Sp=3*(n-1)+2*(m-d)-11*tp
            if Sp<0 or tp<0: continue
            decs=engine.decompositions(n-1,m-d,Sp); tot=0; nd=0; unk=0; det=[]
            for dec in decs:
                g={}
                for x in dec: g[x]=g.get(x,0)+1
                size=1; ok=True
                for typ,kk in g.items():
                    if typ==(1,0,0): continue
                    ck=(typ[0],typ[1],typ[2],d)
                    if not valid(*ck): size=0; break
                    visit(ck)
                    cc=count(ck) if seen[ck]['status']=='have' else None
                    if cc is None: size=None; break
                    size*=ncomb(cc,kk)
                if size is None: unk+=1
                else: tot+=size
                det.append((sorted(g.items()),size))
            seen[k]['branches'].append(dict(d=d,tp=tp,Sp=Sp,ndec=len(decs),inputs_known=tot,unknown_decs=unk,dec=det))
if __name__=='__main__':
    tops=[tuple(map(int,a.split(','))) for a in sys.argv[1:]]
    for t in tops: visit(t,True)
    for k,v in sorted(seen.items()):
        if v['status']=='MISSING':
            print('MISSING',k,v['route'])
            for b in v['branches']:
                print('   d=%d tp=%d S=%d ndec=%d inputs_known=%d unknown_decs=%d'%(b['d'],b['tp'],b['Sp'],b['ndec'],b['inputs_known'],b['unknown_decs']))
                if os.environ.get('V'):
                    for d_,s in b['dec']: print('       ',d_,s)
        elif v['status']=='have' and k in tops: print('HAVE',k,v['classes'])
