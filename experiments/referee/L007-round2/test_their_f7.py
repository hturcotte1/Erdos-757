"""Test the authors' F7 detectors (prover f7check.has_f7 = Lemma F test; falsifier e757.cpsat_model.find_f7)
against my definitional detector det_A on controls and random linear 3-graphs (positive and negative cases)."""
import sys, random, itertools, importlib.util, json
sys.path.insert(0, '/home/user/Erdos-757')
from f7_ref import det_A, det_B, is_linear, F7
spec = importlib.util.spec_from_file_location('f7check', '/home/user/Erdos-757/experiments/prover/L007/indep/f7check.py')
f7check = importlib.util.module_from_spec(spec); spec.loader.exec_module(f7check)
from e757.cpsat_model import find_f7
rng = random.Random(7)
stats = dict(tested=0, withF7=0, disagree_prover=0, disagree_falsifier=0)
def check(es):
    a = det_A(es); p = f7check.has_f7(es); q = len(find_f7(es)) > 0
    stats['tested'] += 1; stats['withF7'] += a
    stats['disagree_prover'] += (a != p); stats['disagree_falsifier'] += (a != q)
# controls: F7 under random relabellings, embedded in random linear supergraphs
for t in range(300):
    n = rng.randint(7, 14); perm = rng.sample(range(n), 7)
    es = [tuple(sorted(perm[v] for v in e)) for e in F7]
    for _ in range(300):
        e = tuple(sorted(rng.sample(range(n), 3)))
        if e not in es and is_linear(es + [e]): es.append(e)
        if len(es) >= rng.randint(5, 13): break
    rng.shuffle(es); check(es)
# random linear graphs (mostly F7-free)
for t in range(1500):
    n = rng.randint(7, 14); es = []
    target = rng.randint(5, 14)
    for _ in range(400):
        e = tuple(sorted(rng.sample(range(n), 3)))
        if e not in es and is_linear(es + [e]): es.append(e)
        if len(es) >= target: break
    check(es)
# count of F7 copies agreement (find_f7 returns all copies): compare with brute-force copy count
def count_A(es):
    from f7_ref import COPIES
    c = 0
    for five in itertools.combinations([tuple(sorted(e)) for e in es], 5):
        U = sorted(set().union(*five))
        if len(U) != 7: continue
        r = {v: i for i, v in enumerate(U)}
        c += frozenset(tuple(sorted(r[v] for v in e)) for e in five) in COPIES
    return c
cc = 0
for t in range(300):
    n = rng.randint(7, 11); es = []
    for _ in range(400):
        e = tuple(sorted(rng.sample(range(n), 3)))
        if e not in es and is_linear(es + [e]): es.append(e)
    if count_A(es) != len(find_f7(es)): cc += 1
stats['copycount_mismatch_find_f7_on_300_maximal_linear'] = cc
print(json.dumps(stats))
