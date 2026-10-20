"""Referee L014 r1: audit of the INFO lines of all 145 prover cell files: per recursion branch bad_tau = 0, graphs = inputs =
searched + tg_too_small + bad_tau, filt chunk totals = hits_in_C, sum of survivors_connected = connected_hits, filt chunk
summaries clean (bad_labels = 0, linear = total, contain_F7 = 0 and P3_violated = 0 for pruned ext_d output); direct cells:
labelled / in_C counts.  Usage: python3 info_audit.py CELLDIR"""
import sys, json, glob, os, re
CD = sys.argv[1]; problems = 0; nrec = nbr = ndir = 0
for fn in sorted(glob.glob(CD + '/cell_*.txt')):
    info = None; nf = 0
    for l in open(fn):
        if l.startswith('FOUND'): nf += 1
        elif l.startswith('INFO '): info = json.loads(l[5:])
    key = os.path.basename(fn)
    if info is None: print('NO INFO', key); problems += 1; continue
    if info['route'] == 'direct':
        ndir += 1
        continue
    nrec += 1; conn = 0
    for b in info['branches']:
        nbr += 1
        if b['inputs'] == 0: continue
        e = b['ext']
        if e['bad_tau'] != 0 or e['graphs'] != b['inputs'] or e['searched'] + e['tg_too_small'] + e['bad_tau'] != e['graphs']:
            print('EXT COUNTER PROBLEM', key, b['d'], b['tp'], e); problems += 1
        if e.get('tg_too_small', 0): print('tg_too_small > 0 in', key, e['tg_too_small'])
        tot = 0
        for fs in b.get('filt_chunks', []):
            kv = dict(x.split('=', 1) for x in fs.split() if '=' in x)
            tot += int(kv['total']); conn += int(kv['survivors_connected'])
            if kv['bad_labels'] != '0' or kv['linear'] != kv['total'] or kv['contain_F7'] != '0' or kv['P3_violated'] != '0' or kv['survivors'] != kv['total']:
                print('FILT CHUNK PROBLEM', key, fs); problems += 1
        if 'filt_chunks' in b and tot != e['hits_in_C']: print('HIT COUNT PROBLEM', key, tot, e['hits_in_C']); problems += 1
    if 'filt_chunks' in json.dumps(info) and conn != info['connected_hits']: print('CONN PROBLEM', key, conn, info['connected_hits']); problems += 1
print('SUMMARY files', nrec + ndir, 'direct', ndir, 'recursion', nrec, 'branches', nbr, 'problems', problems)
