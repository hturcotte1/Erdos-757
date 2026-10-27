import os,sys,itertools,subprocess
os.environ['CELLDIR']=os.path.abspath('out/cells'); os.environ['ENGINELOG']='/dev/null'
sys.path.insert(0,'src'); import engine
n,m,d,tp=24,19,4,9; lines=[]
Sp=3*(n-1)+2*(m-d)-11*tp
for dec in engine.decompositions(n-1,m-d,Sp):
    g={}
    for c in dec: g[c]=g.get(c,0)+1
    gl=[]
    for typ,k in sorted(g.items()):
        cls=engine.cell(typ[0],typ[1],typ[2],d); gl.append((typ,cls,list(itertools.combinations_with_replacement(range(len(cls)),k))))
    for combo in itertools.product(*[x[2] for x in gl]):
        es=[];off=0
        for (typ,cls,_),idxs in zip(gl,combo):
            for i in idxs: es+=[tuple(v+off for v in e) for e in cls[i]]; off+=typ[0]
        lines.append('%d '%len(es)+' '.join('%d %d %d'%e for e in es))
open('out/regress_in.txt','w').write('\n'.join(lines)+'\n'); print(len(lines))
