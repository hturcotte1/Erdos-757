"""Build extension inputs from enumerator outputs.  caseA: every labelled connected (12,10,>=5) maxdeg<=3 graph R (vertices 0..11)
plus the edge (12,13,14);  caseB: every labelled connected (15,11,>=6) maxdeg<=3 graph.  Lines "m a b c ...". """
import re, sys
def parse(path):
    for l in open(path):
        if l.startswith('FOUND:'):
            yield [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,]+)\)', l)]
mode, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
cnt = 0
with open(out, 'w') as f:
    for es in parse(src):
        if mode == 'A':
            assert len(es) == 10 and set().union(*es) == set(range(12)); es = es + [(12, 13, 14)]
        else:
            assert len(es) == 11 and set().union(*es) == set(range(15))
        f.write('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) + '\n'); cnt += 1
print(mode, 'graphs written:', cnt)
