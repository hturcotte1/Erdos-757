#!/usr/bin/env python3
"""Inventory of stored class lists with A=27n+35m-132tau <= 15: per (n,m,tau) pick the source with the most
connected Delta<=3 graphs; report all sources and disagreements. Writes inventory.json (selected file per cell)."""
import glob, os, re, json, sys
R='/home/user/Erdos-757/experiments/'
pats=['prover/L017/out/L01*/cells*/cell_*','20261027-0340-induction-n28-n29-f25/out/cells*/cell_*',
 '20261027-0340-induction-n28-n29-f25/lists/cell_*','20261027-0300-transversal-richness/inputs/cell_*',
 '20261027-0730-kt-cells/**/cell_*']
sys.path.insert(0,'/home/user/Erdos-757/experiments/prover/L021')
import kt
def load(path):
    gs=[]; complete=False
    txt=open(path)
    first=True
    for l in txt:
        if l.startswith('FOUND'): gs.append(kt.parse_edges(l))
        elif l.startswith('INFO') or l.startswith('{'): complete=True
        elif first and re.match(r'^\d+ \d+ \d+',l):
            # richness format: n m tau then edges
            v=list(map(int,l.split())); n,m,t=v[:3]; e=v[3:]
            gs.append([tuple(e[3*i:3*i+3]) for i in range(m)]); complete=True
        first=False
    return gs,complete
def good(g):
    n=kt.nverts(g); deg=[0]*n
    for e in g:
        for x in e: deg[x]+=1
    return max(deg)<=3
cells={}
for p in pats:
    for f in glob.glob(R+p,recursive=True):
        mm=re.match(r'cell_(\d+)_(\d+)_(\d+)(?:_D(\d+))?\.txt',os.path.basename(f))
        if not mm: continue
        n,m,t=map(int,mm.groups()[:3]); D=int(mm.group(4)) if mm.group(4) else None
        A=27*n+35*m-132*t
        if A>15: continue
        cells.setdefault((n,m,t),[]).append((f,D))
out={}
for key in sorted(cells):
    best=None; info=[]
    for f,D in cells[key]:
        if D is not None and D<2: continue
        gs,comp=load(f)
        gs3=[g for g in gs if good(g)]
        info.append((f.replace(R,''),D,len(gs3),comp))
        sc=(D is not None and D>=3, len(gs3))
        if D==2: sc=(False,len(gs3))
        if best is None or sc>best[0]: best=(sc,f,D,len(gs3),comp)
    out[str(key)]=dict(file=best[1],D=best[2],count=best[3],complete=best[4],A=27*key[0]+35*key[1]-132*key[2],
                       sources=info, disagree=len(set(i[2] for i in info if (i[1] or 3)>=3))>1)
json.dump(out,open('/home/user/Erdos-757/experiments/falsify/kt-star-e1hub/inventory.json','w'),indent=1)
for k,v in out.items():
    print(k,'A',v['A'],'D',v['D'],'count',v['count'],'complete',v['complete'],'nsrc',len(v['sources']),'DISAGREE' if v['disagree'] else '')
