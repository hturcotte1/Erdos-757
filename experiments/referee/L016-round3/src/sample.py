import sys, random
lines = open(sys.argv[1]).read().split('\n'); lines = [l for l in lines if l.strip()]
k = int(sys.argv[2]); rnd = random.Random(int(sys.argv[3]))
for l in (rnd.sample(lines, k) if k < len(lines) else lines): print(l)
