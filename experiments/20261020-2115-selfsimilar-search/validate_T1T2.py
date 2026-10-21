import sys, subprocess, random
sys.path.insert(0,'.')
from ss_lib import *
SP='/tmp/claude-0/-home-user-Erdos-757/32619e2f-2987-5d2f-a1f8-a110778bce61/scratchpad/'
lines=open('seeds_n12.txt').read().splitlines()
tests=[open('reader.txt').read().strip()]+random.Random(5).sample(lines,6)
for sl in tests:
    open(SP+'one.txt','w').write(sl+"\n")
    out=subprocess.run(['env','FULL=1','./filt',SP+'one.txt','3','0','1'],capture_output=True,text=True).stdout
    t=sl.split(); n=int(t[1]); O=list(map(int,t[2:]))
    for l in out.splitlines():
        f=l.split()
        if f[-1]=='T0': continue
        sid,a,b,ap,bp=map(int,f[:5]); typ=f[-1]
        phi,_=make_phi(O,a,b,ap,bp)
        best,M,R0=transfer(O,a,b,ap,bp); hs=hseq(M,R0,2)
        ex=[]
        for K in (0,1,2):
            cs=copies(O,phi,K); S=sorted(set(x for c in cs for x in c)); ex.append(alpha_exact(S,aps_of(S)))
        print(typ,(a,b,ap,bp),'transfer',hs,'exact',ex,'OK' if hs==ex else 'DIFF')
