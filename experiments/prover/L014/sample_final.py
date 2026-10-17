"""(L014) Sample for cross-check (e2).  python3 sample_final.py INPUTS TAGS NOPRUNE_OUT OUT SEED PER_DEC_SPEC MAX_WITH_HITS
INPUTS/TAGS from gen_inputs.py (one tag line per input: d, t', decomposition index, class indices); NOPRUNE_OUT = output of
`ext_d ... noprune` on INPUTS (HIT lines; their first m(G) edges are the input's edges in input order).  Selects, with
random.Random(SEED): for each decomposition index i, min(size_i, PER_DEC_SPEC[i]) random inputs; plus up to MAX_WITH_HITS random
inputs among those with at least one noprune hit.  Writes the selected input lines (deduplicated, in input order) to OUT."""
import sys, re, random
inp, tags, nop, out, seed = sys.argv[1:6]; per = list(map(int, sys.argv[6].split(','))); mx = int(sys.argv[7])
lines = open(inp).read().splitlines(); tg = open(tags).read().splitlines(); assert len(lines) == len(tg)
dec = [int(re.search(r'dec=(\d+)', t).group(1)) for t in tg]
key = {}
for i, l in enumerate(lines):
    a = list(map(int, l.split())); m = a[0]; key[tuple(tuple(a[1 + 3 * j: 4 + 3 * j]) for j in range(m))] = i
m0 = int(lines[0].split()[0]) if lines else 0
withhit = set()
for l in open(nop):
    if l.startswith('HIT:'):
        es = [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
        # the input has m(G) edges; inputs of one branch all have the same m(G) = m0
        withhit.add(key[tuple(es[:m0])])
R = random.Random(int(seed)); chosen = set()
for i in sorted(set(dec)):
    idx = [j for j in range(len(lines)) if dec[j] == i]
    chosen.update(R.sample(idx, min(len(idx), per[i] if i < len(per) else 0)))
wh = sorted(withhit); chosen.update(R.sample(wh, min(len(wh), mx)))
with open(out, 'w') as f:
    for j in sorted(chosen): f.write(lines[j] + '\n')
print('inputs %d, decompositions %s, inputs with noprune hits %d, selected %d (of them with hits %d)' % (
    len(lines), {i: dec.count(i) for i in sorted(set(dec))}, len(withhit), len(chosen), len(chosen & withhit)))
