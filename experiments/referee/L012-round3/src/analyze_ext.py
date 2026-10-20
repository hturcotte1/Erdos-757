"""Referee L012 round 3: analyse an xext output file.  Tallies the SUMMARY and the per-survivor flags (#conn, #tauok, #maxdeg), writes the
connected survivors to OUT, and matches them (igraph BLISS canonical forms of the 2-coloured incidence graph; equal form => isomorphic by
construction) against the representatives in REPS: every survivor must match a representative, every representative must be hit.
A random sample of matches is confirmed with networkx VF2.  Usage: python3 analyze_ext.py XEXT_OUT n REPS OUT"""
import sys, re, random
sys.path.insert(0, '/home/user/Erdos-757/experiments/referee/L012-round3/src')
from iso_check import canon_igraph, parse, vf2_iso
fn, n, repsfn, outfn = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
summary = None; surv = []; flags = {}
for l in open(fn):
    if l.startswith('SUMMARY'): summary = l.strip()
    elif l.startswith('HIT:'):
        es = [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]
        fl = dict(kv.split('=') for kv in re.findall(r'#(\w+=\d+)', l))
        key = (fl['conn'], fl['tauok'], fl['maxdeg']); flags[key] = flags.get(key, 0) + 1
        if fl['conn'] == '1': surv.append(es)
print(summary)
print('survivor flags (conn,tauok,maxdeg):', flags)
with open(outfn, 'w') as f:
    for es in surv: f.write('FOUND: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n')
reps = parse(repsfn)
rf = {}
for i, e in enumerate(reps): rf.setdefault(canon_igraph(e, n), []).append(i)
assert all(len(v) == 1 for v in rf.values()), 'representatives not pairwise non-isomorphic under BLISS'
myforms = set(); hit = [0] * len(reps); unmatched = 0; pairs = []
for es in surv:
    f = canon_igraph(es, n); myforms.add(f)
    if f in rf: hit[rf[f][0]] += 1; pairs.append((es, rf[f][0]))
    else: unmatched += 1
print('connected survivors', len(surv), '-> distinct BLISS classes', len(myforms), '; representatives', len(reps), '; UNMATCHED survivors', unmatched,
      '; representatives hit', sum(1 for h in hit if h), 'of', len(reps))
random.seed(3); samp = random.sample(pairs, min(150, len(pairs)))
print('VF2 confirmation on a sample of matches:', sum(vf2_iso(e, reps[i], n) for e, i in samp), 'of', len(samp))
