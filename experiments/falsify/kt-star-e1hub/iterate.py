#!/usr/bin/env python3
"""Iterate the hub construction: read type-'H' records (graphs in C_3 with tau known) from IN files, apply every b-configuration
hub, keep new H in C_3, write type-'H' records to OUT.  usage: iterate.py OUT.jsonl IN1.jsonl [IN2.jsonl ...]  (env MAXN to cap n of inputs)"""
import sys, json, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hubs, kt
out = open(sys.argv[1], 'a'); ins = sys.argv[2:]
MAXN = int(os.environ.get('MAXN', '99'))
reg = hubs.Registry()
stats = dict(inputs=0, bconf_labelled=0, new_classes=0, inC=0, minP=None, hits=0, by_cell={}, notinT=0)
t0 = time.time()
seen_in = hubs.Registry()
for fn in ins:
    for l in open(fn):
        d = json.loads(l)
        if d.get('type') not in ('H','UV','FH'): continue
        n, E, t = d['n'], [tuple(e) for e in d['H']], d['tau']
        if n > MAXN: continue
        rec, new = seen_in.lookup(n, E)   # dedupe inputs across files
        if not new: continue
        stats['inputs'] += 1
        bc, nT, notin = hubs.bconfigs(n, E, t)
        stats['notinT'] += len(notin)
        stats['bconf_labelled'] += len(bc)
        for (a, b, c) in bc:
            n2, E2 = hubs.add_hub(n, E, a, b, c)
            rec2, new2 = reg.lookup(n2, E2)
            if not new2: continue
            stats['new_classes'] += 1
            r = hubs.analyse_H(n2, E2, t + 2)
            if not r['inC']: continue
            stats['inC'] += 1
            key = '(%d,%d,%d)' % (r['n'], r['m'], r['tau'])
            stats['by_cell'][key] = stats['by_cell'].get(key, 0) + 1
            if stats['minP'] is None or r['P'] < stats['minP']: stats['minP'] = r['P']
            out.write(json.dumps(dict(type='H', src=d.get('src', d.get('cell', d['type'])) + '>iter', G=E, abc=(a, b, c), n=r['n'], m=r['m'], tau=r['tau'], A=r['A'], DEF=r['DEF'], DEFp=r['DEFp'], P=r['P'], Pp=r['Pp'], piece=r['piece'], H=E2)) + '\n'); out.flush()
            if r['P'] < 0 or (r['piece'] is None and r['Pp'] < 0):
                stats['hits'] += 1
                print('HIT', r, E2, flush=True)
        if stats['inputs'] % 20 == 0:
            print({k: v for k, v in stats.items() if k != 'by_cell'}, '[%.0fs]' % (time.time() - t0), flush=True)
print('FINAL', stats, flush=True)
json.dump(stats, open(sys.argv[1] + '.stats.json', 'w'), indent=1)
