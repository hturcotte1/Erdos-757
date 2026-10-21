import sys, random, subprocess, json
sys.path.insert(0,'.')
from ss_lib import *
# validate C filter against exact python on a few seeds, ALL maps
def cfilter(seedline, kmax=3):
    open('/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad/one.txt','w').write(seedline+"\n")
    out=subprocess.run(['env','FULL=1','./filt','/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad/one.txt',str(kmax),'0','1'],capture_output=True,text=True,timeout=300).stdout
    return {tuple(map(int,l.split()[:5])):l.split() for l in out.splitlines()}
lines=open('seeds_n12.txt').read().splitlines()
tests=[open('reader.txt').read().strip()]+random.Random(1).sample(lines,3)
bad=0; tot=0; surv=0
for sl in tests:
    t=sl.split(); sid=int(t[0]); n=int(t[1]); O=list(map(int,t[2:]))
    C=cfilter(sl)
    for a in range(n):
     for b in range(a+1,n):
      for ap in range(n):
       for bp in range(n):
        if ap==bp or {ap,bp}&{a,b}: continue
        r=F(O[bp]-O[ap],O[b]-O[a])
        if abs(r)>=1: continue
        phi,_=make_phi(O,a,b,ap,bp)
        ok=all(( lambda c: c['count_ok'] and c['ap_equal'] and c['is_45_fast'])(structure_check(O,phi,K)) for K in (1,2,3))
        tot+=1
        inC=(a,b,ap,bp) in {k[1:] for k in C}
        surv+=ok
        if ok!=inC: bad+=1; print('MISMATCH',sid,a,b,ap,bp,ok,inC)
        elif ok:
            # compare slope
            best,M,R0=transfer(O,a,b,ap,bp); s,_=slope(M,R0)
            g=int(C[(sid,a,b,ap,bp)][8]) if (sid,a,b,ap,bp) in C else None
            if g is not None and F(g,120)!=s: print('SLOPE MISMATCH',sid,a,b,ap,bp,s,g)
print('maps',tot,'survivors(py)',surv,'mismatches',bad)
