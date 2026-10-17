"""Independent check of the reconstructed 8 classes of connected (17,13,7) maxdeg<=3 F7-free e(S)-ok graphs: random slices of the DIRECT DFS
(conn_dfs3s 17 13 7 3, consistent slicing) -> every F7-free e(S)-ok graph found must be isomorphic to one of the 8 classes; also report which classes were hit."""
import subprocess,random,time,re,sys,json
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'.')
import networkx as nx
from gutil import graph
from e757.cpsat_model import find_f7
from post import sub_ok
nm=lambda a,b:a['t']==b['t']
classes=[[tuple(e) for e in g] for g in json.load(open(sys.argv[6]))]
bk={}
for i,es in enumerate(classes): bk.setdefault(nx.weisfeiler_lehman_graph_hash(graph(es),node_attr='t'),[]).append((i,graph(es)))
K=21698; random.seed(int(sys.argv[1])); TL=float(sys.argv[2]); t0=time.time()
slices=0; found=0; f7free=0; ok=0; bad=[]; hit=set(); tot_nodes=0
while time.time()-t0<TL:
    I=random.randrange(K)
    out=subprocess.run(['nice','-n','10','./conn_dfs3s',sys.argv[3],sys.argv[4],sys.argv[5],'3','0','0',str(K),str(I)],capture_output=True,text=True).stdout
    slices+=1
    for l in out.splitlines():
        if l.startswith('FOUND') and l.endswith(')'):
            found+=1; es=[tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
            if find_f7(es): continue
            f7free+=1
            if not sub_ok(es,int(sys.argv[3])): continue
            G=graph(es); h=nx.weisfeiler_lehman_graph_hash(G,node_attr='t')
            m=[i for i,H in bk.get(h,[]) if nx.is_isomorphic(G,H,node_match=nm)]
            if m: ok+=1; hit.add(m[0])
            else: bad.append(es)
print(dict(slices=slices,found=found,F7free=f7free,F7free_eS_ok_in_classes=ok,classes_hit=sorted(hit),not_in_classes=len(bad)))
json.dump(dict(slices=slices,found=found,F7free=f7free,ok=ok,classes_hit=sorted(hit),not_in_classes=bad),open('validate_generic_%s_%s.json'%(sys.argv[6],sys.argv[1]),'w'))
