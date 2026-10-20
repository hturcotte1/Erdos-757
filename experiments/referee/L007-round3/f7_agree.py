# Compare referee F7 detector with the prover's (Lemma F, f7check.has_f7) and the falsifier's (e757 find_f7)
# on random linear 3-graphs (some with a planted F7) and on the control set.
import sys, random, itertools, importlib.util
sys.path.insert(0,'/home/user/Erdos-757')
from reff7 import contains, linear, F7
spec=importlib.util.spec_from_file_location('f7check','/home/user/Erdos-757/experiments/prover/L007/indep/f7check.py'); f7c=importlib.util.module_from_spec(spec); spec.loader.exec_module(f7c)
from e757.cpsat_model import find_f7
rnd=random.Random(20261017)
def rand_linear(n, tries, plant):
    E=[]; used=set()
    if plant:
        perm=rnd.sample(range(n),7); E=[tuple(sorted(perm[x] for x in e)) for e in F7]
        for e in E: used|=set(itertools.combinations(e,2))
    for _ in range(tries):
        e=tuple(sorted(rnd.sample(range(n),3))); ps=set(itertools.combinations(e,2))
        if ps & used: continue
        E.append(e); used|=ps
    return E
stats={'total':0,'pos':0,'disagree':0}
for it in range(6000):
    n=rnd.randint(7,13); E=rand_linear(n, rnd.randint(3,30), rnd.random()<0.3)
    assert linear(E)
    a=contains(E); b=f7c.has_f7(E); c=len(find_f7(E,limit=1))>0
    stats['total']+=1; stats['pos']+=a
    if not (a==b==c): stats['disagree']+=1; print('DISAGREE',E,a,b,c)
print(stats)
