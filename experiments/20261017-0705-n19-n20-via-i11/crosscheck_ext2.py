"""Independent numpy re-implementation of the vertex-extension step (nG -> nG+1, 3 new edges, endpoints of G-degree<=2, tau(H)>=T)
on a random sample of G's; compares hit counts with ext_vertex2.   usage: crosscheck_ext2.py input.txt nG T SAMPLE"""
import sys,itertools,random,subprocess,re,numpy as np
path,nG,T,S=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
random.seed(11)
lines=open(path).read().strip().splitlines(); idx=random.sample(range(len(lines)),min(S,len(lines)))
n=nG+1
allk=np.array([sum(1<<v for v in c) for c in itertools.combinations(range(n),T-1)],dtype=np.int64)
tot=0
for i in idx:
    t=list(map(int,lines[i].split()))[1:]; g=[(t[3*k],t[3*k+1],t[3*k+2]) for k in range(len(t)//3)]
    gm=[sum(1<<v for v in e) for e in g]; deg=[sum(v in e for e in g) for v in range(nG)]
    pairs=[(a,b) for a in range(nG) for b in range(a+1,nG) if deg[a]<=2 and deg[b]<=2 and not any((m>>a&1) and (m>>b&1) for m in gm)]
    okg=np.ones(len(allk),dtype=bool)
    for em in gm: okg&=((allk&em)!=0)
    cand=allk[okg]
    trip=[(x,y,z) for x,y,z in itertools.combinations(pairs,3) if len({*x,*y,*z})==6]
    hits=0
    for s in range(0,len(trip),1000):
        ch=np.array([[ (1<<a)|(1<<b)|(1<<nG) for a,b in tr] for tr in trip[s:s+1000]],dtype=np.int64)
        cov=np.ones((len(ch),len(cand)),dtype=bool)
        for j in range(3): cov&=((cand[None,:]&ch[:,j:j+1])!=0)
        hits+=int((~cov.any(axis=1)).sum())
    out=subprocess.run(['./ext_vertex2',str(nG),str(T),'3'],input=lines[i]+"\n",capture_output=True,text=True).stdout.strip().splitlines()[-1]
    r=int(re.search(r'hits=(\d+)',out).group(1)); assert r==hits,(i,r,hits); tot+=hits
print('sampled',len(idx),'G; total hits (python == C):',tot)
