"""cross-check my dual-graph enumeration of connected Delta<=2 members of C (n<=14) against L012's enum_conn + filt + canon."""
import subprocess, json, sys, collections
B='/home/user/Erdos-757/experiments/prover/L012/bin/'
def run(cmd,inp=None):
    return subprocess.run(cmd,input=inp,capture_output=True,text=True,shell=isinstance(cmd,str),timeout=600).stdout
mine=json.load(open('part2_enum_results.json'))
# my counts per (n,m): need class counts, recompute from cache
import pickle
sys.path.insert(0,'src')
from part2_enum import dual_hypergraph
levels=pickle.load(open('levels_cache_11.pkl','rb'))
cnt=collections.Counter()
for m,L in levels.items():
    for G in L:
        n,es=dual_hypergraph(G); cnt[(n,m)]+=1
cnt[(1,0)]=1
res={}; bad=[]
for n in range(2,15):
    for m in range(1,n):
        if n>2*m+1 or m>n-2: continue
        tot=0
        for t in range(1,m+1):
            out=run('%senum_conn %d %d %d 2 1'%(B,n,m,t))
            found=[l for l in out.splitlines() if l.startswith('FOUND:')]
            if not found: continue
            f=run([B+'filt','FOUND',str(n),'tau',str(t)],'\n'.join(found)+'\n')
            surv=[l.split(' #conn')[0] for l in f.splitlines() if l.startswith('SURVIVOR:') and l.endswith('#conn=1')]
            if not surv: continue
            cl=run([B+'canon',str(n)],'\n'.join(surv)+'\n').splitlines()
            tot+=len(set(cl))
        res[f'{n},{m}']=(tot,cnt.get((n,m),0))
        if tot!=cnt.get((n,m),0): bad.append((n,m,tot,cnt.get((n,m),0)))
for k in cnt:
    if k[0]<=14 and f'{k[0]},{k[1]}' not in res and k!=(1,0): bad.append(('missing',k,cnt[k]))
json.dump({'per_nm_(enum_conn_classes,mine)':res,'mismatches':bad,'total_enum_conn':sum(v[0] for v in res.values()),'total_mine_n_le_14':sum(v for k,v in cnt.items() if k[0]<=14 and k!=(1,0))},open('part2_crosscheck.json','w'),indent=1)
print(bad, sum(v[0] for v in res.values()))
