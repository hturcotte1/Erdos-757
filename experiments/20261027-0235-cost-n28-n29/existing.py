import os, plan2, model
from model import *
orig = lambda k: os.path.exists(os.path.join(plan2.CELLS, 'cell_%d_%d_%d_D%d.txt' % k))
used = {}
for nm in ('n28', 'n29rec', 'n29full', 'rec25'):
    for k in build(tops_for(nm)):
        if k in KNOWN: used.setdefault(k, set()).add(nm)
L = ['cell(n,m,tau,Delta)\tclasses\torigin\ttargets']
for k in sorted(used, key=lambda k: (k[0], k[1], k[3])):
    L.append('%s\t%d\t%s\t%s' % (k, KNOWN[k], 'old (L012-L016/n27 lists)' if orig(k) else 'computed here or by the d4 worker', ','.join(sorted(used[k]))))
open('existing_cells_used.tsv', 'w').write('\n'.join(L) + '\n'); print(len(L) - 1, 'cells known/used;', sum(1 for k in used if orig(k)), 'old')
