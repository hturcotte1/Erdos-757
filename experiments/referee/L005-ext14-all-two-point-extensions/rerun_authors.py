"""Rerun the AUTHORS' extend_all.process (their code, unmodified, imported from their directory) on chosen classes
and compare every output field except 'secs' with the stored row of results.jsonl. Also runs the --abase-test input."""
import sys, json, gzip, os, time
EXP = '/home/user/Erdos-757/experiments/20261015-2340-ext14-all'
sys.path.insert(0, EXP)
import extend_all  # authors' code
os.nice(15)
classes = json.load(open('picked.json'))['classes']
sets = [json.loads(l)['set'] for l in gzip.open('/home/user/Erdos-757/data/census_n14_m12_classes.jsonl.gz', 'rt') if l.strip()]
rows = {json.loads(l)['class']: json.loads(l) for l in open(EXP + '/results.jsonl')}
out = []
t0 = time.time()
mism = 0
for c in classes:
    r = extend_all.process((c, sets[c]))
    r = json.loads(json.dumps(r))
    a = dict(rows[c]); a.pop('secs'); r.pop('secs')
    eq = (a == r)
    if not eq:
        mism += 1
    out.append({'class': c, 'equal_to_stored_row': eq, 'n_t1b_45': r['n_t1b_45'], 'n_single_45': r['n_single_45'],
                'min_h': r['min_h'], 'records': r['records']})
    print(c, eq, r['Px_size'], r['n_single_45'], r['t1_pairs'], r['n_t1b_45'], r['t2_isect_pts'], r['min_h'], flush=True)
ab = extend_all.process((0, [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]))
ab.pop('secs')
print('abase-test', {k: v for k, v in ab.items() if k not in ('set', 'hist')}, ab['hist'])
print('classes rerun', len(classes), 'mismatches', mism, 'time', round(time.time() - t0))
json.dump({'rows': out, 'abase_test': ab, 'mismatches': mism}, open('rerun_authors_out.json', 'w'), indent=1)
