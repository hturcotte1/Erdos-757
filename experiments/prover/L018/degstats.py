import gzip, sys, collections
def parse(line):
    t = line.split()
    m = int(t[0]); E = [tuple(map(int, x.split('.'))) for x in t[1:1+m]]
    return E
for k in [4,5,6,8]:
    fn = f'/home/user/Erdos-757/experiments/20261027-0230-red-config/redk{k}_free_graphs.txt.gz'
    cnt = collections.Counter()
    for line in gzip.open(fn, 'rt'):
        if line.startswith('#'): continue
        E = parse(line)
        n = 1 + max(max(e) for e in E)
        d = [0]*n
        for e in E:
            for v in e: d[v] += 1
        cnt[(n, len(E), min(d), max(d))] += 1
    print(k, sorted(cnt.items()))
