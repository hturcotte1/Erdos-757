import sys, re, random, importlib.util
sys.path.insert(0,'/home/user/Erdos-757')
from reff7 import contains, linear, F7
spec=importlib.util.spec_from_file_location('f7check','/home/user/Erdos-757/experiments/prover/L007/indep/f7check.py'); f7c=importlib.util.module_from_spec(spec); spec.loader.exec_module(f7c)
from e757.cpsat_model import find_f7
def parse(path,tag='CLASS'):
    return [[tuple(sorted(map(int,t.split(',')))) for t in re.findall(r'\(([\d,]+)\)',l)] for l in open(path) if l.startswith(tag)]
# controls through all three detectors
fano=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
pts=[(x,y) for x in range(3) for y in range(3)]; lines=set()
for p in pts:
    for d in [(0,1),(1,0),(1,1),(1,2)]: lines.add(frozenset(((p[0]+t*d[0])%3*3+(p[1]+t*d[1])%3) for t in range(3)))
ag=[tuple(sorted(L)) for L in lines]
l13=[tuple(sorted({i%13,(i+1)%13,(i+3)%13})) for i in range(13)]
ctrl={'F7':(F7,True),'AG23':(ag,True),'F8':([L for L in ag if 8 not in L],True),'Fano':(fano,False),'Fano-2':(fano[:5],False),'L13':(l13,False),'F7-1':(F7[:4],False),'F7mod':(F7[:4]+[(2,4,7)],False)}
for k,(E,w) in ctrl.items():
    r=(contains(E),f7c.has_f7(E),len(find_f7(E,limit=1))>0); print(f'control {k:7s} expected={w} ref/prover/falsifier={r}', 'OK' if r==(w,w,w) else 'WRONG')
for path in sys.argv[1:]:
    G=parse(path)
    res=[(contains(E),linear(E)) for E in G]
    print(path, 'classes',len(G),'contain_F7',sum(a for a,b in res),'F7_free',sum(not a for a,b in res),'all_linear',all(b for a,b in res))
