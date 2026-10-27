import json, gzip, subprocess, sys, os, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, ROOT)
from e757.core import ap_edges
I11 = os.path.join(HERE, 'i11')

def graph_of_set(A):
    A = sorted(A); idx = {x: i for i, x in enumerate(A)}
    return len(A), [tuple(sorted((idx[a], idx[b], idx[c]))) for a, b, c in ap_edges(A)]

def line(n, edges):
    return "%d %d %s" % (n, len(edges), " ".join("%d,%d,%d" % tuple(e) for e in edges))

def run_eval(lines):
    """lines: list of graph lines -> list of (n,m,tau,slack,cc,maxdeg,ncomp,iso)"""
    p = subprocess.run([I11, 'eval'], input="\n".join(lines) + "\n", capture_output=True, text=True, check=True)
    out = []
    for l in p.stdout.strip().split("\n"):
        out.append(tuple(int(x) for x in l.split()) if l[0] != 'P' else None)
    return out

def induced(n, edges, S):
    S = sorted(S); mp = {v: i for i, v in enumerate(S)}
    return len(S), [tuple(mp[v] for v in e) for e in edges if all(v in mp for v in e)]

def load_pieces():
    P = {}
    sm = json.load(open(os.path.join(ROOT, 'data/small_records.json')))
    for k, v in sm['sets'].items():
        P['rec' + k] = graph_of_set(v['set'])
    P['Abase'] = P['rec14']
    cls = []
    with gzip.open(os.path.join(ROOT, 'data/census_n14_m12_classes.jsonl.gz')) as f:
        for l in f:
            d = json.loads(l); cls.append((d['n'], [tuple(sorted(e)) for e in d['edges']]))
    fam = json.load(open(os.path.join(ROOT, 'data/reader_5_9_family.json')))['family']
    for x in fam:
        if x['K'] <= 8: P['S%d' % x['K']] = graph_of_set(x['set'])
    for c in ['C003-reader-5-9-K6', 'C004-lemmaE-SK5-E1', 'C005-lemmaE-SK6-E1']:
        d = json.load(open(os.path.join(ROOT, 'results/claims/%s.json' % c)))
        P[c[:4]] = graph_of_set(d['set'])
    return P, cls
