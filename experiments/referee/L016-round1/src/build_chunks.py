#!/usr/bin/env python3
"""Referee L016 round 1 (own code): inputs of cell(25,19,10,3) (branch d=3, t'=9, S'=5: decompositions of (24,16,9)),
built from the lists with my own decomposition brute force, in the decomposition order of the worker's INFO line (so that
chunk c = inputs 25000c .. 25000c+24999 is comparable with the worker's chunk files), and writing only selected chunks.
Usage: build_chunks.py info_cell.txt.gz cell_24_16_9.txt chunks(comma) outdir
The (24,16,9,3) list is taken from the given file (file order matters for the chunk boundaries); other lists from the seeds."""
import sys, os, json, gzip, itertools, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mydecomp import decomps
import build_inputs as BI

def main():
    info_file, l24, chunks, outdir = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(',')], sys.argv[4]
    info = [l for l in gzip.open(info_file, 'rt') if l.startswith('INFO')][0]
    j = json.loads(info[5:])
    br = j['branches'][0]
    order = [tuple(sorted(tuple(c) for c in dec)) for dec, cnt in br['dec']]
    mine = sorted(tuple(sorted(d)) for d in decomps(24, 16, 9))
    assert sorted(order) == mine, 'decomposition sets differ'
    print('decompositions: mine %d, worker %d, equal as sets' % (len(mine), len(order)))
    want = {}
    for c in chunks:
        want[c] = open(os.path.join(outdir, 'chunk_%05d.txt' % c), 'w')
    idx = 0; total = 0
    for dec in order:
        groups = {}
        for ty in dec:
            groups[ty] = groups.get(ty, 0) + 1
        choices = []; cnt = 1
        for ty, k in sorted(groups.items()):
            if ty == (1, 0, 0):
                lst = [[]]
            elif ty == (24, 16, 9):
                lst = [BI.parse_found(l) for l in open(l24) if l.startswith('FOUND:')]
            else:
                lst = BI.load(ty[0], ty[1], ty[2], 3)
                if lst is None:
                    lst = []
                    print('MISSING list', ty)
            choices.append((ty, k, lst)); cnt *= math.comb(len(lst) + k - 1, k)
        lo, hi = idx, idx + cnt
        total += cnt
        sel = [c for c in want if not (25000 * (c + 1) <= lo or 25000 * c >= hi)]
        if sel and cnt:
            per_type = [list(itertools.combinations_with_replacement(range(len(lst)), k)) for (ty, k, lst) in choices]
            i = lo
            for combo in itertools.product(*per_type):
                c = i // 25000
                if c in want:
                    edges = []; off = 0
                    for (ty, k, lst), idxs in zip(choices, combo):
                        for ix in idxs:
                            edges += [(a + off, b + off, cc + off) for (a, b, cc) in lst[ix]]
                            off += ty[0]
                    assert off == 24
                    want[c].write('%d %s\n' % (len(edges), ' '.join('%d %d %d' % e for e in edges)))
                i += 1
        idx = hi
    print('TOTAL inputs', total)

if __name__ == '__main__':
    main()
