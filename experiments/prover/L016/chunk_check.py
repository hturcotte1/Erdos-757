"""(L016) Chunk-level comparison with the worker's run of cell(25,19,10,3) (experiments/20261017-2150-i11-n27, mystream2.py: the inputs of
the single branch d=3, t'=9 in the engine's order, cut into contiguous chunks of 25,000; per chunk a keys.gz file (the distinct canonical
forms of the connected survivors) and a meta.json (ext_d counters, number of HIT lines, number of connected survivors)).
python3 chunk_check.py INPUTFILE WORKERCHUNKDIR BIN chunk_index [chunk_index ...]
INPUTFILE = the full input list in the engine's order (gen_inputs.py 25 19 10 3, one branch only).  For every chunk index c: lines
[25000c, 25000c+25000) are run through BIN 24 9 10 3 2 | HIT lines | filt HIT 25 notau | SURVIVOR #conn=1 lines | canon 25 | sort -u,
and the ext_d SUMMARY counters, the number of HIT lines, the number of connected survivors and the key set are compared with the worker's."""
import sys, os, subprocess, gzip, json, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
inp, wdir, BIN = sys.argv[1], sys.argv[2], sys.argv[3]; idxs = [int(x) for x in sys.argv[4:]]
lines = open(inp).read().splitlines(); CH = 25000
allok = True
for c in idxs:
    chunk = lines[c * CH:(c + 1) * CH]
    with tempfile.TemporaryDirectory(dir=os.path.join(HERE, 'out')) as td:
        fin = os.path.join(td, 'in'); open(fin, 'w').write('\n'.join(chunk) + '\n')
        cmd = ("set -o pipefail; %s 24 9 10 3 2 < %s | awk '/^HIT:/{print; next} {print > \"%s/extsum\"}' | tee >(wc -l > %s/nhit) "
               "| %s HIT 25 notau | awk '/^SURVIVOR:/{print; next} {print > \"%s/filtsum\"}' | awk '/#conn=1$/' | tee >(wc -l > %s/nsurv) "
               "| cut -d'#' -f1 | %s 25 2>/dev/null | LC_ALL=C sort -u > %s/keys"
               % (BIN, fin, td, td, os.path.join(HERE, 'bin', 'filt'), td, td, os.path.join(HERE, 'bin', 'canon'), td))
        r = subprocess.run(['bash', '-c', cmd]); assert r.returncode == 0, r.returncode
        import time; time.sleep(1)
        ext = dict(kv.split('=') for kv in open(os.path.join(td, 'extsum')).read().split()[1:]); ext = {k: int(v) for k, v in ext.items()}
        nhit = int(open(os.path.join(td, 'nhit')).read().split()[0]); nsurv = int(open(os.path.join(td, 'nsurv')).read().split()[0])
        mine = set(l for l in open(os.path.join(td, 'keys')).read().splitlines() if l)
    meta = json.load(open(os.path.join(wdir, 'c%05d.meta.json' % c)))
    theirs = set(l for l in gzip.open(os.path.join(wdir, 'c%05d.keys.gz' % c), 'rt').read().splitlines() if l)
    ok = (ext == meta['ext'] and nhit == meta['nhit'] and nsurv == meta['nsurv'] and mine == theirs and len(chunk) == meta['ninputs'])
    allok = allok and ok
    print('chunk %d (inputs %d..%d): mine ext=%s nhit=%d nsurv=%d keys=%d | worker ext=%s nhit=%d nsurv=%d keys=%d -> %s'
          % (c, c * CH + 1, c * CH + len(chunk), ext, nhit, nsurv, len(mine), meta['ext'], meta['nhit'], meta['nsurv'], len(theirs), 'IDENTICAL' if ok else 'DIFFERENT'), flush=True)
print('RESULT chunks', idxs, 'ALL IDENTICAL' if allok else 'DIFFERENCES')
