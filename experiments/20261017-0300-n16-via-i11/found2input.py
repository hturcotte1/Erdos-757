import re,sys
for f in sys.argv[1:]:
    for l in open(f):
        if l.startswith('FOUND') and l.endswith(')\n'):
            es=[tuple(map(int,t.split(','))) for t in re.findall(r'\(([\d,]+)\)',l)]
            print(len(es)," ".join("%d %d %d"%e for e in es))
