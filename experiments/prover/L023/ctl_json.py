"""(L023) Compare realize_sdr.decide with rexact.py's JSON results (class by class: verdict and number of realizable labellings).
usage: python3 ctl_json.py results_X.json"""
import sys, json, time
sys.path.insert(0, '/home/user/Erdos-757/experiments/prover/L023')
from realize_sdr import decide
R = json.load(open(sys.argv[1])); ag = dis = 0
for r in R:
    E = [tuple(e) for e in r['edges']]; n = r['n']
    if len(E) != n - 2: print('SKIP class', r['cls'], 'not saturated'); continue
    t0 = time.time(); st, ex = decide(E, n)
    ok = (bool(st['REAL']) == r['realizable']) and (st['REAL'] == r['realizable_labellings'])
    ag += ok; dis += (not ok)
    print('CLASS %d n=%d mine=%s labellings_REAL=%d rexact=%s rexact_labellings=%d %s %s secs=%.1f' % (r['cls'], n, 'REAL' if st['REAL'] else 'NOT', st['REAL'],
          'REAL' if r['realizable'] else 'NOT', r['realizable_labellings'], 'AGREE' if ok else 'DISAGREE', json.dumps(st), time.time() - t0), flush=True)
print('SUMMARY classes %d agree %d disagree %d' % (ag + dis, ag, dis))
