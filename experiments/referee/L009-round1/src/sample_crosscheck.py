"""Referee L009: cross-check the prover's labelled extension runs against the referee's ext1 on random samples of the prover's
labelled inputs (rebuild of (17,13,7): inT17.txt / hitsT17.txt; final step: inH18.txt).  Usage: sample_crosscheck.py K SEED"""
import random, subprocess, sys, re
K, seed = int(sys.argv[1]), int(sys.argv[2]); random.seed(seed)
O = '/home/user/Erdos-757/experiments/referee/L009-round1/out/pr/'
B = '/home/user/Erdos-757/experiments/referee/L009-round1/bin/'
def edges_of_line(l):
    t = list(map(int, l.split()))[1:]; return [tuple(sorted(t[3*i:3*i+3])) for i in range(len(t) // 3)]
# (a) rebuild (17,13,7): prover hits for the sampled inputs vs referee ext1 hits
inp = open(O + 'inT17.txt').read().splitlines(); S = random.sample(range(len(inp)), K)
key = {frozenset(edges_of_line(inp[i])): i for i in S}
prov = set()
for l in open(O + 'hitsT17.txt'):
    if not l.startswith('HIT:'): continue
    es = [tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)]
    if frozenset(es[:-3]) in key: prov.add(frozenset(es))
txt = ''.join('I: ' + ' '.join('(%d,%d,%d)' % e for e in edges_of_line(inp[i])) + '\n' for i in S)
r = subprocess.run([B + 'ext1', '16', '7', '3'], input=txt, capture_output=True, text=True)
mine = set(frozenset(tuple(sorted(map(int, t.split(',')))) for t in re.findall(r'\(([\d,]+)\)', l)) for l in r.stdout.splitlines() if l.startswith('X'))
print('(a) rebuild sample of', K, 'labelled inputs: prover hits', len(prov), 'referee hits', len(mine), 'identical:', prov == mine, '|', r.stderr.strip())
# (b) final step: referee ext1 on a random sample of the prover's labelled inputs inH18.txt, and the prover's ext_indep3 on the same sample
inp = open(O + 'inH18.txt').read().splitlines(); S = random.sample(range(len(inp)), K)
txt = ''.join('I: ' + ' '.join('(%d,%d,%d)' % e for e in edges_of_line(inp[i])) + '\n' for i in S)
r = subprocess.run([B + 'ext1', '17', '8', '3'], input=txt, capture_output=True, text=True)
r2 = subprocess.run([B + 'ext_indep3_prover', '17', '7', '3'], input=''.join(inp[i] + '\n' for i in S), capture_output=True, text=True)
print('(b) final-step sample of', K, 'labelled inputs: referee:', r.stderr.strip(), '| prover ext_indep3:', r2.stdout.strip().splitlines()[-1])
