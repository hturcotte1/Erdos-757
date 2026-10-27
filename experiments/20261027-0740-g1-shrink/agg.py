"""Aggregate d1_results.json and d2_patterns_*.jsonl.gz into results.json, patterns.json (D1 survivors), patterns_d2.jsonl.gz."""
import json, gzip, glob, collections
from g1lib import load_pieces, slack
PI = {P.name: P for P in load_pieces()}
d1 = json.load(open('d1_results.json'))
res = {'D1': {}, 'D2_per_piece': {}, 'D2_per_pair': {}}
keys1 = ['total', 'void_no_outer', 'notC', 'killedI11', 'killedKT', 'survive']
for name, c in d1['counts'].items():
    res['D1'][name] = {k: c[k] for k in keys1}
    res['D1'][name]['I11_formula_kill_all'] = c['I11_formula_kill_all']
res['D1']['TOTAL'] = {k: sum(v[k] for n, v in res['D1'].items() if n != 'TOTAL') for k in keys1 + ['I11_formula_kill_all']}
# patterns.json: D1 survivors with exact parameters
pat = {}
for name, lst in d1['survivors'].items():
    P = PI[name]
    pat[name] = [dict(traces=r['traces'], k=r['k'], outer=r['outer'], full=r['full'], min_s_k0=r['min_s_k0']) for r in lst]
json.dump(pat, open('patterns.json', 'w'))
prof = collections.Counter(); mins = None; outer_d = collections.Counter()
for name, lst in pat.items():
    for r in lst:
        prof[(r['k'], tuple(sorted(len(q) for q in r['traces'])))] += 1
        outer_d[r['outer']] += 1
        ms = r['min_s_k0']['s']
        if mins is None or ms < mins[0]: mins = (ms, name, r['traces'])
res['D1_profile'] = {str(k): v for k, v in sorted(prof.items())}
res['D1_outer_vertices_distribution'] = dict(outer_d)
res['D1_min_sub_extension_slack_over_survivors'] = dict(s=mins[0], piece=mins[1], traces=mins[2])
# D2
keys2 = ['claimB', 'killed_I11', 'killed_KT_only', 'notC_among_unkilled', 'survive_C']
perpiece = collections.defaultdict(lambda: collections.Counter())
perpair = {}
d2_outer = collections.Counter(); d2_mins = [None]
with gzip.open('patterns_d2.jsonl.gz', 'wt') as out:
    for fn in sorted(glob.glob('d2_patterns_*.jsonl.gz')):
        def lines(fn=fn):
            try:
                for l in gzip.open(fn, 'rt'): yield l
            except EOFError: return
        for line in lines():
            r = json.loads(line); c = r['counts']
            a, b = r['F1'], r['F2']
            perpair[a + ' x ' + b] = {k: c[k] for k in keys2}
            for nm in ({a, b}):
                for k in keys2: perpiece[nm][k] += c[k]
                perpiece[nm]['pairs'] += 1
            P1, P2 = PI[a], PI[b]
            rows = []
            for sv in r['survivors']:
                outer = sum(2 - len(x[0]) - len(x[1]) for x in sv)
                n = P1.n + P2.n + 1 + outer; m = P1.m + P2.m + 3; tau = P1.tau + P2.tau + 1   # Claim B => t = 1
                rows.append(dict(types=sv, n=n, m=m, tau=tau, s=slack(n, m, tau), outer=outer)); d2_outer[outer] += 1
                if d2_mins[0] is None or slack(n, m, tau) < d2_mins[0]['s']: d2_mins[0] = dict(s=slack(n, m, tau), n=n, pair=[a, b], types=sv)
            out.write(json.dumps(dict(F1=a, F2=b, survivors=rows)) + '\n')
res['D2_per_piece'] = {k: dict(v) for k, v in perpiece.items()}
res['D2_per_pair'] = perpair
res['D2_profile_outer'] = dict(d2_outer)
res['D2_min_full_slack'] = d2_mins[0]
res['D2_TOTAL_over_pairs'] = {k: sum(v[k] for v in perpair.values()) for k in keys2}
res['D2_pairs_done'] = len(perpair)
json.dump(res, open('results.json', 'w'), indent=1)
print(json.dumps(res['D1']['TOTAL']), json.dumps(res['D2_TOTAL_over_pairs']), 'pairs', len(perpair))
