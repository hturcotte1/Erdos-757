"""For each new cell: every component cell (type, D=d of the branch) used by the decompositions, and where its list comes from:
'refereed' = identical (as sets of FOUND lines) to a file in experiments/prover/L017/out (extracted L012-L016 tarballs);
otherwise the first source and agreeing sources recorded by the 0340 worker's provenance.json (all unrefereed)."""
import json, os, re, glob, sys
H = '/home/user/Erdos-757/experiments'
prov = json.load(open(H + '/20261027-0340-induction-n28-n29-f25/provenance.json'))
ref = {}
for p in glob.glob(H + '/prover/L017/out/**/cell_*', recursive=True):
    m = re.search(r'cell_(\d+)_(\d+)_(\d+)_D(\d+)\.txt$', p)
    if m: ref.setdefault(tuple(map(int, m.groups())), p)
def found(p): return frozenset(l.strip() for l in open(p) if l.startswith('FOUND'))
out = {}
for key in ['25,14,9,3', '26,17,10,3', '27,13,9,3', '27,20,11,3']:
    n, m, t, D = map(int, key.split(','))
    txt = open(f'out/cells/cell_{n}_{m}_{t}_D{D}.txt').read().splitlines()
    info = json.loads([l for l in txt if l.startswith('INFO')][0][5:])
    comps = set()
    for b in info['branches']:
        for dec, cnt in b['dec']:
            for typ in dec:
                if typ[0] == 1 and typ[1] == 0: continue
                comps.add((typ[0], typ[1], typ[2], b['d']))
    res = []
    for c in sorted(comps):
        f = f'out/cells/cell_{c[0]}_{c[1]}_{c[2]}_D{c[3]}.txt'
        if not os.path.exists(f): res.append((c, 'MISSING')); continue
        mine = found(f)
        # refereed file with same key and D (or larger D: restrict to degree<=D is not done; require same key)
        r = ref.get(c)
        if r is not None and found(r) == mine: res.append((c, len(mine), 'refereed (identical to L017/out copy)'))
        elif r is not None: res.append((c, len(mine), 'DIFFERS from refereed copy!'))
        elif not os.path.islink(f) and c in [(25,14,9,3),(26,17,10,3),(27,13,9,3),(27,20,11,3)]:
            res.append((c, len(mine), 'COMPUTED IN THIS FOLDER (own run, see progress.tsv)'))
        else:
            pv = prov.get('%d,%d,%d,%d' % c)
            res.append((c, len(mine), 'no refereed copy; ' + (pv['first'] + ' | agree: ' + '; '.join(pv['agree']) if pv else 'no provenance row') + (' | DISAGREE ' + str(pv['disagree']) if pv and pv['disagree'] else '')))
    out[key] = res
json.dump(out, open('deps_provenance.json', 'w'), indent=1, default=str)
for k, v in out.items():
    nref = sum(1 for x in v if x[-1].startswith('refereed')); print(k, 'components', len(v), 'refereed-identical', nref)
    for x in v:
        if not x[-1].startswith('refereed'): print('   ', x)
