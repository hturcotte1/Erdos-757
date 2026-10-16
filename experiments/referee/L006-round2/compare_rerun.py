import gzip, json
ROOT = '/home/user/Erdos-757'
ids = json.load(open(ROOT + '/experiments/referee/L006-round2/rerun_ids.json'))
rows = {r['class']: r for r in (json.loads(l) for l in gzip.open(ROOT + '/data/ext12_all_rows.jsonl.gz', 'rt'))}
mine = [json.loads(l) for l in open(ROOT + '/experiments/referee/L006-round2/rerun_out/results.jsonl')]
assert len(mine) == len(ids) == len({r['class'] for r in mine})
same = 0; bad = []
for r in mine:
    orig = ids[r['class']]
    st = rows[orig]
    a = {k: v for k, v in r.items() if k not in ('secs', 'class')}
    b = {k: v for k, v in st.items() if k not in ('secs', 'class')}
    if a == b: same += 1
    else: bad.append((orig, {k: (a.get(k), b.get(k)) for k in set(a) | set(b) if a.get(k) != b.get(k)}))
print(f'{same}/{len(mine)} rerun rows identical to stored rows (all fields except class index and secs)')
for b in bad[:10]: print('MISMATCH', b)
print('classes:', ids[:12], '...', ids[-8:])
