"""Referee L014 round 2: compare two lists of hypergraphs as sets of isomorphism classes, with nauty labelg (own build of
unmodified nauty 2.8.8) applied to the vertex/edge incidence graph with the 2-colour partition (-f).  Inputs: files with lines
'N M a b c ...' (own format) or 'FOUND: (a,b,c) ...' (prover's cell files).  Prints sizes, number of distinct classes, overlap.
usage: python3 canon_cmp.py n m fileA fileB [--dump PREFIX]"""
import sys, re, subprocess, os, tempfile
LABELG = '/home/user/Erdos-757/experiments/referee/L014-round2/out/nbin/labelg'
def read_hg(fn, n, m):
    out = []
    op = __import__('gzip').open if fn.endswith('.gz') else open
    with op(fn, 'rt') as f:
        for l in f:
            if l.startswith('FOUND:') or l.startswith('SURVIVOR:') or l.startswith('HIT:'):
                es = [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]
            elif l.startswith('MEMBER'):
                a = list(map(int, l.split(':', 1)[1].split())); es = [tuple(a[2 + 3*i: 5 + 3*i]) for i in range(a[1])]
                assert a[0] == n
            elif l[:1].isdigit():
                a = list(map(int, l.split())); es = [tuple(a[2 + 3*i: 5 + 3*i]) for i in range(a[1])]
                assert a[0] == n
            else: continue
            assert len(es) == m, (fn, l[:80])
            out.append(es)
    return out
def g6(n, es):
    """graph6 of the vertex/edge incidence graph: vertex nodes 0..n-1, edge nodes n..n+m-1 (only vertex-edge adjacencies)."""
    N = n + len(es); nbits = N * (N - 1) // 2; nbytes = (nbits + 5) // 6
    b = bytearray(nbytes)
    for j, e in enumerate(es):
        col = n + j; base = col * (col - 1) // 2
        for v in e:
            pos = base + v; b[pos // 6] |= 1 << (5 - pos % 6)
    return chr(N + 63) + ''.join(chr(x + 63) for x in b)
def g6_slow(n, es):
    N = n + len(es); adj = set()
    for j, e in enumerate(es):
        for v in e: adj.add((v, n + j))
    bits = []
    for j in range(1, N):
        for i in range(j):
            bits.append(1 if (i, j) in adj or (j, i) in adj else 0)
    while len(bits) % 6: bits.append(0)
    s = chr(N + 63)
    for k in range(0, len(bits), 6):
        v = 0
        for bb in bits[k:k+6]: v = 2 * v + bb
        s += chr(v + 63)
    return s
def canon(n, m, graphs):
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.g6', dir='/home/user/Erdos-757/experiments/referee/L014-round2/out') as f:
        for es in graphs: f.write(g6(n, es) + '\n')
        fn = f.name
    part = 'a' * n + 'b' * m
    r = subprocess.run([LABELG, '-q', '-f' + part, fn], capture_output=True, text=True)
    os.remove(fn)
    assert r.returncode == 0, r.stderr
    out = r.stdout.split()
    assert len(out) == len(graphs)
    return out
if __name__ == '__main__':
    n, m = int(sys.argv[1]), int(sys.argv[2]); A = read_hg(sys.argv[3], n, m); Bl = read_hg(sys.argv[4], n, m)
    ca = canon(n, m, A); cb = canon(n, m, Bl); sa, sb = set(ca), set(cb)
    print('CMP n=%d m=%d A=%s (%d graphs, %d classes) B=%s (%d graphs, %d classes) common=%d onlyA=%d onlyB=%d %s' % (
        n, m, os.path.basename(sys.argv[3]), len(A), len(sa), os.path.basename(sys.argv[4]), len(Bl), len(sb), len(sa & sb), len(sa - sb), len(sb - sa),
        'IDENTICAL' if sa == sb else 'DIFFERENT'))
