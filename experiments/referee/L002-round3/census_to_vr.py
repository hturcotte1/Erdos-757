"""Referee round 3: dump the census output sets (results/realized_n12.json.gz) as 'n x1..xn' lines for ./vr set,
and their stored edge lists to a side file for comparison."""
import gzip, json, sys
R = '/home/user/Erdos-757/experiments/20261014-1005-census-dfs/results/realized_n12.json.gz'
d = json.load(gzip.open(R, 'rt'))
with open(sys.argv[1], 'w') as fe:
    for r in d:
        s = r['set']
        sys.stdout.write('%d %s\n' % (len(s), ' '.join(map(str, s))))
        fe.write(' '.join('%d,%d,%d' % tuple(e) for e in sorted(map(tuple, r['edges']))) + '\n')
sys.stderr.write('records=%d\n' % len(d))
