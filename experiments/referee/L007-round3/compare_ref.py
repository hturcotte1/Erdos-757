# Validate levelgen (referee) against bfref (referee brute force) on every cell with n<=NMAX:
#  (1) unpruned run (T0=0, DMAX=100): labelled count sum N!/|Aut| per (tau, maxdeg) must equal brute force;
#  (2) pruned runs for every t in 0..taumax+1 and D in {2,3,100}: labelled total must equal brute-force count
#      of graphs with tau>=t and maxdeg<=D; every output must satisfy tau>=t, maxdeg<=D (checked in levelgen + here).
import subprocess, sys, math, collections, re
NMAX=int(sys.argv[1])
def run(N,M,T0,D,pr=1):
    out=subprocess.run(['./levelgen',str(N),str(M),str(T0),str(D),'0',str(pr)],capture_output=True,text=True,check=True).stdout
    cls=[]
    for line in out.splitlines():
        if line.startswith('CLASS'):
            mm=re.match(r'CLASS aut=(\d+) tau=(\d+) maxdeg=(\d+)',line); cls.append(tuple(map(int,mm.groups())))
        if line.startswith('FINAL'):
            lab=int(re.search(r'labelled=(\d+)',line).group(1)); nc=int(re.search(r'classes=(\d+)',line).group(1))
    return cls,lab,nc
cells=0; mism=0; runs=0; totcls=0
for n in range(3,NMAX+1):
    bf=collections.defaultdict(int)
    for line in open(f'bf_ref_n{n}.txt'):
        a=list(map(int,line.split())); bf[(a[1],a[2],a[3])]+=a[4]
    ms=sorted(set(k[0] for k in bf))
    allm=sorted(set(ms)|set(range(1,n)))
    for m in allm:
        cls,lab,nc=run(n,m,0,100)
        mine=collections.defaultdict(int)
        for aut,t,d in cls: mine[(t,d)]+=math.factorial(n)//aut
        theirs={(t,d):c for (mm,t,d),c in bf.items() if mm==m}
        cells+=1; totcls+=nc
        if dict(mine)!=theirs: mism+=1; print('MISMATCH unpruned',n,m,dict(mine),theirs)
        taumax=max([t for (t,d) in theirs]+[0])
        for t in range(0,taumax+2):
            for D in (2,3,100):
                cls2,lab2,nc2=run(n,m,t,D,1); runs+=1
                want=sum(c for (tt,d),c in theirs.items() if tt>=t and d<=D)
                bad=[c for c in cls2 if c[1]<t or c[2]>D]
                if lab2!=want or bad: mism+=1; print('MISMATCH pruned',n,m,t,D,lab2,want,bad)
print(f'n<={NMAX}: cells={cells} pruned_runs={runs} mismatches={mism} classes_unpruned_total={totcls}')
