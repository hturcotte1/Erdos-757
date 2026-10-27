import sys, json, itertools, collections
sys.path.insert(0,'src')
from hg import *
R='cells12/cells/'
T=[]
for f in ['cell_3_1_1_D4.txt','cell_10_7_4_D4.txt','cell_14_12_6_D4.txt','cell_17_13_7_D3.txt']:
    for es in parse_cell(R+f): T.append((nverts(es),es))
for g in json.load(open('part3a_results.json'))['graphs']: T.append((g['n'],[tuple(e) for e in g['edges']]))
tt=[tau(n,es) for n,es in T]
cnt=collections.Counter(); bad=[]; notC=0; tot=0
for i in range(len(T)):
    for j in range(i,len(T)):
        n1,e1=T[i]; n2,e2=T[j]
        for x1 in range(n1):
            for x2 in range(n2):
                # identify x2 with x1: vertices of T2 renamed
                mp={}; nxt=n1
                for v in range(n2):
                    if v==x2: mp[v]=x1
                    else: mp[v]=nxt; nxt+=1
                es=list(e1)+[tuple(sorted(mp[v] for v in e)) for e in e2]
                n=nxt
                if n>40: continue
                tot+=1
                if not classC_fast(n,es): notC+=1; continue
                t=tau(n,es); s=slack(n,es,t)
                cnt[(s, t==tt[i]+tt[j]-1)]+=1
                if t!=tt[i]+tt[j]-1: bad.append((i,j,x1,x2,t,s))
print('total gluings',tot,'not in C',notC,dict(cnt),'bad',bad[:5])
json.dump({'tight_graphs':len(T),'total_gluings':tot,'not_in_C':notC,'counts_(slack,tau=t1+t2-1)':{str(k):v for k,v in cnt.items()},'bad':bad[:20]},open('part1b_glue.json','w'))
