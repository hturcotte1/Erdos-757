"""Independent numpy re-implementation of the vertex-extension step for a random sample of G's; compares #hits with ext_vertex."""
import re, itertools, random, subprocess, numpy as np
random.seed(5)
lines=[l.split() for l in open('ext_vertex_input.txt')]
idx=random.sample(range(len(lines)),25)
five=np.array([sum(1<<v for v in c) for c in itertools.combinations(range(14),5)],dtype=np.int64)
tot_hits=0; tot_tested=0; ref_hits=0
for i in idx:
    t=list(map(int,lines[i][1:])); g=[(t[3*k],t[3*k+1],t[3*k+2]) for k in range(len(t)//3)]
    gm=[sum(1<<v for v in e) for e in g]
    pairs=[(a,b) for a in range(13) for b in range(a+1,13) if not any((m>>a&1) and (m>>b&1) for m in gm)]
    Hs=[]
    for x,y,z in itertools.combinations(pairs,3):
        if len({*x,*y,*z})<6: continue
        Hs.append([(1<<a)|(1<<b)|(1<<13) for a,b in (x,y,z)])
    gm_arr=np.array(gm,dtype=np.int64)
    hits=0
    for s in range(0,len(Hs),2000):
        chunk=np.array(Hs[s:s+2000],dtype=np.int64)  # (c,3)
        c=len(chunk)
        # covered[c,5sets]: all G edges hit & all 3 new edges hit
        okg=np.ones(len(five),dtype=bool)
        for em in gm_arr: okg&=((five&em)!=0)
        cand=five[okg]   # 5-sets covering G
        cov=np.ones((c,len(cand)),dtype=bool)
        for j in range(3): cov&=((cand[None,:]&chunk[:,j:j+1])!=0)
        hits+=int((~cov.any(axis=1)).sum())   # no 5-cover => tau>=6
    tot_hits+=hits; tot_tested+=len(Hs)
    inp="8 "+" ".join(lines[i][1:])+"\n"
    out=subprocess.run(['./ext_vertex'],input=inp,capture_output=True,text=True).stdout.strip().splitlines()[-1]
    r=int(re.search(r'hits\(tau>=6\)=(\d+)',out).group(1)); ref_hits+=r
    assert r==hits,(i,r,hits)
print('25 sampled G: python hits',tot_hits,'C hits',ref_hits,'tested',tot_tested)
