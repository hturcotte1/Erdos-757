"""(L014) python3 big_table.py CELLDIR key ... : one Markdown table row per cell: key, classes, route, inputs, ext_d nodes, F7-free
extensions with the required tau, of them in C (HIT lines), connected (= kept before the canonical reduction), seconds (wall)."""
import sys, os, json
d = sys.argv[1]
print('| cell | classes | route | inputs | `ext_d` nodes | $F_7$-free ext. | in $C$ | connected | wall s |')
print('|---|---|---|---|---|---|---|---|---|')
for k in sys.argv[2:]:
    key = tuple(map(int, k.split(','))); info = None; reps = 0
    for l in open(os.path.join(d, 'cell_%d_%d_%d_D%d.txt' % key)):
        if l.startswith('FOUND:'): reps += 1
        elif l.startswith('INFO '): info = json.loads(l[5:])
    if info['route'] == 'direct':
        print('| (%d,%d,%d,%d) | %s | direct | %s labelled | %s | - | %s | - | %s |' % (key + ('{:,}'.format(reps), '{:,}'.format(info['labelled']), info['enum'].split('calls=')[1].split()[0] + ' calls', '{:,}'.format(info['in_C_tau_exact']), info.get('secs'))))
        continue
    inp = sum(b['inputs'] for b in info['branches']); nodes = sum(b.get('ext', {}).get('nodes', 0) for b in info['branches'])
    f7 = sum(b.get('ext', {}).get('hits_F7free', 0) for b in info['branches']); inc = sum(b.get('ext', {}).get('hits_in_C', 0) for b in info['branches'])
    print('| (%d,%d,%d,%d) | %s | recursion (%d branch%s) | %s | %s | %s | %s | %s | %s |' % (key + ('{:,}'.format(reps), len(info['branches']), 'es' if len(info['branches']) > 1 else '', '{:,}'.format(inp), '{:,}'.format(nodes), '{:,}'.format(f7), '{:,}'.format(inc), '{:,}'.format(info.get('connected_hits')), info.get('secs'))))
