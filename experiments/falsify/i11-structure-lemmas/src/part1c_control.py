"""Control: how common are universal vertices (in every maximum independent set) in connected C-graphs of slack 2..6, from all stored cells."""
import sys, glob, re, json, random, collections
sys.path.insert(0,'src')
from hg import *
random.seed(3)
files=set()
for d in ['cells12/cells','cells13/cells','cells14/cells']:
    for f in glob.glob(d+'/cell_*_D*.txt'): files.add(f)
seen={}
for f in sorted(files):
    m=re.search(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)',f); n,mm,t,D=map(int,m.groups())
    if n>20: continue
    key=(n,mm,t,D)
    if key in seen: continue
    seen[key]=f
stat=collections.defaultdict(lambda:[0,0,0])  # slack -> [graphs, with universal, universal vertices]
for (n,mm,t,D),f in sorted(seen.items()):
    s=3*n+2*mm-11*t
    if s>8 or s<0: continue
    L=parse_cell(f)
    if len(L)>40: L=random.sample(L,40)
    for es in L:
        if not is_connected(n,es): continue
        st=stat[s]; st[0]+=1
        u=0
        for x in range(n):
            tx=tau(n,es,((1<<n)-1)&~(1<<x))
            if tx==t: u+=1
        if u: st[1]+=1; st[2]+=u
print({s:v for s,v in sorted(stat.items())})
json.dump({str(s):{'graphs_sampled':v[0],'graphs_with_universal_vertex':v[1],'universal_vertices_total':v[2]} for s,v in sorted(stat.items())},open('part1c_control.json','w'),indent=1)
