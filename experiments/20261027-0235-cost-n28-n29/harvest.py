import os, re, json, glob
CELLDIRS=['../20261017-2150-i11-n27/out/cells','out/cells','../20261027-0300-tight-cells-d4/out/cells']
rows=[]
import itertools
seenk=set()
for p in itertools.chain(*[sorted(glob.glob(c+'/cell_*.txt')) for c in CELLDIRS]):
    m=re.match(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt',os.path.basename(p)); k=tuple(map(int,m.groups()))
    if k in seenk: continue
    c=0; info=None
    with open(p) as f:
        for l in f:
            if l.startswith('FOUND:'): c+=1
            elif l.startswith('INFO '): info=json.loads(l[5:])
    n,mm,t,D=k; s=3*n+2*mm-11*t
    nodes=ins=0; hits=0; secs=None; route=None
    if info:
        route=info.get('route'); secs=info.get('secs')
        for b in info.get('branches',[]):
            e=b.get('ext',{}); nodes+=e.get('nodes',0) if isinstance(e,dict) else 0; ins+=b.get('inputs',0)
        if route=='recurse' and ins==0: pass
    if info is None: continue
    seenk.add(k)
    rows.append(dict(key=k,s=s,count=c,route=route,nodes=nodes,inputs=ins,secs=secs,ext=[b.get('ext') for b in (info or {}).get('branches',[])][:1]))
json.dump(rows,open('harvest.json','w'))
for r in rows:
    if (r['route'] or '').startswith('recurse') and r['inputs']>0: print(r['key'],'s=%d'%r['s'],'classes',r['count'],'inputs',r['inputs'],'nodes %.2e'%r['nodes'],'n/in %.0f'%(r['nodes']/r['inputs']) if r['nodes'] else '', 'secs',r['secs'])
