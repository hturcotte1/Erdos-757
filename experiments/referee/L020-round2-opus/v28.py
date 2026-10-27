"""Pattern at vertex 28 of K29 (class 0), as now described in Consequence (b) and Step 6.1."""
import json
from hgr2 import HG
from patt import analyse
d = json.load(open('/home/user/Erdos-757/experiments/prover/L020/K29_classes.json'))
E = [tuple(sorted(e)) for e in d[0]['edges']]; V = sorted(set(u for e in E for u in e))
K = HG(V, E)
r = analyse(K, 28)
print('v=28:', r)
G = K.full & ~K.inc[28]
comps, iso = K.components([u for u in V if u != 28], G)
print('components:', [(sorted(Vc)[:3], len(Vc)) for Vc, em in comps], 'isolated', iso, 'tau(K-28) =', K.tau_mask(G))
