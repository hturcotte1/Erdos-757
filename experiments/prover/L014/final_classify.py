"""(L014) python3 final_classify.py NV FILE... : classifies every HIT line (all unpruned extensions with tau >= T printed by
`ext_d ... noprune`) with the pure-Python verifier, independently of filt: linear?, contains F7?, (P3) (tested for the linear
F7-free ones), connected on NV vertices?  Prints the counts; 'members of C' must be 0 for Theorem 1."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyverify as pv
NV = int(sys.argv[1]); c = dict(hits=0, nonlinear=0, F7=0, F7free_P3_violated=0, members_of_C=0, disconnected=0, F7free_connected=0)
for fn in sys.argv[2:]:
    for l in open(fn):
        if not l.startswith('HIT:'): continue
        E = [tuple(map(int, x.split(','))) for x in re.findall(r'\((\d+,\d+,\d+)\)', l)]; c['hits'] += 1
        cn = pv.connected(E, range(NV)); c['disconnected'] += (not cn)
        if not pv.linear(E): c['nonlinear'] += 1; continue
        if pv.has_f7(E): c['F7'] += 1; continue
        c['F7free_connected'] += cn
        if not pv.p3(E, range(NV)): c['F7free_P3_violated'] += 1; continue
        c['members_of_C'] += 1; print('MEMBER', l.strip())
print('SUMMARY', ' '.join('%s=%d' % kv for kv in c.items()))
