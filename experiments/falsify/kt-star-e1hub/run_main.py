#!/usr/bin/env python3
"""Main pass: every stored connected Delta<=3 class G' with A(G')<=15 -> all b-configurations -> hubs H.
usage: run_main.py OUT.jsonl cellkey1 cellkey2 ...   (cellkey like 20,15,8) or 'all' ; env PART=i/k splits cell list."""
import sys, json, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hubs, kt
inv = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventory.json')))
out = open(sys.argv[1], 'a', buffering=1)
nwrit = 0
keys = sys.argv[2:]
cells = sorted(inv, key=lambda k: eval(k))
if keys != ['all']:
    want = set(tuple(map(int, k.split(','))) for k in keys)
    cells = [c for c in cells if eval(c) in want]
reg = hubs.Registry()
def good(g):
    n = kt.nverts(g); d = hubs.degs(n, g)
    return max(d) <= 3
tot = dict(cells=0, graphs=0, bconf=0, hubs_classes=0, hubs_inC=0, minP=None, minPp_new=None, hits=0)
t0 = time.time()
for ck in cells:
    n0, m0, t_ = eval(ck); info = inv[ck]
    gs = [g for g in kt.read_cell(info['file']) if good(g)]
    if not gs:
        out.write(json.dumps(dict(type='cell', cell=ck, A=info['A'], D=info['D'], graphs=0, file=info['file'].split('experiments/')[-1])) + '\n'); out.flush()
        continue
    st = dict(type='cell', cell=ck, A=info['A'], D=info['D'], file=info['file'].split('experiments/')[-1], graphs=0, nonconnected=0, bconf_labelled=0,
              graphs_with_bconf=0, notinT_low_vertices=0, hub_classes_new=0, hub_inC=0, hubs_by_cell={}, minP=None, minPp_nonpiece=None, hits=[])
    for g in gs:
        n = kt.nverts(g); m = len(g)
        assert n == n0 and m == m0
        t = kt.tau_masks(kt.masks(g)); assert t == t_, (ck, t)
        st['graphs'] += 1
        bc, nT, notin = hubs.bconfigs(n, g, t)
        st['notinT_low_vertices'] += len(notin)
        if bc: st['graphs_with_bconf'] += 1
        st['bconf_labelled'] += len(bc)
        for (a, b, c) in bc:
            n2, E2 = hubs.add_hub(n, g, a, b, c)
            rec, new = reg.lookup(n2, E2)
            if not new:
                continue
            st['hub_classes_new'] += 1
            r = hubs.analyse_H(n2, E2, t + 2)
            rec.update(r)
            if not r['inC']: continue
            st['hub_inC'] += 1
            nwrit += 1
            out.write(json.dumps(dict(type='H', src=ck, G=g, abc=(a,b,c), n=r['n'], m=r['m'], tau=r['tau'], A=r['A'], DEF=r['DEF'], DEFp=r['DEFp'], P=r['P'], Pp=r['Pp'], piece=r['piece'], H=E2)) + '\n'); out.flush(); os.fsync(out.fileno())
            key = '(%d,%d,%d)' % (r['n'], r['m'], r['tau'])
            st['hubs_by_cell'][key] = st['hubs_by_cell'].get(key, 0) + 1
            if st['minP'] is None or r['P'] < st['minP']: st['minP'] = r['P']
            if r['piece'] is None and (st['minPp_nonpiece'] is None or r['Pp'] < st['minPp_nonpiece']): st['minPp_nonpiece'] = r['Pp']
            if r['P'] < 0 or (r['piece'] is None and r['Pp'] < 0):
                st['hits'].append(dict(G=g, abc=(a, b, c), H=E2, **r))
                print('HIT', ck, a, b, c, r, flush=True)
    out.write(json.dumps(st) + '\n'); out.flush(); os.fsync(out.fileno())
    print('H records written', nwrit)
    print(ck, {k: v for k, v in st.items() if k not in ('hits', 'file')}, '[%.0fs]' % (time.time() - t0), flush=True)
