import sys, json, os
n,m,t,D = map(int, sys.argv[1:5]); src = 'out/cells/cell_%d_%d_%d_D%d.txt' % (n,m,t,D)
dst = 'lists/cell_%d_%d_%d_D%d.txt' % (n,m,t,D)
found = [l for l in open(src) if l.startswith('FOUND:')]
with open(dst, 'w') as f:
    f.write('# cell (n,m,tau,Delta)=(%d,%d,%d,%d) classes=%d ; connected members of C (linear, F7-free, e(S)<=|S|-2), tau exactly, max degree <= Delta; one canonical class per line (engine format); computed in experiments/20261027-0340-induction-n28-n29-f25 (L012 engine, streamed L016 driver); unrefereed\n' % (n,m,t,D,len(found)))
    f.writelines(found)
json.dump(dict(cell=[n,m,t,D], classes=len(found)), open(dst[:-4] + '.json', 'w'))
print(dst, len(found))
