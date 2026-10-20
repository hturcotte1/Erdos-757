"""For every cell file in MYDIR (my genbg+hfilt output), compare with the prover's cell file: count, and (if both non-empty
and at most LIMIT classes) the classes by VF2 (iso_compare)."""
import sys, os, re, glob, subprocess
mydir, pdir, limit = sys.argv[1], sys.argv[2], int(sys.argv[3])
tot = 0; eq = 0; diff = []
for fn in sorted(glob.glob(os.path.join(mydir, 'cell_*.txt')), key=lambda f: tuple(map(int, re.findall(r'\d+', os.path.basename(f))))):
    key = tuple(map(int, re.findall(r'\d+', os.path.basename(fn))))
    mine = [l for l in open(fn) if l.startswith('FOUND')]
    summ = [l for l in open(fn) if l.startswith('SUMMARY')][-1]
    pf = os.path.join(pdir, os.path.basename(fn))
    theirs = [l for l in open(pf) if l.startswith('FOUND')]
    tot += 1
    status = 'count EQUAL' if len(mine) == len(theirs) else 'count DIFFERENT'
    extra = ''
    if len(mine) == len(theirs) and 0 < len(mine) <= limit:
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'iso_compare.py'), str(key[0]), fn, pf], capture_output=True, text=True).stdout.strip()
        extra = ' | VF2: ' + r
        if 'EQUAL' not in r: status = 'classes DIFFERENT'
    if status.endswith('EQUAL'): eq += 1
    else: diff.append(key)
    gen = re.search(r'total=(\d+)', summ).group(1)
    print('%s genbg=%s mine=%d prover=%d %s%s' % (key, gen, len(mine), len(theirs), status, extra))
print('cells compared %d, equal %d, different %s' % (tot, eq, diff))
