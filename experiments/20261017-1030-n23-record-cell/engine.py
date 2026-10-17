"""Recursive reconstruction engine for connected cells (n,m,t,Delta): iso classes of CONNECTED linear graphs, F7-free, e(S)<=|S|-2, n vertices, m edges,
tau>=t (determined by slack), max degree <= Delta (Delta=3 or 4).
 - m <= MD: direct DFS (conn_dfs3, maxdeg Delta), then F7 / e(S) filters, iso dedupe.
 - else: for each possible maximum degree d (ceil(3m/n)..Delta) of X: remove a max-degree vertex w: X-w has n-1 vertices, m-d edges, maxdeg<=d, tau' in {t-1 (always), t (only if slack_X>=3+2d)},
   components = connected cells (incl. isolated vertex, slack 3) with slack sum S'; recurse on components with Delta=d; take disjoint unions; re-insert w with ext3 (d disjoint pairs,
   tau(X)>=t, F7-free, Hall e(S)); keep connected results; iso dedupe."""
import re,sys,json,subprocess,itertools,os,time,math
sys.path.insert(0,'/home/user/Erdos-757'); sys.path.insert(0,'.')
import networkx as nx
from parts import parts
from gutil import graph
from e757.cpsat_model import find_f7
from post import sub_ok
import dedupe_fast as DF
MD=10; LIMIT=400000
MEMO={}; LOG=[]
def log(*a):
    s=' '.join(str(x) for x in a); print(s,flush=True); LOG.append(s)
def parse_found(txt):
    for l in txt.splitlines():
        if l.startswith('FOUND') and l.endswith(')'): yield [tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
def parse_hits(txt):
    for l in txt.splitlines():
        if l.startswith('HIT:'): yield [tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
def connected_all(es,n):
    par=list(range(n))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for e in es:
        for v in e[1:]: par[f(v)]=f(e[0])
    return len({f(v) for v in range(n)})==1
def iso_dedupe(graphs):
    seen={}; reps=[]
    for es in graphs:
        key=tuple(sorted(DF.comp_id(c) for c in DF.components(es)))
        if key in seen: continue
        seen[key]=1; reps.append(es)
    return reps
def union(parts_):
    es=[];off=0
    for nv,p in parts_:
        es+=[tuple(v+off for v in e) for e in p]; off+=nv
    return es,off
def cell(n,m,t,D):
    key=(n,m,t,D)
    if key in MEMO: return MEMO[key]
    if (n,m)==(1,0): MEMO[key]=[[]]; return MEMO[key]
    t0=time.time()
    if m<=MD: res=direct(n,m,t,D)
    else: res=recurse(n,m,t,D)
    log('CELL',key,'classes',len(res),'secs',round(time.time()-t0,1))
    MEMO[key]=res; return res
def direct(n,m,t,D):
    f='out/K_%d_%d_%d_D%d.txt'%(n,m,t,D)
    if not os.path.exists(f) or 'DONE' not in open(f).read()[-300:]:
        subprocess.run('nice -n 10 ./conn_dfs3 %d %d %d %d 0 0 > %s'%(n,m,t,D,f),shell=True,check=True)
    txt=open(f).read(); last=txt.strip().splitlines()[-1]
    nodes=int(re.search(r'nodes=(\d+)',last).group(1)); found=int(re.search(r'found=(\d+)',last).group(1))
    reps=iso_dedupe(g for g in parse_found(txt) if not find_f7(g))
    reps=[g for g in reps if sub_ok(g,n)]
    log('  direct DFS',(n,m,t,D),'nodes',nodes,'labelled',found,'classes F7-free e(S)ok',len(reps))
    return reps
def gprime(N,M,S,d):
    P=parts(N,M,S); out=[]; nparts=len(P)
    for p in P:
        groups={}
        for c in p: groups.setdefault(c[:3],[]).append(c)
        gl=[]; size=1
        for key,cs in groups.items():
            cls=cell(key[0],key[1],key[2],d)
            idx=list(itertools.combinations_with_replacement(range(len(cls)),len(cs)))
            gl.append((key,cls,idx)); size*=len(idx)
        if size>LIMIT: raise RuntimeError('partition product too large: %s -> %d'%([c[:4] for c in p],size))
        for combo in itertools.product(*[g[2] for g in gl]):
            pp=[]
            for (key,cls,_),idxs in zip(gl,combo):
                for i in idxs: pp.append((key[0],cls[i]))
            es,nv=union(pp); assert nv==N; out.append(es)
    return out,P
def run_ext(Gs,nG,T,d,epdeg,tag):
    inp='out/in_%s.txt'%tag; outf='out/hits_%s.txt'%tag
    with open(inp,'w') as f:
        for es in Gs: f.write("%d "%len(es)+" ".join("%d %d %d"%tuple(e) for e in es)+"\n")
    t0=time.time()
    subprocess.run('nice -n 10 ./ext3 %d %d %d %d < %s > %s'%(nG,T,d,epdeg,inp,outf),shell=True,check=True)
    last=open(outf).read().strip().splitlines()[-1]
    log('  EXT',tag,last,'secs',round(time.time()-t0,1))
    return list(parse_hits(open(outf).read())),last
def recurse(n,m,t,D):
    X=[]; slackX=3*n+2*m-11*t
    for d in range(max(2,math.ceil(3*m/n)),D+1):
        for tp in (t-1,t):
            if tp==t and slackX<3+2*d: continue
            Sp=3*(n-1)+2*(m-d)-11*tp
            if Sp<0: continue
            Gs,P=gprime(n-1,m-d,Sp,d)
            log('  RECURSE',(n,m,t,D),'d=%d tau\'=%d slack\'=%d partitions=%d G-prime=%d'%(d,tp,Sp,len(P),len(Gs)))
            if not Gs: continue
            hits,last=run_ext(Gs,n-1,t,d,d-1,'c_%d_%d_%d_D%d_d%d_tp%d'%(n,m,t,D,d,tp))
            X+=[h for h in hits if connected_all(h,n)]
    reps=iso_dedupe(X)
    log('  RESULT',(n,m,t,D),'connected iso classes',len(reps))
    return reps
