import json, glob
R = []
for f in sorted(glob.glob('rx/full_p*.jsonl')):
    R += [json.loads(l) for l in open(f)]
ids = [r['class'] for r in R]
print('Route X rows', len(R), 'distinct classes', len(set(ids)), 'all 0..54242:', sorted(set(ids)) == list(range(54243)))
print('flags (deficient (4,5) pairs or h(A u x)=7 with A u x (4,5)):', sum(len(r['flags']) for r in R))
print('classes with nonempty core (vertex in every maximum Sidon set):', sum(1 for r in R if r['core']))
print('x with empty G_x (after parallelogram filter):', sum(r['x_empty_G'] for r in R))
print('spot classes (c % 25 == 0, slow Y_x recomputation + per-pair Sidon re-verification):', sum(1 for r in R if r['class'] % 25 == 0))
print('deficient ordered pairs (x in P_x, x passing the filter) tested for (4,5):', sum(r['deficient_ordered_pairs_x_in_Px'] for r in R))
print('n_maxT range', min(r['n_maxT'] for r in R), max(r['n_maxT'] for r in R), '; P_x range', min(r['Px'] for r in R), max(r['Px'] for r in R))
import gzip
st = {}
for l in gzip.open('/home/user/Erdos-757/data/ext12_all_rows.jsonl.gz', 'rt'):
    r = json.loads(l); st[r['class']] = r
print('n_maxT == stored n_max_sidon:', all(r['n_maxT'] == st[r['class']]['n_max_sidon'] for r in R), '; Px == stored Px_size:', all(r['Px'] == st[r['class']]['Px_size'] for r in R))
