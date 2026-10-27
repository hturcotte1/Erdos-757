"""Select, for each cell (n,m,tau), the stored list file with largest Delta label then most lines.
Writes selected.json. Considers slack<=SMAX."""
import os,re,gzip,json,collections,sys
SMAX=int(sys.argv[1]) if len(sys.argv)>1 else 10
ROOT='/home/user/Erdos-757'
best={}
def nlines(p):
    op=gzip.open if p.endswith('.gz') else open
    k=0
    try:
        with op(p,'rt') as f:
            for l in f:
                if l.startswith('FOUND') or (l and l[0].isdigit()): k+=1
    except Exception as e:
        pass
    return k
allf=[]
for root,ds,fs in os.walk(ROOT+'/experiments'):
    for f in fs:
        m=re.match(r'cell_(\d+)_(\d+)_(\d+)(?:_D(\d+))?',f)
        if not m or f.endswith('.json') or f.endswith('.tmp'): continue
        n,mm,t=map(int,m.groups()[:3]); s=3*n+2*mm-11*t
        if s>SMAX: continue
        D=int(m.group(4)) if m.group(4) else -1
        p=os.path.join(root,f)
        allf.append((n,mm,t,D,p))
print(len(allf),'candidate files')
bycell=collections.defaultdict(list)
for n,mm,t,D,p in allf: bycell[(n,mm,t)].append((D,p))
sel={}
for k,lst in bycell.items():
    Dmax=max(D for D,p in lst)
    cands=[p for D,p in lst if D==Dmax]
    # lines count for up to a few candidates; take the max
    best=max(cands,key=lambda p: (nlines(p) if os.path.getsize(p)<50e6 else os.path.getsize(p)))
    sel[k]=(Dmax,best)
out=[{'n':k[0],'m':k[1],'tau':k[2],'D':v[0],'path':v[1],'slack':3*k[0]+2*k[1]-11*k[2]} for k,v in sorted(sel.items())]
json.dump(out,open(sys.argv[2] if len(sys.argv)>2 else "selected.json","w"),indent=0)
c=collections.Counter()
for o in out: c[o['slack']]+=os.path.getsize(o['path'])
print(len(out),'cells selected'); print(sorted(c.items()))
