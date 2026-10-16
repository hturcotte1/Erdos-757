"""Convert the census DFS output (json edge lists) to 'i,j,k ...' lines for ./vr pat 12."""
import sys, gzip, json
for l in gzip.open(sys.argv[1], 'rt'):
    sys.stdout.write(' '.join('%d,%d,%d' % tuple(e) for e in sorted(map(tuple, json.loads(l)))) + '\n')
