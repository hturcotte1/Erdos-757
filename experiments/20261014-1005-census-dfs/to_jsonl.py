import gzip, json
n=0
with gzip.open('results/n12_m10_all.raw.gz','rt') as f, gzip.open('results/n12_m10_all.jsonl.gz','wt') as g:
    for line in f:
        if line.startswith('SOL'):
            t=line.split()
            g.write(json.dumps([[int(x) for x in e.split(',')] for e in t[2:]],separators=(',',':'))+"\n"); n+=1
print(n)
