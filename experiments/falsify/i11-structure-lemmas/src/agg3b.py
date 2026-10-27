import sys, re, json, glob, collections
sys.path.insert(0,'src')
import networkx as nx
from hg import *
def inc(n,edges):
    B=nx.Graph()
    for v in range(n): B.add_node(('v',v),t=0)
    for i,e in enumerate(edges):
        B.add_node(('e',i),t=1)
        for v in e: B.add_edge(('v',v),('e',i))
    return B
def key(B): return nx.weisfeiler_lehman_graph_hash(B,iterations=4,node_attr='t')
def iso(B1,B2): return nx.is_isomorphic(B1,B2,node_match=lambda a,b:a['t']==b['t'])
# known cells index
known=collections.defaultdict(list)   # (n,m,tau)->list of (hash,B)
import os
cellfiles=set()
for d in ['cells12/cells','cells13/cells','cells14/cells','cells16/cells_new/runA','cells16/cells_new/runF','cells16/cells_new/runB2']:
    for f in glob.glob(d+'/cell_*_D*.txt'): cellfiles.add(f)
def load_known(n,m,t):
    k=(n,m,t)
    if k in known: return known[k]
    seen=[]
    for f in cellfiles:
        mm=re.search(r'cell_(\d+)_(\d+)_(\d+)_D',f)
        if tuple(map(int,mm.groups()))!=k: continue
        for es in parse_cell(f):
            B=inc(n,es); seen.append((key(B),B))
    known[k]=seen
    return seen
summ={}; saves=[]
for f in sorted(glob.glob('out3b/*.txt')):
    for line in open(f):
        if line.startswith('RESULT'):
            d=dict(re.findall(r'(\w+)=([\w:\- ]+?)(?= \w+=|$)',line.strip()))
            n=int(d['n']); m=int(d['m'])
            hist=dict((int(a),int(b)) for a,b in (x.split(':') for x in d['hist'].split()))
            summ[(n,m)]={'samples':int(d['samples']),'bestTau':int(d['bestTau']),'minSlack':int(d['minSlack']),'hist':hist,'grown':int(d['grown'])}
        elif line.startswith('SAVE'):
            mm=re.match(r'SAVE n=(\d+) m=(\d+) slack=(-?\d+) tau=(\d+) E=(.*)',line.strip())
            n,m,s,t=map(int,mm.groups()[:4]); es=[tuple(int(x) for x in e.split(',')) for e in mm.group(5).split(';') if e]
            saves.append((n,m,s,t,es))
# dedupe saves
uniq=[]
bucket=collections.defaultdict(list)
for n,m,s,t,es in saves:
    B=inc(n,es); k=(n,m,t,key(B))
    if any(iso(B,B2) for B2 in bucket[k]): continue
    bucket[k].append(B); uniq.append((n,m,s,t,es,B))
out=[]
for n,m,s,t,es,B in uniq:
    kn=load_known(n,m,t)
    kh=key(B)
    is_known=any(h==kh and iso(B,B2) for h,B2 in kn)
    assert is_in_C if False else True
    ok=classC_fast(n,es) and is_connected(n,es) and slack(n,es,tau(n,es))==s
    out.append({'n':n,'m':m,'slack':s,'tau':t,'known_cell_has_entries':len(kn),'isomorphic_to_known_cell_member':is_known,'verified_C_conn_slack':ok,'edges':es})
minby=collections.defaultdict(lambda:10**9); tot=collections.Counter()
for (n,m),v in summ.items():
    minby[n]=min(minby[n],v['minSlack']); tot[n]+=v['samples']
res={'per_nm':{f'{n},{m}':v for (n,m),v in sorted(summ.items())},'min_slack_by_n':dict(sorted(minby.items())),'samples_by_n':dict(sorted(tot.items())),
     'graphs_slack_le_1_distinct':len(out),'graphs':out}
json.dump(res,open('part3b_results.json','w'))
print('min slack by n',dict(sorted(minby.items())))
print('samples by n',dict(sorted(tot.items())))
print('distinct slack<=1 graphs',len(out),collections.Counter((o['n'],o['m'],o['tau'],o['slack'],o['isomorphic_to_known_cell_member']) for o in out))
