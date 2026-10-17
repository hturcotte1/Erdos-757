"""Independent numpy count of tau(X)>=T extensions (d=3 only) vs ext3d with NOF7 NOHALL (raw cover-killing count) on the same sampled G."""
import sys,itertools,random,subprocess,re,numpy as np
path,nG,T,S,d=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]); MAXP=int(sys.argv[6])
random.seed(7); lines=open(path).read().strip().splitlines()
def npairs(l):
    t=list(map(int,l.split()))[1:]; g=[(t[3*k],t[3*k+1],t[3*k+2]) for k in range(len(t)//3)]
    gm=[sum(1<<v for v in e) for e in g]; deg=[sum(v in e for e in g) for v in range(nG)]
    return sum(1 for a in range(nG) for b in range(a+1,nG) if deg[a]<=d-1 and deg[b]<=d-1 and not any((m>>a&1) and (m>>b&1) for m in gm))
small=[i for i,l in enumerate(lines) if npairs(l)<=MAXP]
idx=random.sample(small,min(S,len(small)))
n=nG+1; allk=np.array([sum(1<<v for v in c) for c in itertools.combinations(range(n),T-1)],dtype=np.int64)
tot=0; sub=[]
for i in idx:
    sub.append(lines[i]); t=list(map(int,lines[i].split()))[1:]; g=[(t[3*k],t[3*k+1],t[3*k+2]) for k in range(len(t)//3)]
    gm=[sum(1<<v for v in e) for e in g]; deg=[sum(v in e for e in g) for v in range(nG)]
    pairs=[(a,b) for a in range(nG) for b in range(a+1,nG) if deg[a]<=d-1 and deg[b]<=d-1 and not any((m>>a&1) and (m>>b&1) for m in gm)]
    okg=np.ones(len(allk),dtype=bool)
    for em in gm: okg&=((allk&em)!=0)
    cand=allk[okg]; trip=[c for c in itertools.combinations(pairs,d) if len({v for p in c for v in p})==2*d]
    h=0
    for s in range(0,len(trip),500):
        ch=np.array([[(1<<a)|(1<<b)|(1<<nG) for a,b in tr] for tr in trip[s:s+500]],dtype=np.int64)
        cov=np.ones((len(ch),len(cand)),dtype=bool)
        for j in range(d): cov&=((cand[None,:]&ch[:,j:j+1])!=0)
        h+=int((~cov.any(axis=1)).sum())
    tot+=h
import os
env=dict(os.environ,NOF7='1',NOHALL='1')
out=subprocess.run(['./ext3d',str(nG),str(T),str(d),str(d-1)],input="\n".join(sub)+"\n",capture_output=True,text=True,env=env).stdout.strip().splitlines()[-1]
c=int(re.search(r'hits_after_hall=(\d+)',out).group(1))
print('sampled',len(idx),'numpy hits',tot,'ext3d raw hits',c,'EQUAL' if tot==c else 'DIFFERENT')
