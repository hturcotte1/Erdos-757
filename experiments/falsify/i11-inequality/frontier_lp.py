"""Exact frontier of valid inequalities  tau <= a*n + b*m  over the union data tau_max(n,m) (induced subsets of all census data).
a(b) = max_{(n,m)} (tau_max - b*m)/n  (exact Fractions).  Also the points where I11 (a,b)=(3/11,2/11) is tight."""
import json
from fractions import Fraction as F
T={tuple(map(int,k.split(','))):v for k,v in json.load(open('results_tau_max_union.json')).items()}
cells=[(n,m,v[0],v[1]) for (n,m),v in T.items() if n>=3]
def a_of(b):
    best=max(F(t)-b*m for n,m,t,_ in cells if True) if False else None
    arg=max(cells,key=lambda c:(F(c[2])-b*c[1])/c[0])
    return (F(arg[2])-b*arg[1])/arg[0],arg
out={'ncells':len(cells),'n_range':[min(c[0] for c in cells),max(c[0] for c in cells)]}
# I11 tight cells
a,b=F(3,11),F(2,11)
out['I11_tight_cells']=[dict(n=n,m=m,tau=t,src=s) for n,m,t,s in sorted(cells) if F(t)==a*n+b*m]
out['I11_violations']=[dict(n=n,m=m,tau=t) for n,m,t,s in cells if F(t)>a*n+b*m]
rows=[]
for bn in range(0,41):
    b=F(bn,34); av,arg=a_of(b)
    rows.append(dict(b=str(b),a=str(av),a_plus_b=float(av+b),a_plus_b_exact=str(av+b),tight_cell=arg[:3]))
out['frontier']=rows
best=min(rows,key=lambda r:r['a_plus_b'])
out['min_a_plus_b_on_grid']=best
# restricting to saturated-like cells m>=n-3 only (asymptotic regime)
sat=[c for c in cells if c[1]>=c[0]-3]
out['sat_cells_max_tau_over_n']=max((F(c[2],c[0]),c[:3]) for c in sat if c[0]>=10) and str(max((F(c[2],c[0]),c[:3]) for c in sat if c[0]>=10))
json.dump(out,open('results_frontier.json','w'),indent=1)
print('cells',len(cells),'I11 tight:',[(c['n'],c['m'],c['tau']) for c in out['I11_tight_cells']],'violations',out['I11_violations'])
for r in rows[::4]: print(r['b'],r['a'],round(r['a_plus_b'],4),r['tight_cell'])
print('min a+b',best)
