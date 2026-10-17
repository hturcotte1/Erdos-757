"""Referee round 2 (L008): input sets for i11_sets.  Writes data_tests/basic_sets.txt (+ names), census14.txt, census12.txt,
ext15.txt from data/ (exact integers).  Gluings A u (qB + 10^12) with the first q in a fixed list making the union a (4,5)-set."""
import json, gzip, itertools
D = '/home/user/Erdos-757/data/'
out = open('data_tests/basic_sets.txt', 'w'); names = []
d = json.load(open(D + 'small_records.json'))
for k, v in d['sets'].items():
    s = v['set'] if isinstance(v, dict) else v
    out.write(' '.join(map(str, s)) + '\n'); names.append('small_records:' + k)
AB = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]
C16 = sorted(AB + [-323, 5000])
fib = [2, 3]
while len(fib) < 18: fib.append(fib[-1] + fib[-2])
for nm, s in [('A_base', AB), ('C16', C16), ('FIB_F3..F18 (16)', fib[:16]), ('FIB_F3..F20 (18)', fib[:18]),
              ('S12_third', [0,269,385,467,501,511,521,523,535,538,549,575])]:
    out.write(' '.join(map(str, s)) + '\n'); names.append(nm)
def is45(A):
    return all(len({abs(x - y) for x, y in itertools.combinations(q, 2)}) >= 5 for q in itertools.combinations(A, 4))
S12 = d['sets']['12']['set'] if isinstance(d['sets']['12'], dict) else d['sets']['12']
for nm, base, B in [('glue A_base+A_base', AB, AB), ('glue A_base+S12', AB, S12), ('glue S12+S12', S12, S12)]:
    for q in [7919, 104729, 1299709, 15485863]:
        G = sorted(set(base) | {q * b + 10**12 for b in B})
        if len(G) == len(base) + len(B) and is45(G):
            out.write(' '.join(map(str, G)) + '\n'); names.append('%s q=%d n=%d' % (nm, q, len(G))); break
out.close(); json.dump(names, open('data_tests/basic_names.json', 'w'))
for src, dst in [('census_n14_m12_classes.jsonl.gz', 'census14.txt'), ('ext12_all_rows.jsonl.gz', 'census12.txt'), ('ext15_sets.jsonl.gz', 'ext15.txt')]:
    with gzip.open(D + src, 'rt') as f, open('data_tests/' + dst, 'w') as g:
        for l in f: g.write(' '.join(map(str, json.loads(l)['set'])) + '\n')
print(names)
