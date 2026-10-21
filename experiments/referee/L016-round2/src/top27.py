"""Final step for cell(27,25,12,3) with own programs: own decompositions of (26,22) with slack 1, own 334 inputs from the
stored lists, own extension program with and without connectivity pruning."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rlib
CF = sys.argv[1]
n, m, t, D = 27, 25, 12, 3
print('branches', rlib.branches(n, m, t, D))
decs = rlib.my_decomps(26, 22, 1); print('decompositions of (26,22) with slack 1:', decs)
lines = []
for dec in decs:
    L = list(rlib.inputs_for(dec, CF, 3, 26)); print('  ', dec, 'inputs', len(L)); lines += L
print('total inputs', len(lines))
for mode in ([], ['noconn']):
    r = subprocess.run([rlib.REXT, 'ext', '26', '11', '3', '2'] + mode, input='\n'.join(lines) + '\n', capture_output=True, text=True)
    print('rext ext 26 11 3 2', ' '.join(mode), 'rc=%d' % r.returncode, 'outputs=%d' % len(r.stdout.split()), '|', ' | '.join(r.stderr.strip().splitlines()))
