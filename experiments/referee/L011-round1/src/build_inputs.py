"""Referee L011: build extension inputs from genbg CLASS REPRESENTATIVES (one per isomorphism class of each component cell).
Usage: build_inputs.py OUT MODE SLOT1 SLOT2 ...
  MODE  = C   : component classes restricted to members of C (bin/rfilt: linear, F7-free, P3)
          all : every Delta<=3 class of the cell (superset; robustness run)
  SLOT  = AP | ISO | n_m_t   (cell file out/g_n_m_t_d3.txt)
Repeated identical cell slots are combined as multisets (i <= j), so every isomorphism class of the disjoint union occurs
exactly once.  Output lines "m a1 b1 c1 ..." (numeric format), components on consecutive point blocks in slot order."""
import sys, re, subprocess, itertools, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
out, mode, slots = sys.argv[1], sys.argv[2], sys.argv[3:]
def parse(l): return [tuple(map(int, t.split(','))) for t in re.findall(r'\((\d+,\d+,\d+)\)', l)]
def load(slot):
    if slot == 'AP': return [[(0, 1, 2)]], 3
    if slot == 'ISO': return [[]], 1
    n, m, t = map(int, slot.split('_'))
    f = os.path.join(R, 'out', 'g_%d_%d_%d_d3.txt' % (n, m, t))
    L = [parse(l) for l in open(f) if l.startswith('G:')]
    if mode == 'C' and L:
        data = ''.join('G: ' + ' '.join('(%d,%d,%d)' % e for e in es) + '\n' for es in L)
        r = subprocess.run([os.path.join(R, 'bin', 'rfilt'), str(n), 'G', 'v'], input=data, capture_output=True, text=True, check=True)
        keep = []
        for l in r.stdout.split('\n'):
            if l.startswith('R:'):
                if ' lin=1 f7=0 p3ok=1 ' in l: keep.append(parse(l.split('|')[-1]))
        L = keep
    for es in L:
        assert len(es) == m and set(v for e in es for v in e) == set(range(n)), slot
    return L, n
loaded = [(s, load(s)) for s in slots]
# group identical slots to take multisets
groups = []
for s, (L, n) in loaded:
    if groups and groups[-1][0] == s: groups[-1][2] += 1
    else: groups.append([s, (L, n), 1])
choices = []
for s, (L, n), k in groups:
    choices.append([(c, n) for c in itertools.combinations_with_replacement(range(len(L)), k)])
cnt = 0; total_n = None
with open(out, 'w') as f:
    for combo in itertools.product(*choices):
        es = []; off = 0
        for (s, (L, n), k), (idxs, nn) in zip(groups, combo):
            for i in idxs:
                es += [tuple(v + off for v in e) for e in L[i]]; off += n
        total_n = off
        f.write('%d ' % len(es) + ' '.join('%d %d %d' % e for e in es) + '\n'); cnt += 1
print(out, mode, slots, 'inputs:', cnt, 'points:', total_n, 'class counts per slot:', [len(L) for s, (L, n) in loaded])
