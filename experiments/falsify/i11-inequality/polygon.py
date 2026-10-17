import json, itertools
from fractions import Fraction as F
T={tuple(map(int,k.split(','))):v for k,v in json.load(open('results_tau_max_union.json')).items()}
cells=[(n,m,v[0]) for (n,m),v in T.items() if n>=3]
cons=[(F(n),F(m),F(t)) for n,m,t in cells]+[(F(1),F(0),F(0)),(F(0),F(1),F(0))]  # n a + m b >= t ; a>=0 -> 1*a>=0 ; b>=0
def feas(a,b): return all(n*a+m*b>=t for n,m,t in cons)
V=set()
for (n1,m1,t1),(n2,m2,t2) in itertools.combinations(cons,2):
    det=n1*m2-n2*m1
    if det==0: continue
    a=(t1*m2-t2*m1)/det; b=(n1*t2-n2*t1)/det
    if feas(a,b): V.add((a,b))
V=sorted(V)
res=[dict(a=str(a),b=str(b),a_plus_b=float(a+b),tight=[(int(n),int(m),int(t)) for n,m,t in cons if n*a+m*b==t and n>=3]) for a,b in V]
for r in res: print(r['a'],r['b'],round(r['a_plus_b'],4),r['tight'][:6])
json.dump(res,open('results_polygon_vertices.json','w'),indent=1)
