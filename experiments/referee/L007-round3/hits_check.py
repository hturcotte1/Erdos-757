import sys, re
sys.path.insert(0,'.')
from reff7 import contains, linear
def parse(path,tag):
    return [[tuple(sorted(map(int,t.split(',')))) for t in re.findall(r'\(([\d,]+)\)',l)] for l in open(path) if l.startswith(tag)]
def components(E):
    V=set().union(*map(set,E)); par={v:v for v in V}
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for e in E:
        for v in e[1:]: par[f(v)]=f(e[0])
    return len({f(v) for v in V})
def maxdeg(E):
    d={}
    for e in E:
        for v in e: d[v]=d.get(v,0)+1
    return max(d.values())
def f7_uses(E,v):
    # does every F7 copy use vertex v?  <=> H - v (edges avoiding v) is F7-free
    return not contains([e for e in E if v not in e])
mine=parse('out/ext_ref_hits.txt','HIT:')
print('my hits',len(mine),'contain F7:',sum(contains(E) for E in mine),'linear:',all(linear(E) for E in mine))
for path in sys.argv[1:]:
    H=parse(path,'HIT:')
    c=sum(contains(E) for E in H)
    print(path,'hits',len(H),'contain F7',c,'linear',all(linear(E) for E in H),
          'components hist',{k:sum(1 for E in H if components(E)==k) for k in (1,2,3)},
          'maxdeg hist',{k:sum(1 for E in H if maxdeg(E)==k) for k in (3,4,5)})
