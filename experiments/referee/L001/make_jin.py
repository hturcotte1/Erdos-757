"""Create claim-format inputs (A, 10 sets A u {x}, 40 sets A u {x,y}) in ./jin for the frozen verifier."""
import json, random, os
D = json.load(open('/home/user/Erdos-757/experiments/referee/L001/t1_out.json'))
A = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
out = '/home/user/Erdos-757/experiments/referee/L001/jin'
os.makedirs(out, exist_ok=True)
rng = random.Random(1)
items = [('L001ref-A', A, 8)]
for i, xs in enumerate(rng.sample(D['P_ok'], 10)):
    items.append((f'L001ref-Ax{i}', A + [xs], 9))
for i, (xs, ys, h, W) in enumerate(rng.sample(D['good'], 40)):
    items.append((f'L001ref-B{i}', A + [xs, ys], 10))
for cid, S, h in items:
    with open(f'{out}/{cid}.json', 'w') as f:
        json.dump({'id': cid, 'type': 'construction', 'set': [str(s) for s in S], 'claimed_h': h}, f)
print(len(items))
