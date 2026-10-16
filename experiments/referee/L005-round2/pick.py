import json, random, glob
R = [json.loads(l) for l in open('/home/user/Erdos-757/experiments/20261015-2340-ext14-all/results.jsonl')]
loc = {}
for f in glob.glob('/home/user/Erdos-757/experiments/referee/L005-ext14-all-two-point-extensions/locus_all*.jsonl'):
    for l in open(f):
        r = json.loads(l); loc[r['class']] = r
pick = {2440, 729, 857, 960, 1951, 2437}
for key in ['t1_pairs', 'n_t1b_45', 'n_max_sidon', 'n_single_45', 'Px_size', 't2_isect_pts']:
    pick.add(max(R, key=lambda r: r[key])['class']); pick.add(min(R, key=lambda r: r[key])['class'])
pick.add(max(loc.values(), key=lambda r: r['n_isolated_pts'])['class'])
pick.add(min(loc.values(), key=lambda r: r['n_isolated_pts'])['class'])
rng = random.Random(20261016)
while len(pick) < 100:
    pick.add(rng.randrange(2910))
pick = sorted(pick)
json.dump(pick, open('routeF_picked.json', 'w'))
print(len(pick), pick)
print(' '.join(map(str, pick[0::2])), file=open('routeF_half0.txt', 'w'))
print(' '.join(map(str, pick[1::2])), file=open('routeF_half1.txt', 'w'))
