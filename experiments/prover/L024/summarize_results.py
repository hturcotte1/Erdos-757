"""L024: print the totals and per-type counts stored in the pattern_a3 result files (the evidence of record; the text logs
of runs longer than about 100 s in the foreground lost their last lines, see README).
Run: timeout 300 nice -n 10 python3 summarize_results.py > results_summary.txt"""
import json, collections
for f in ['pattern_a3_small_results.json', 'pattern_a3_poor_results.json', 'pattern_a3_richcheck_results.json']:
    D = json.load(open('/home/user/Erdos-757/experiments/prover/L024/' + f))
    print(f, 'TOTALS', D['totals'])
    per = collections.Counter(); inc = collections.Counter(); ce = collections.Counter(); pmin = {}
    for r in D['configs']:
        t = tuple(r['types']); per[t] += 1
        if r['claimE']: ce[t] += 1
        if r['inC3']:
            inc[t] += 1
            pmin[t] = min(pmin.get(t, 10 ** 9), r['P_lower'])
    for t in sorted(per):
        print('  ', t, 'configs', per[t], 'claimE', ce[t], 'inC3', inc[t], 'min P over inC3', pmin.get(t))
